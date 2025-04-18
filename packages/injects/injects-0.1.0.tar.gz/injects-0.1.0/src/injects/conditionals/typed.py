# ~/injects/src/injects/conditionals/typed.py
"""
Type-based conditions for the transformation pipeline.
"""
from __future__ import annotations
import ast, typing as t

from injects.conditionals.base import Condition

class InstanceOfCondition(Condition):
    """Condition that checks if a node is an instance of a specific type"""
    def __init__(self, nodetype: t.Union[t.Type[ast.AST], t.Tuple[t.Type[ast.AST], ...]]) -> None:
        self.nodetype = nodetype

    def check(self, node: ast.AST) -> bool:
        return isinstance(node, self.nodetype)


class HasAttributeCondition(Condition):
    """Condition that checks if a node has a specific attribute"""
    def __init__(self, attribute: str) -> None:
        self.attribute = attribute

    def check(self, node: ast.AST) -> bool:
        return hasattr(node, self.attribute)


class AttributeTypeCondition(Condition):
    """Condition that checks if a node's attribute is of a specific type"""
    def __init__(self, attribute: str, expectedtype: t.Type) -> None:
        self.attribute = attribute
        self.expectedtype = expectedtype

    def check(self, node: ast.AST) -> bool:
        if not hasattr(node, self.attribute):
            return False

        try:
            attrvalue = getattr(node, self.attribute)
            return isinstance(attrvalue, self.expectedtype)
        except Exception:
            return False


class HasChildOfTypeCondition(Condition):
    """Condition that checks if a node has a child of a specific type"""
    def __init__(self, childtype: t.Union[t.Type[ast.AST], t.Tuple[t.Type[ast.AST], ...]]) -> None:
        self.childtype = childtype

    def check(self, node: ast.AST) -> bool:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, self.childtype):
                return True
        return False
