# ~/injects/src/injects/conditionals/base.py
"""
Base classes for condition checking in the transformation pipeline.
"""
from __future__ import annotations
import ast, typing as t

class Condition:
    """Base class for all conditions"""
    def check(self, node: ast.AST) -> bool:
        """
        Check if the condition is satisfied for the given node.

        Args:
            node: The AST node to check the condition against

        Returns:
            bool: True if the condition is satisfied, False otherwise
        """
        raise NotImplementedError("Condition classes must implement check()")

    def __and__(self, other: Condition) -> AndCondition:
        """Combine with another condition using AND logic"""
        return AndCondition(self, other)

    def __or__(self, other: Condition) -> OrCondition:
        """Combine with another condition using OR logic"""
        return OrCondition(self, other)

    def __invert__(self) -> NotCondition:
        """Negate this condition"""
        return NotCondition(self)


class AndCondition(Condition):
    """Logical AND combination of multiple conditions"""
    def __init__(self, *conditions: Condition) -> None:
        self.conditions = conditions

    def check(self, node: ast.AST) -> bool:
        return all(condition.check(node) for condition in self.conditions)


class OrCondition(Condition):
    """Logical OR combination of multiple conditions"""
    def __init__(self, *conditions: Condition) -> None:
        self.conditions = conditions

    def check(self, node: ast.AST) -> bool:
        return any(condition.check(node) for condition in self.conditions)


class NotCondition(Condition):
    """Negation of a condition"""
    def __init__(self, condition: Condition) -> None:
        self.condition = condition

    def check(self, node: ast.AST) -> bool:
        return not self.condition.check(node)


class AlwaysCondition(Condition):
    """Condition that is always satisfied"""
    def check(self, node: ast.AST) -> bool:
        return True


class NeverCondition(Condition):
    """Condition that is never satisfied"""
    def check(self, node: ast.AST) -> bool:
        return False


class PatternCondition(Condition):
    """Condition that is satisfied when a pattern matches"""
    def __init__(self, pattern: t.Any) -> None:
        self.pattern = pattern

    def check(self, node: ast.AST) -> bool:
        if hasattr(self.pattern, 'matches'):
            return self.pattern.matches(node)
        return False


class FunctionCondition(Condition):
    """Condition that uses a custom function for checking"""
    def __init__(self, func: t.Callable[[ast.AST], bool]) -> None:
        self.func = func

    def check(self, node: ast.AST) -> bool:
        try:
            return bool(self.func(node))
        except Exception:
            return False
