# ~/injects/src/injects/patterns/function.py
"""
Pattern matchers for function-related AST nodes.
"""
from __future__ import annotations
import ast, re, typing as t

from injects.patterns.base import Pattern, RegexPattern, NodeTypePattern

class FunctionDefPattern(Pattern):
    """Pattern to match function definitions"""
    def __init__(self, namepattern: t.Optional[str] = None):
        self.nameregex = re.compile(namepattern) if namepattern else None

    def matches(self, node: ast.AST) -> bool:
        if not isinstance(node, ast.FunctionDef):
            return False

        if self.nameregex:
            return bool(self.nameregex.match(node.name))
        return True


class FunctionCallPattern(Pattern):
    """Pattern to match function calls"""
    def __init__(self, namepattern: t.Optional[str] = None):
        self.nameregex = re.compile(namepattern) if namepattern else None

    def matches(self, node: ast.AST) -> bool:
        if not isinstance(node, ast.Call):
            return False

        if self.nameregex and isinstance(node.func, ast.Name):
            return bool(self.nameregex.match(node.func.id))
        elif self.nameregex and isinstance(node.func, ast.Attribute):
            return bool(self.nameregex.match(node.func.attr))

        return self.nameregex is None


class MethodCallPattern(Pattern):
    """Pattern to match method calls on objects"""
    def __init__(self,
                 methodpattern: t.Optional[str] = None,
                 objectpattern: t.Optional[str] = None):
        self.methodregex = re.compile(methodpattern) if methodpattern else None
        self.objectregex = re.compile(objectpattern) if objectpattern else None

    def matches(self, node: ast.AST) -> bool:
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            return False

        matchesmethod = True
        if self.methodregex:
            matchesmethod = bool(self.methodregex.match(node.func.attr))

        matchesobject = True
        if self.objectregex and isinstance(node.func.value, ast.Name):
            matchesobject = bool(self.objectregex.match(node.func.value.id))

        return matchesmethod and matchesobject


class ReturnPattern(Pattern):
    """Pattern to match return statements"""
    def __init__(self, hasvalue: t.Optional[bool] = None):
        self.hasvalue = hasvalue

    def matches(self, node: ast.AST) -> bool:
        if not isinstance(node, ast.Return):
            return False

        if self.hasvalue is not None:
            hasvalue = node.value is not None
            return hasvalue == self.hasvalue

        return True
