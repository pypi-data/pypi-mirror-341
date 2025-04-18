# ~/injects/src/injects/patterns/operators.py
"""
Pattern matchers for operator-related AST nodes.
"""
from __future__ import annotations
import ast, typing as t

from injects.patterns.base import Pattern, NodeTypePattern

class BinaryOperationPattern(Pattern):
    """Pattern to match binary operations"""
    def __init__(self, optype: t.Optional[t.Type[ast.operator]] = None):
        self.optype = optype

    def matches(self, node: ast.AST) -> bool:
        if not isinstance(node, ast.BinOp):
            return False

        if self.optype:
            return isinstance(node.op, self.optype)

        return True


class ComparisonPattern(Pattern):
    """Pattern to match comparison operations"""
    def __init__(self, optype: t.Optional[t.Type[ast.cmpop]] = None):
        self.optype = optype

    def matches(self, node: ast.AST) -> bool:
        if not isinstance(node, ast.Compare):
            return False

        if self.optype:
            return any(isinstance(op, self.optype) for op in node.ops)

        return True


class UnaryOperationPattern(Pattern):
    """Pattern to match unary operations"""
    def __init__(self, optype: t.Optional[t.Type[ast.unaryop]] = None):
        self.optype = optype

    def matches(self, node: ast.AST) -> bool:
        if not isinstance(node, ast.UnaryOp):
            return False

        if self.optype:
            return isinstance(node.op, self.optype)

        return True


class BooleanOperationPattern(Pattern):
    """Pattern to match boolean operations (and/or)"""
    def __init__(self, optype: t.Optional[t.Type[ast.boolop]] = None):
        self.optype = optype

    def matches(self, node: ast.AST) -> bool:
        if not isinstance(node, ast.BoolOp):
            return False

        if self.optype:
            return isinstance(node.op, self.optype)

        return True
