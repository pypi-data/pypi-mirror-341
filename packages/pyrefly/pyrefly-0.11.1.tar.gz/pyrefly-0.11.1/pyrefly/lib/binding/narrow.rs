/*
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

use ruff_python_ast::Arguments;
use ruff_python_ast::BoolOp;
use ruff_python_ast::CmpOp;
use ruff_python_ast::Expr;
use ruff_python_ast::ExprAttribute;
use ruff_python_ast::ExprBoolOp;
use ruff_python_ast::ExprCall;
use ruff_python_ast::ExprCompare;
use ruff_python_ast::ExprNamed;
use ruff_python_ast::ExprUnaryOp;
use ruff_python_ast::UnaryOp;
use ruff_python_ast::name::Name;
use ruff_text_size::Ranged;
use ruff_text_size::TextRange;
use starlark_map::small_map::SmallMap;
use starlark_map::smallmap;
use vec1::Vec1;

use crate::assert_words;
use crate::types::types::Type;
use crate::util::prelude::SliceExt;

assert_words!(AtomicNarrowOp, 10);
assert_words!(NarrowOp, 11);

#[derive(Clone, Debug)]
pub enum AtomicNarrowOp {
    Is(Expr),
    IsNot(Expr),
    Truthy,
    Falsy,
    Eq(Expr),
    NotEq(Expr),
    IsInstance(Expr),
    IsNotInstance(Expr),
    IsSubclass(Expr),
    IsNotSubclass(Expr),
    TypeGuard(Type, Arguments),
    NotTypeGuard(Type, Arguments),
    TypeIs(Type, Arguments),
    NotTypeIs(Type, Arguments),
    /// (func, args) for a function call that may narrow the type of its first argument.
    Call(Box<Expr>, Arguments),
    NotCall(Box<Expr>, Arguments),
}

#[derive(Clone, Debug)]
pub struct NarrowedAttribute(pub Box<Vec1<Name>>);

impl NarrowedAttribute {
    pub fn new(chain: Vec1<Name>) -> Self {
        Self(Box::new(chain))
    }

    pub fn names(&self) -> &Vec1<Name> {
        match self {
            Self(box chain) => chain,
        }
    }
}

#[derive(Clone, Debug)]
pub enum NarrowOp {
    Atomic(Option<NarrowedAttribute>, AtomicNarrowOp),
    And(Vec<NarrowOp>),
    Or(Vec<NarrowOp>),
}

impl AtomicNarrowOp {
    pub fn negate(&self) -> Self {
        match self {
            Self::Is(v) => Self::IsNot(v.clone()),
            Self::IsNot(v) => Self::Is(v.clone()),
            Self::IsInstance(v) => Self::IsNotInstance(v.clone()),
            Self::IsNotInstance(v) => Self::IsInstance(v.clone()),
            Self::IsSubclass(v) => Self::IsNotSubclass(v.clone()),
            Self::IsNotSubclass(v) => Self::IsSubclass(v.clone()),
            Self::Eq(v) => Self::NotEq(v.clone()),
            Self::NotEq(v) => Self::Eq(v.clone()),
            Self::Truthy => Self::Falsy,
            Self::Falsy => Self::Truthy,
            Self::TypeGuard(ty, args) => Self::NotTypeGuard(ty.clone(), args.clone()),
            Self::NotTypeGuard(ty, args) => Self::TypeGuard(ty.clone(), args.clone()),
            Self::TypeIs(ty, args) => Self::NotTypeIs(ty.clone(), args.clone()),
            Self::NotTypeIs(ty, args) => Self::TypeIs(ty.clone(), args.clone()),
            Self::Call(f, args) => Self::NotCall(f.clone(), args.clone()),
            Self::NotCall(f, args) => Self::Call(f.clone(), args.clone()),
        }
    }
}

#[derive(Clone, Debug)]
enum NarrowingSubject {
    Name(Name),
    Attribute(Name, NarrowedAttribute),
}

impl NarrowOp {
    pub fn negate(&self) -> Self {
        match self {
            Self::Atomic(attr, op) => Self::Atomic(attr.clone(), op.negate()),
            Self::And(ops) => Self::Or(ops.map(|op| op.negate())),
            Self::Or(ops) => Self::And(ops.map(|op| op.negate())),
        }
    }

    fn and(&mut self, other: Self) {
        match self {
            Self::And(ops) => ops.push(other),
            _ => *self = Self::And(vec![self.clone(), other]),
        }
    }

    fn or(&mut self, other: Self) {
        match self {
            Self::Or(ops) => ops.push(other),
            _ => *self = Self::Or(vec![self.clone(), other]),
        }
    }
}

#[derive(Clone, Debug, Default)]
pub struct NarrowOps(pub SmallMap<Name, (NarrowOp, TextRange)>);

impl NarrowOps {
    pub fn new() -> Self {
        Self(SmallMap::new())
    }

    pub fn is(name: &Name, v: Expr, range: TextRange) -> Self {
        Self(smallmap! { name.clone() => (NarrowOp::Atomic(None, AtomicNarrowOp::Is(v)), range) })
    }

    pub fn eq(name: &Name, v: Expr, range: TextRange) -> Self {
        Self(smallmap! { name.clone() => (NarrowOp::Atomic(None, AtomicNarrowOp::Eq(v)), range) })
    }

    pub fn isinstance(name: &Name, v: Expr, range: TextRange) -> Self {
        Self(
            smallmap! { name.clone() => (NarrowOp::Atomic(None, AtomicNarrowOp::IsInstance(v)), range) },
        )
    }

    pub fn negate(&self) -> Self {
        if self.0.len() == 1 {
            let (name, (op, range)) = self.0.first().unwrap();
            Self(smallmap! {
                name.clone() => (op.negate(), *range)
            })
        } else {
            // We don't have a way to model an `or` condition involving multiple variables (e.g., `x is None or not y`).
            Self::new()
        }
    }

    fn and(&mut self, name: Name, op: NarrowOp, range: TextRange) {
        if let Some((existing_op, _)) = self.0.get_mut(&name) {
            existing_op.and(op)
        } else {
            self.0.insert(name, (op, range));
        }
    }

    fn and_atomic(&mut self, subject: NarrowingSubject, op: AtomicNarrowOp, range: TextRange) {
        let (name, attr) = match subject {
            NarrowingSubject::Name(name) => (name, None),
            NarrowingSubject::Attribute(name, attr) => (name, Some(attr)),
        };
        self.and(name, NarrowOp::Atomic(attr, op), range);
    }

    pub fn and_all(&mut self, other: Self) {
        for (name, (op, range)) in other.0 {
            self.and(name, op, range);
        }
    }

    pub fn or_all(&mut self, other: Self) {
        // We can only model an `or` condition involving a single variable.
        if self.0.len() != 1 || other.0.len() != 1 {
            *self = Self::new();
            return;
        }
        let (self_name, (self_op, _)) = self.0.iter_mut().next().unwrap();
        let (other_name, (other_op, _)) = other.0.into_iter_hashed().next().unwrap();
        if *self_name != *other_name {
            *self = Self::new();
            return;
        }
        self_op.or(other_op);
    }

    pub fn from_single_narrow_op(left: &Expr, op: AtomicNarrowOp, range: TextRange) -> Self {
        let mut narrow_ops = Self::new();
        for subject in expr_to_subjects(left) {
            narrow_ops.and_atomic(subject, op.clone(), range);
        }
        narrow_ops
    }

    pub fn from_expr(test: Option<&Expr>) -> Self {
        match test {
            Some(Expr::Compare(ExprCompare {
                range: _,
                left,
                ops: cmp_ops,
                comparators,
            })) => {
                let mut narrow_ops = Self::new();
                let subjects = expr_to_subjects(left);
                let ops = cmp_ops
                    .iter()
                    .zip(comparators)
                    .filter_map(|(cmp_op, right)| {
                        let range = right.range();
                        let op = match cmp_op {
                            CmpOp::Is => AtomicNarrowOp::Is(right.clone()),
                            CmpOp::IsNot => AtomicNarrowOp::IsNot(right.clone()),
                            CmpOp::Eq => AtomicNarrowOp::Eq(right.clone()),
                            CmpOp::NotEq => AtomicNarrowOp::NotEq(right.clone()),
                            _ => {
                                return None;
                            }
                        };
                        Some((op, range))
                    });

                for (op, range) in ops {
                    for subject in subjects.iter() {
                        narrow_ops.and_atomic(subject.clone(), op.clone(), range);
                    }
                }
                narrow_ops
            }
            Some(Expr::BoolOp(ExprBoolOp {
                range: _,
                op: BoolOp::And,
                values,
            })) => {
                let mut narrow_ops = Self::new();
                for e in values {
                    narrow_ops.and_all(Self::from_expr(Some(e)))
                }
                narrow_ops
            }
            Some(Expr::BoolOp(ExprBoolOp {
                range: _,
                op: BoolOp::Or,
                values,
            })) => {
                let mut exprs = values.iter();
                if let Some(first_val) = exprs.next() {
                    let mut narrow_ops = Self::from_expr(Some(first_val));
                    for next_val in exprs {
                        narrow_ops.or_all(Self::from_expr(Some(next_val)));
                    }
                    narrow_ops
                } else {
                    Self::new()
                }
            }
            Some(Expr::UnaryOp(ExprUnaryOp {
                range: _,
                op: UnaryOp::Not,
                operand: box e,
            })) => Self::from_expr(Some(e)).negate(),
            Some(Expr::Call(ExprCall {
                range,
                func,
                arguments:
                    args @ Arguments {
                        range: _,
                        args: posargs,
                        keywords: _,
                    },
            })) if !posargs.is_empty() => {
                // This may be a function call that narrows the type of its first argument. Record
                // it as a possible narrowing operation that we'll resolve in the answers phase.
                Self::from_single_narrow_op(
                    &posargs[0],
                    AtomicNarrowOp::Call(Box::new((**func).clone()), args.clone()),
                    *range,
                )
            }
            Some(e) => Self::from_single_narrow_op(e, AtomicNarrowOp::Truthy, e.range()),
            None => Self::new(),
        }
    }
}

fn subject_for_attribute(
    expr: &ExprAttribute,
    mut rev_attr_chain: Vec<Name>,
) -> Option<NarrowingSubject> {
    match &*expr.value {
        Expr::Name(name) => {
            let mut final_chain = Vec1::from_vec_push(rev_attr_chain, expr.attr.id.clone());
            final_chain.reverse();
            Some(NarrowingSubject::Attribute(
                name.id.clone(),
                NarrowedAttribute::new(final_chain),
            ))
        }
        Expr::Attribute(x) => {
            rev_attr_chain.push(expr.attr.id.clone());
            subject_for_attribute(x, rev_attr_chain)
        }
        _ => None,
    }
}

fn expr_to_subjects(expr: &Expr) -> Vec<NarrowingSubject> {
    fn f(expr: &Expr, res: &mut Vec<NarrowingSubject>) {
        match expr {
            Expr::Name(name) => res.push(NarrowingSubject::Name(name.id.clone())),
            Expr::Attribute(x) => res.extend(subject_for_attribute(x, Vec::new())),
            Expr::Named(ExprNamed { target, value, .. }) => {
                f(target, res);
                f(value, res);
            }
            _ => {}
        }
    }

    let mut res = Vec::new();
    f(expr, &mut res);
    res
}
