# ~/injects/src/injects/core/transformer.py
"""
Transformer module - Core AST transformation functionality
"""
from __future__ import annotations
import ast, inspect, types, typing as t

from injects.logs import log

class hints:
    patterns = t.Optional[t.Union[t.List[t.Any], t.Tuple[t.Any], t.Any]]
    conditions = t.Optional[t.Union[t.List[t.Any], t.Tuple[t.Any], t.Any]]
    positions = t.Optional[t.Union[t.List[t.Any], t.Tuple[t.Any], t.Any]]

class CodeTransformer(ast.NodeTransformer):
    """Base AST transformer for injects"""
    def __init__(self,
        transfunc: t.Callable,
        transargs: t.Optional[t.Union[t.List, t.Tuple]] = None,
        transkwargs: t.Optional[t.Dict] = None,
        pattern: hints.patterns = None,
        conditions: hints.conditions = None,
        positions: hints.positions = None
    ) -> None:
        self.transfunc = transfunc
        self.transargs = (transargs or ())
        self.transkwargs = (transkwargs or {})
        self.patterns = self._tuplefy(pattern)  # Support for multiple patterns
        self.conditions = self._tuplefy(conditions)  # [], (), {}, single -- support
        self.positions = self._tuplefy(positions)  # [], (), {}, single -- support

    def _tuplefy(self, value: t.Any) -> tuple:
        if value is None:
            return ()
        if isinstance(value, tuple):
            return value
        try:
            if isinstance(value, (list, set)):
                return tuple(value)
            return (value, )
        except Exception as e:
            log.error(f"exception converting value ({type(value)}) to tuple: {str(e)}")
            raise

    def visit(self, node: ast.AST) -> t.Any:
        """Override to add pattern matching, condition checking, and position-based transformation"""
        log.debug(f"visiting node: {type(node).__name__}")

        # check if node matches any pattern
        if self.patterns:
            matches_pattern = False
            for pattern in self.patterns:
                if pattern is None:
                    continue
                if hasattr(pattern, 'matches'):
                    if pattern.matches(node):
                        matches_pattern = True
                        break
            if not matches_pattern:
                return self.generic_visit(node)

        # check all conditions satisfied
        if self.conditions:
            for condition in self.conditions:
                if condition is None:
                    continue
                if hasattr(condition, 'check'):
                    if not condition.check(node):
                        return self.generic_visit(node)
                elif callable(condition):
                    try:
                        if not condition(node):
                            return self.generic_visit(node)
                    except Exception as e:
                        log.error(f"exception in condition function ({condition.__name__}): {str(e)}")
                        return self.generic_visit(node)

        # apply transformations based on positions
        if self.positions:
            for position in self.positions:
                if position is None:
                    continue
                if hasattr(position, 'apply'):
                    try:
                        node = position.apply(node, self.transfunc, self.transargs, self.transkwargs)
                    except Exception as e:
                        log.error(f"error applying position transformation: {str(e)}")
            return node

        # default behavior: apply transformation func directly if possible
        try:
            if callable(self.transfunc):
                transformed = self.transfunc(node, *self.transargs, **self.transkwargs)
                if transformed is not None:
                    return transformed
        except Exception as e:
            log.error(f"error in transformation function ({self.transfunc.__name__}): {str(e)}")

        return self.generic_visit(node)
