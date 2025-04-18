# ~/injects/src/injects/patterns/base.py
"""
Base pattern matching classes for AST node identification.
"""
from __future__ import annotations
import re, ast, typing as t

class hints:
    nodetype = t.Union[t.Type[ast.AST], t.Tuple[t.Type[ast.AST], ...]]

class Pattern:
    """Base class for all pattern matchers"""
    def matches(self, node: ast.AST) -> bool:
        """
        Check if the given AST node matches this pattern.

        Args:
            node: The AST node to check against the pattern

        Returns:
            bool: True if the node matches, False otherwise
        """
        raise NotImplementedError("Pattern classes must implement matches()")

    def __and__(self, other: Pattern) -> AndPattern:
        """Combine with another pattern using AND logic"""
        return AndPattern(self, other)

    def __or__(self, other: Pattern) -> OrPattern:
        """Combine with another pattern using OR logic"""
        return OrPattern(self, other)

    def __invert__(self) -> NotPattern:
        """Negate this pattern"""
        return NotPattern(self)

class AndPattern(Pattern):
    def __init__(self, *patterns: Pattern) -> None:
        self.patterns = patterns

    def matches(self, node: ast.AST) -> bool:
        return all(pattern.matches(node) for pattern in self.patterns)

class OrPattern(Pattern):
    def __init__(self, *patterns: Pattern) -> None:
        self.patterns = patterns

    def matches(self, node: ast.AST) -> bool:
        return any(pattern.matches(node) for pattern in self.patterns)

class NotPattern(Pattern):
    def __init__(self, pattern: Pattern) -> None:
        self.pattern = pattern

    def matches(self, node: ast.AST) -> bool:
        return not self.pattern.matches(node)

class NodeTypePattern(Pattern):
    """Pattern that matches nodes of a specific AST type"""
    def __init__(self, nodetype: hints.nodetype) -> None:
        self.nodetype = nodetype

    def matches(self, node: ast.AST) -> bool:
        return isinstance(node, self.nodetype)

class NodeAttributePattern(Pattern):
    """Pattern that checks for specific attribute values on a node"""
    def __init__(self, attribute: str, value: t.Any, nodetype: t.Optional[hints.nodetype] = None) -> None:
        self.attribute = attribute
        self.value = value
        self.nodetype = nodetype

    def matches(self, node: ast.AST) -> bool:
        if self.nodetype and not isinstance(node, self.nodetype):
            return False

        try:
            return hasattr(node, self.attribute) and (getattr(node, self.attribute) == self.value)
        except Exception:
            return False

class RegexPattern(Pattern):
    """Pattern that matches string attributes against a regex pattern"""
    def __init__(self, attribute: str, pattern: str, nodetype: t.Optional[hints.nodetype] = None):
        self.attribute = attribute
        self.regex = re.compile(pattern)
        self.nodetype = nodetype

    def matches(self, node: ast.AST) -> bool:
        if self.nodetype and not isinstance(node, self.nodetype):
            return False
        try:
            attrval = getattr(node, self.attribute, None)
            if isinstance(attrval, str):
                return bool(self.regex.match(attrval))
            return False
        except Exception:
            return False
