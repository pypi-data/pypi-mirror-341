# ~/injects/src/injects/conditionals/value.py
"""
Value-based conditions for the transformation pipeline.
"""
from __future__ import annotations
import ast, re, typing as t

from injects.conditionals.base import Condition

class AttributeValueCondition(Condition):
    """Condition that checks if a node's attribute has a specific value"""
    def __init__(self, attribute: str, expectedvalue: t.Any) -> None:
        self.attribute = attribute
        self.expectedvalue = expectedvalue

    def check(self, node: ast.AST) -> bool:
        if not hasattr(node, self.attribute):
            return False

        try:
            attrvalue = getattr(node, self.attribute)
            return attrvalue == self.expectedvalue
        except Exception:
            return False


class AttributeRegexCondition(Condition):
    """Condition that checks if a string attribute matches a regex pattern"""
    def __init__(self, attribute: str, pattern: str) -> None:
        self.attribute = attribute
        self.regex = re.compile(pattern)

    def check(self, node: ast.AST) -> bool:
        if not hasattr(node, self.attribute):
            return False

        try:
            attrvalue = getattr(node, self.attribute)
            if isinstance(attrvalue, str):
                return bool(self.regex.match(attrvalue))
            return False
        except Exception:
            return False


class ConstantValueCondition(Condition):
    """Condition that checks if a Constant node has a specific value"""
    def __init__(self, expectedvalue: t.Any) -> None:
        self.expectedvalue = expectedvalue

    def check(self, node: ast.AST) -> bool:
        if not isinstance(node, ast.Constant):
            return False

        return node.value == self.expectedvalue


class FunctionNameCondition(Condition):
    """Condition that checks if a function name matches a specific pattern"""
    def __init__(self, namepattern: str) -> None:
        self.regex = re.compile(namepattern)

    def check(self, node: ast.AST) -> bool:
        if isinstance(node, ast.FunctionDef):
            return bool(self.regex.match(node.name))
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            return bool(self.regex.match(node.func.id))
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            return bool(self.regex.match(node.func.attr))

        return False
