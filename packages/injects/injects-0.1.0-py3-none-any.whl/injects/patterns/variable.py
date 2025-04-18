# ~/injects/src/injects/patterns/variable.py
"""
Pattern matchers for variable-related AST nodes.
"""
from __future__ import annotations
import ast, re, typing as t

from injects.patterns.base import Pattern

class VariableAssignmentPattern(Pattern):
    """Pattern to match variable assignments"""
    def __init__(self, namepattern: t.Optional[str] = None):
        self.nameregex = re.compile(namepattern) if namepattern else None

    def matches(self, node: ast.AST) -> bool:
        if not isinstance(node, ast.Assign):
            return False

        if not self.nameregex:
            return True

        # Check if any target matches the pattern
        for target in node.targets:
            if isinstance(target, ast.Name) and self.nameregex.match(target.id):
                return True

        return False


class VariableAccessPattern(Pattern):
    """Pattern to match variable access/references"""
    def __init__(self, namepattern: t.Optional[str] = None):
        self.nameregex = re.compile(namepattern) if namepattern else None

    def matches(self, node: ast.AST) -> bool:
        if not isinstance(node, ast.Name) or isinstance(node.ctx, ast.Store):
            return False

        if self.nameregex:
            return bool(self.nameregex.match(node.id))

        return True


class AttributeAccessPattern(Pattern):
    """Pattern to match attribute access on objects"""
    def __init__(self,
                 attrpattern: t.Optional[str] = None,
                 objectpattern: t.Optional[str] = None):
        self.attrregex = re.compile(attrpattern) if attrpattern else None
        self.objectregex = re.compile(objectpattern) if objectpattern else None

    def matches(self, node: ast.AST) -> bool:
        if not isinstance(node, ast.Attribute):
            return False

        matchesattr = True
        if self.attrregex:
            matchesattr = bool(self.attrregex.match(node.attr))

        matchesobject = True
        if self.objectregex and isinstance(node.value, ast.Name):
            matchesobject = bool(self.objectregex.match(node.value.id))

        return matchesattr and matchesobject
