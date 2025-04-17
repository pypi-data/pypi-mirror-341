/*
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

use std::fmt;
use std::fmt::Display;
use std::sync::Arc;

use itertools::Itertools;
use pyrefly_derive::TypeEq;
use pyrefly_derive::Visit;
use pyrefly_derive::VisitMut;
use ruff_python_ast::name::Name;
use starlark_map::small_map::SmallMap;
use vec1::Vec1;

use crate::types::types::Type;
use crate::util::visit::Visit;
use crate::util::visit::VisitMut;

/// The `TypeInfo` datatype represents type information associated with a
/// name or expression in a control flow context.
///
/// This is distinct from `Type` because expressions and bound names can
/// track, in addition to the type of the top-level value, zero or more
/// attribute narrows where we have access to additional control-flow-dependent
/// knowledge about how a chain of attribute accesses will resolve.
///
/// For example:
///
/// ```python
/// x: Foo
/// if x.foo is not None x.foo.bar is None and x.baz is None:
///     # here, `x` is still `Foo` but we also can narrow
///     # `x.foo`, `x.foo.bar`, and `x.baz`.
/// ```
#[derive(Debug, Clone, PartialEq, Eq, Visit, VisitMut, TypeEq)]
pub struct TypeInfo {
    ty: Type,
    attrs: NarrowedAttrs,
}

impl TypeInfo {
    pub fn of_ty(ty: Type) -> Self {
        Self {
            ty,
            attrs: NarrowedAttrs::new(),
        }
    }

    pub fn with_ty(self, ty: Type) -> Self {
        Self {
            ty,
            attrs: self.attrs,
        }
    }

    pub fn type_at_name(&self, name: &Name) -> Option<&Type> {
        match self.attrs.get(name) {
            None | Some(NarrowedAttr::WithoutRoot(..)) => None,
            Some(NarrowedAttr::Leaf(ty)) | Some(NarrowedAttr::WithRoot(ty, _)) => Some(ty),
        }
    }

    pub fn at_name(&self, name: &Name, fallback: impl Fn() -> Type) -> Self {
        match self.attrs.get(name) {
            None => TypeInfo::of_ty(fallback()),
            Some(NarrowedAttr::Leaf(ty)) => Self::of_ty(ty.clone()),
            Some(NarrowedAttr::WithoutRoot(attrs)) => Self {
                ty: fallback(),
                attrs: attrs.clone(),
            },
            Some(NarrowedAttr::WithRoot(ty, attrs)) => Self {
                ty: ty.clone(),
                attrs: attrs.clone(),
            },
        }
    }

    pub fn with_narrow(&self, names: &Vec1<Name>, ty: Type) -> Self {
        let mut type_info = self.clone();
        type_info.add_narrow(names, ty);
        type_info
    }

    /// Join two `TypeInfo`s together:
    /// - We'll take the union of the top-level types
    /// - At attribute chains where all branches narrow, take a union of the narrowed types.
    /// - Drop narrowing for attribute chains where at least one branch does not narrow
    pub fn join(branches: Vec<Self>, union_types: &impl Fn(Vec<Type>) -> Type) -> Self {
        let (tys, attrs) = branches
            .into_iter()
            .map(|TypeInfo { ty, attrs }| (ty, attrs))
            .unzip();
        let ty = union_types(tys);
        let attrs = NarrowedAttrs::join(attrs, union_types);
        Self { ty, attrs }
    }

    fn add_narrow(&mut self, names: &Vec1<Name>, ty: Type) {
        if let Some((name, more_names)) = names.split_first() {
            self.attrs.add_narrow(name.clone(), more_names, ty)
        } else {
            unreachable!(
                "We know the Vec1 will split. But the safe API, split_off_first, is not ref-based."
            )
        }
    }

    pub fn ty(&self) -> &Type {
        &self.ty
    }

    pub fn into_ty(self) -> Type {
        self.ty
    }

    pub fn arc_clone(self: Arc<Self>) -> Self {
        Arc::unwrap_or_clone(self)
    }

    pub fn arc_clone_ty(self: Arc<Self>) -> Type {
        self.arc_clone().into_ty()
    }
}

impl Display for TypeInfo {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        self.ty().fmt(f)?;
        if let NarrowedAttrs(Some(_)) = &self.attrs {
            write!(f, " ({})", self.attrs)?;
        }
        Ok(())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, TypeEq)]
struct NarrowedAttrs(Option<Box<SmallMap<Name, NarrowedAttr>>>);

impl NarrowedAttrs {
    fn new() -> Self {
        Self(None)
    }

    fn add_narrow(&mut self, name: Name, more_names: &[Name], ty: Type) {
        if self.0.is_none() {
            self.0 = Some(Box::new(SmallMap::with_capacity(1)))
        }
        match &mut self.0 {
            None => unreachable!("We just ensured that we have a map of attrs"),
            Some(box attrs) => {
                let attr = match attrs.shift_remove(&name) {
                    Some(attr) => attr.with_narrow(more_names, ty),
                    None => NarrowedAttr::new(more_names, ty),
                };
                attrs.insert(name, attr);
            }
        }
    }

    fn get(&self, name: &Name) -> Option<&NarrowedAttr> {
        match &self.0 {
            None => None,
            Some(box attrs) => attrs.get(name),
        }
    }

    fn of_narrow(name: Name, more_names: &[Name], ty: Type) -> Self {
        let mut attrs = SmallMap::with_capacity(1);
        attrs.insert(name.clone(), NarrowedAttr::new(more_names, ty));
        Self(Some(Box::new(attrs)))
    }

    fn join(mut branches: Vec<Self>, union_types: &impl Fn(Vec<Type>) -> Type) -> Self {
        let n = branches.len();
        if n == 0 {
            // Exit early on empty branches - the split_off call is only legal
            // if the vec has at least one element.
            return Self::new();
        }
        let mut tail = branches.split_off(1);
        match branches.into_iter().next() {
            None => {
                // Not actually reachable since we exit early for n == 0, but needed for type
                // safety (and if split_off behaved differently it would be reachable)
                Self::new()
            }
            Some(first) => match first.0 {
                None => Self::new(),
                Some(box attrs) => {
                    let attrs: SmallMap<_, _> = attrs
                        .into_iter()
                        .filter_map(|(name, attr)| {
                            let mut attr_vec = vec![attr];
                            attr_vec.extend(
                                tail.iter_mut()
                                    .filter_map(|attrs| attrs.shift_remove(&name)),
                            );
                            // If any map lacked this name, we just drop it. Only join if all maps have it.
                            if attr_vec.len() == n {
                                NarrowedAttr::join(attr_vec, union_types)
                                    .map(move |attr| (name, attr))
                            } else {
                                None
                            }
                        })
                        .collect();
                    if attrs.is_empty() {
                        Self::new()
                    } else {
                        Self(Some(Box::new(attrs)))
                    }
                }
            },
        }
    }

    fn shift_remove(&mut self, name: &Name) -> Option<NarrowedAttr> {
        match &mut self.0 {
            None => None,
            Some(box attrs) => attrs.shift_remove(name),
        }
    }

    fn fmt_with_prefix(&self, prefix: &mut Vec<String>, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        if let Some(attrs) = &self.0 {
            let mut first = true;
            for (name, value) in attrs.iter() {
                if first {
                    first = false
                } else {
                    write!(f, ", ")?;
                }
                match value {
                    NarrowedAttr::Leaf(ty) => Self::fmt_type_with_label(prefix, name, ty, f),
                    NarrowedAttr::WithRoot(ty, attrs) => {
                        Self::fmt_type_with_label(prefix, name, ty, f)?;
                        write!(f, ", ")?;
                        attrs.fmt_with_prefix_and_name(prefix, name, f)
                    }
                    NarrowedAttr::WithoutRoot(attrs) => {
                        attrs.fmt_with_prefix_and_name(prefix, name, f)
                    }
                }?;
            }
        }
        Ok(())
    }

    fn fmt_with_prefix_and_name<'a>(
        &self,
        prefix: &mut Vec<String>,
        name: &'a Name,
        f: &mut fmt::Formatter<'_>,
    ) -> fmt::Result {
        prefix.push(name.to_string());
        self.fmt_with_prefix(prefix, f)?;
        prefix.pop();
        Ok(())
    }

    fn fmt_type_with_label(
        prefix: &[String],
        name: &Name,
        ty: &Type,
        f: &mut fmt::Formatter<'_>,
    ) -> fmt::Result {
        write!(
            f,
            "_.{}{}{}: {}",
            prefix.iter().join("."),
            if prefix.is_empty() { "" } else { "." },
            name,
            ty
        )
    }
}

impl Visit<Type> for NarrowedAttrs {
    fn recurse<'a>(&'a self, f: &mut dyn FnMut(&'a Type)) {
        if let Some(attrs) = &self.0 {
            attrs.values().for_each(|value| {
                value.visit(f);
            })
        }
    }
}

impl VisitMut<Type> for NarrowedAttrs {
    fn recurse_mut(&mut self, f: &mut dyn FnMut(&mut Type)) {
        if let Some(attrs) = &mut self.0 {
            attrs.values_mut().for_each(|value| {
                value.visit_mut(f);
            })
        }
    }
}

impl Display for NarrowedAttrs {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        self.fmt_with_prefix(&mut Vec::new(), f)
    }
}

/// A `NarrowedAttr` represents a single attribute within a tree of narrowed
/// attributes. The attribute itself may or may not be narrowed, and it may or
/// may not have any sub-attributes (but at least one must be the case, or it
/// wouldn't be in the tree at all)
#[derive(Debug, Clone, Visit, VisitMut, PartialEq, Eq, TypeEq)]
enum NarrowedAttr {
    /// This attribute is narrowed, and has no narrowed sub-attributes (Leaf)
    Leaf(Type),
    /// This attribute is narrowed, and has one or more narrowed sub-attributes (WithRoot)
    WithRoot(Type, NarrowedAttrs),
    /// This attribute is not narrowed, and has one or more narrowed sub-attributes (WithoutRoot)
    WithoutRoot(NarrowedAttrs),
}

impl NarrowedAttr {
    fn new(names: &[Name], ty: Type) -> Self {
        match names {
            [] => Self::Leaf(ty),
            [name, more_names @ ..] => {
                Self::WithoutRoot(NarrowedAttrs::of_narrow((*name).clone(), more_names, ty))
            }
        }
    }

    fn with_narrow(self, names: &[Name], narrowed_ty: Type) -> Self {
        match names {
            [] => {
                // We are setting a narrow at the current node (potentially overriding an existing narrow; it is
                // up to callers to make sure this works correctly, we just take what was given).
                match self {
                    Self::Leaf(_) => Self::Leaf(narrowed_ty),
                    Self::WithRoot(_, attrs) | Self::WithoutRoot(attrs) => {
                        Self::WithRoot(narrowed_ty, attrs)
                    }
                }
            }
            [name, more_names @ ..] => {
                // We are setting a narrow in a subtree. We need to preserve any existing tree.
                match self {
                    Self::Leaf(root_ty) => {
                        let attrs =
                            NarrowedAttrs::of_narrow((*name).clone(), more_names, narrowed_ty);
                        Self::WithRoot(root_ty, attrs)
                    }
                    Self::WithoutRoot(mut attrs) => {
                        attrs.add_narrow((*name).clone(), more_names, narrowed_ty);
                        Self::WithoutRoot(attrs)
                    }
                    Self::WithRoot(root_ty, mut attrs) => {
                        attrs.add_narrow((*name).clone(), more_names, narrowed_ty);
                        Self::WithRoot(root_ty, attrs)
                    }
                }
            }
        }
    }

    fn join(branches: Vec<Self>, union_types: &impl Fn(Vec<Type>) -> Type) -> Option<Self> {
        fn monadic_push_option<T>(acc: &mut Option<Vec<T>>, item: Option<T>) {
            match item {
                None => *acc = None,
                Some(item) => {
                    if let Some(acc) = acc {
                        acc.push(item)
                    }
                }
            };
        }
        let mut ty_branches = Some(Vec::with_capacity(branches.len()));
        let mut attrs_branches = Some(Vec::with_capacity(branches.len()));
        for attr in branches {
            let (ty, attrs) = match attr {
                // TODO(stroxler) It might be worth making NarrowedAttr a tuple to start
                // with; the more descriptive types don't seem to benefit us much in practice.
                Self::WithRoot(ty, attrs) => (Some(ty), Some(attrs)),
                Self::Leaf(ty) => (Some(ty), None),
                Self::WithoutRoot(attrs) => (None, Some(attrs)),
            };
            monadic_push_option(&mut ty_branches, ty);
            monadic_push_option(&mut attrs_branches, attrs);
            if let (None, None) = (&ty_branches, &attrs_branches) {
                // Not needed for correctness, but saves some work.
                return None;
            }
        }
        let ty = ty_branches.map(union_types);
        let attrs =
            attrs_branches.map(|attrs_branches| NarrowedAttrs::join(attrs_branches, union_types));
        match (ty, attrs) {
            (None, None | Some(NarrowedAttrs(None))) => None,
            (Some(ty), None | Some(NarrowedAttrs(None))) => Some(Self::Leaf(ty)),
            (Some(ty), Some(attrs)) => Some(Self::WithRoot(ty, attrs)),
            (None, Some(attrs)) => Some(Self::WithoutRoot(attrs)),
        }
    }
}

#[cfg(test)]
mod tests {

    use ruff_python_ast::name::Name;
    use vec1::Vec1;

    use crate::types::class::ClassType;
    use crate::types::class::TArgs;
    use crate::types::display::tests::fake_class;
    use crate::types::type_info::TypeInfo;
    use crate::types::types::Type;

    fn fake_class_type(class_name: &str) -> Type {
        Type::ClassType(ClassType::new(
            fake_class(class_name, "class_defs_module", 5, Vec::new()),
            TArgs::default(),
        ))
    }

    #[test]
    fn test_type_info_one_level_only() {
        let x = || Name::new_static("x");
        let y = || Name::new_static("y");
        let mut type_info = TypeInfo::of_ty(fake_class_type("Foo"));
        assert_eq!(type_info.to_string(), "Foo");
        type_info.add_narrow(&Vec1::new(x()), fake_class_type("Bar"));
        assert_eq!(type_info.to_string(), "Foo (_.x: Bar)");
        type_info.add_narrow(&Vec1::new(y()), fake_class_type("Baz"));
        assert_eq!(type_info.to_string(), "Foo (_.x: Bar, _.y: Baz)");
    }

    #[test]
    fn test_type_info_adding_sub_attributes() {
        let x = || Name::new_static("x");
        let y = || Name::new_static("y");
        let z = || Name::new_static("z");
        let mut type_info = TypeInfo::of_ty(fake_class_type("Foo"));
        type_info.add_narrow(&Vec1::new(x()), fake_class_type("Bar"));
        type_info.add_narrow(&Vec1::from_vec_push(vec![x()], y()), fake_class_type("Baz"));
        assert_eq!(type_info.to_string(), "Foo (_.x: Bar, _.x.y: Baz)");
        type_info.add_narrow(&Vec1::from_vec_push(vec![x()], z()), fake_class_type("Qux"));
        assert_eq!(
            type_info.to_string(),
            "Foo (_.x: Bar, _.x.y: Baz, _.x.z: Qux)"
        );
        type_info.add_narrow(
            &Vec1::from_vec_push(vec![x(), y()], x()),
            fake_class_type("Foo"),
        );
        assert_eq!(
            type_info.to_string(),
            "Foo (_.x: Bar, _.x.z: Qux, _.x.y: Baz, _.x.y.x: Foo)"
        );
    }

    #[test]
    fn test_type_info_creating_subtrees_and_narrowing_roots() {
        let x = || Name::new_static("x");
        let y = || Name::new_static("y");
        let z = || Name::new_static("z");
        let w = || Name::new_static("w");
        let mut type_info = TypeInfo::of_ty(fake_class_type("Foo"));
        type_info.add_narrow(
            &Vec1::from_vec_push(vec![x(), y()], z()),
            fake_class_type("Bar"),
        );
        assert_eq!(type_info.to_string(), "Foo (_.x.y.z: Bar)");
        type_info.add_narrow(
            &Vec1::from_vec_push(vec![x(), y()], w()),
            fake_class_type("Baz"),
        );
        assert_eq!(type_info.to_string(), "Foo (_.x.y.z: Bar, _.x.y.w: Baz)");
        type_info.add_narrow(&Vec1::from_vec_push(vec![x()], y()), fake_class_type("Qux"));
        assert_eq!(
            type_info.to_string(),
            "Foo (_.x.y: Qux, _.x.y.z: Bar, _.x.y.w: Baz)"
        );
    }

    #[test]
    fn test_type_info_overwiting_existing_narrows() {
        let x = || Name::new_static("x");
        let y = || Name::new_static("y");
        let z = || Name::new_static("z");
        let mut type_info = TypeInfo::of_ty(fake_class_type("Foo"));
        type_info.add_narrow(
            &Vec1::from_vec_push(vec![x(), y()], z()),
            fake_class_type("Bar"),
        );
        type_info.add_narrow(&Vec1::from_vec_push(vec![x()], y()), fake_class_type("Qux"));
        assert_eq!(type_info.to_string(), "Foo (_.x.y: Qux, _.x.y.z: Bar)");
        type_info.add_narrow(
            &Vec1::from_vec_push(vec![x()], y()),
            fake_class_type("Qux1"),
        );
        assert_eq!(type_info.to_string(), "Foo (_.x.y: Qux1, _.x.y.z: Bar)");
        type_info.add_narrow(
            &Vec1::from_vec_push(vec![x(), y()], z()),
            fake_class_type("Bar1"),
        );
        assert_eq!(type_info.to_string(), "Foo (_.x.y: Qux1, _.x.y.z: Bar1)");
    }

    #[test]
    fn test_type_info_empty_join() {
        let type_info = TypeInfo::join(Vec::new(), &|ts| {
            if ts.is_empty() {
                fake_class_type("Never")
            } else {
                fake_class_type("FakeUnionType")
            }
        });
        assert_eq!(type_info.to_string(), "Never");
    }
}
