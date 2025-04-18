# ~/injects/src/injects/insert/base.py
"""
Base classes for insertion strategies in the transformation pipeline.
"""
from __future__ import annotations
import ast, typing as t, copy as cp

from injects.logs import log

class InsertionStrategy:
    """Base class for all insertion strategies"""
    def apply(self, node: ast.AST, transfunc: t.Callable,
              transargs: t.Tuple = (), transkwargs: t.Dict = {}) -> ast.AST:
        """
        Apply the transformation to the given node based on the insertion strategy.

        Args:
            node: The AST node to transform
            transfunc: The transformation function to apply
            transargs: Arguments to pass to the transformation function
            transkwargs: Keyword arguments to pass to the transformation function

        Returns:
            ast.AST: The transformed node
        """
        raise NotImplementedError("Insertion strategies must implement apply()")


class ReplaceStrategy(InsertionStrategy):
    """Strategy that replaces the node with the transformation result"""
    def apply(self, node: ast.AST, transfunc: t.Callable,
              transargs: t.Tuple = (), transkwargs: t.Dict = {}) -> ast.AST:
        try:
            result = transfunc(node, *transargs, **transkwargs)
            if result is not None:
                # Ensure the result is a valid AST node
                if isinstance(result, ast.AST):
                    ast.fix_missing_locations(result)
                    return result
                else:
                    log.error(f"Transformation result is not an AST node: {type(result)}")

            return node
        except Exception as e:
            log.error(f"Error applying replacement transformation: {str(e)}")
            return node


class WrapStrategy(InsertionStrategy):
    """Strategy that wraps the node with code before and after"""
    def __init__(self, before: bool = True, after: bool = True):
        self.before = before
        self.after = after

    def apply(self, node: ast.AST, transfunc: t.Callable,
              transargs: t.Tuple = (), transkwargs: t.Dict = {}) -> ast.AST:
        try:
            # This is a placeholder implementation that would need to be
            # customized based on the specific node type
            if isinstance(node, ast.stmt):
                return self._wrapstatement(node, transfunc, transargs, transkwargs)
            elif isinstance(node, ast.expr):
                return self._wrapexpression(node, transfunc, transargs, transkwargs)
            else:
                return node
        except Exception as e:
            log.error(f"Error applying wrap transformation: {str(e)}")
            return node

    def _wrapstatement(self, node: ast.stmt, transfunc: t.Callable,
                       transargs: t.Tuple, transkwargs: t.Dict) -> ast.AST:
        # Placeholder for statement wrapping logic
        return node

    def _wrapexpression(self, node: ast.expr, transfunc: t.Callable,
                        transargs: t.Tuple, transkwargs: t.Dict) -> ast.AST:
        # Placeholder for expression wrapping logic
        return node


class ModifyStrategy(InsertionStrategy):
    """Strategy that modifies the node in place"""
    def apply(self, node: ast.AST, transfunc: t.Callable,
              transargs: t.Tuple = (), transkwargs: t.Dict = {}) -> ast.AST:
        try:
            # Create a copy of the node to avoid modifying the original
            nodecopy = cp.deepcopy(node)

            # Apply the transformation function with the node copy
            result = transfunc(nodecopy, *transargs, **transkwargs)

            # If the transformation returns None, assume it modified the node in-place
            if result is None:
                return nodecopy

            # Otherwise, return the result if it's a valid AST node
            if isinstance(result, ast.AST):
                ast.fix_missing_locations(result)
                return result

            # Default fallback
            return node
        except Exception as e:
            log.error(f"Error applying modification transformation: {str(e)}")
            return node
