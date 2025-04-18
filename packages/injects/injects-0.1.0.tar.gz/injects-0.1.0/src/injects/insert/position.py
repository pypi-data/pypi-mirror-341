# ~/injects/src/injects/insert/position.py
"""
Position-based insertion strategies for the transformation pipeline.
"""
from __future__ import annotations
import ast, typing as t

from injects.logs import log
from injects.insert.base import InsertionStrategy

class BeforeStrategy(InsertionStrategy):
    """Strategy that inserts code before the matched node"""

    def apply(self, node: ast.AST, transfunc: t.Callable,
              transargs: t.Tuple = (), transkwargs: t.Dict[str, t.Any] = {}) -> t.Union[ast.AST, t.List[ast.stmt]]:
        try:
            if isinstance(node, ast.stmt):
                return self._insertbefore(node, transfunc, transargs, transkwargs)

            log.warning(f"BeforeStrategy only supports statement nodes, not {type(node).__name__}")
            return node
        except Exception as e:
            log.error(f"Error applying before insertion: {str(e)}")
            return node

    def _insertbefore(self, node: ast.stmt, transfunc: t.Callable,
                      transargs: t.Tuple, transkwargs: t.Dict[str, t.Any]) -> t.Union[ast.AST, t.List[ast.stmt]]:
        # Generate the statement(s) to insert before the node
        beforestmts = transfunc(node, *transargs, **transkwargs)

        # If transformation returned None or the original node, just return the node
        if beforestmts is None or beforestmts is node:
            return node

        # If transformation returned a list of statements
        if isinstance(beforestmts, list):
            # Ensure all elements are statements
            if not all(isinstance(stmt, ast.stmt) for stmt in beforestmts):
                log.error("Before transformation must return a list of statement nodes")
                return node

            # Create a new list with before statements followed by the original node
            result = beforestmts + [node]

            # If there's only one statement in the result, return it directly
            if len(result) == 1:
                return result[0]

            # Otherwise, return the list of statements
            return result

        # If transformation returned a single statement, return it and the original node
        if isinstance(beforestmts, ast.stmt):
            return [beforestmts, node]

        log.error(f"Before transformation must return statements, got {type(beforestmts).__name__}")
        return node


class AfterStrategy(InsertionStrategy):
    """Strategy that inserts code after the matched node"""
    def apply(self, node: ast.AST, transfunc: t.Callable,
              transargs: t.Tuple = (), transkwargs: t.Dict[str, t.Any] = {}) -> t.Union[ast.AST, t.List[ast.stmt]]:
        try:
            if isinstance(node, ast.stmt):
                return self._insertafter(node, transfunc, transargs, transkwargs)

            log.warning(f"AfterStrategy only supports statement nodes, not {type(node).__name__}")
            return node
        except Exception as e:
            log.error(f"Error applying after insertion: {str(e)}")
            return node

    def _insertafter(self, node: ast.stmt, transfunc: t.Callable,
                     transargs: t.Tuple, transkwargs: t.Dict[str, t.Any]) -> t.Union[ast.AST, t.List[ast.stmt]]:
        # Generate the statement(s) to insert after the node
        afterstmts = transfunc(node, *transargs, **transkwargs)

        # If transformation returned None or the original node, just return the node
        if afterstmts is None or afterstmts is node:
            return node

        # If transformation returned a list of statements
        if isinstance(afterstmts, list):
            # Ensure all elements are statements
            if not all(isinstance(stmt, ast.stmt) for stmt in afterstmts):
                log.error("After transformation must return a list of statement nodes")
                return node

            # Create a new list with the original node followed by after statements
            result = [node] + afterstmts

            # If there's only one statement in the result, return it directly
            if len(result) == 1:
                return result[0]

            # Otherwise, return the list of statements
            return result

        # If transformation returned a single statement, return the original node and it
        if isinstance(afterstmts, ast.stmt):
            return [node, afterstmts]

        log.error(f"After transformation must return statements, got {type(afterstmts).__name__}")
        return node


class AroundStrategy(InsertionStrategy):
    """Strategy that inserts code before and after the matched node"""
    def apply(self, node: ast.AST, transfunc: t.Callable,
              transargs: t.Tuple = (), transkwargs: t.Dict[str, t.Any] = {}) -> t.Union[ast.AST, t.List[ast.stmt]]:
        try:
            if isinstance(node, ast.stmt):
                return self._insertaround(node, transfunc, transargs, transkwargs)

            log.warning(f"AroundStrategy only supports statement nodes, not {type(node).__name__}")
            return node
        except Exception as e:
            log.error(f"Error applying around insertion: {str(e)}")
            return node

    def _insertaround(self, node: ast.stmt, transfunc: t.Callable,
                      transargs: t.Tuple, transkwargs: t.Dict[str, t.Any]) -> t.Union[ast.AST, t.List[ast.stmt]]:
        # Generate the before and after statements
        result = transfunc(node, *transargs, **transkwargs)

        # If transformation returned None or the original node, just return the node
        if result is None or result is node:
            return node

        # If transformation returned a tuple of (beforestmts, afterstmts)
        if isinstance(result, tuple) and len(result) == 2:
            beforestmts, afterstmts = result

            # Convert to lists if single statements
            if isinstance(beforestmts, ast.stmt):
                beforestmts = [beforestmts]
            if isinstance(afterstmts, ast.stmt):
                afterstmts = [afterstmts]

            # Validate before statements
            if not (beforestmts is None or (isinstance(beforestmts, list) and
                                           all(isinstance(stmt, ast.stmt) for stmt in beforestmts))):
                log.error("Before statements must be a list of statement nodes or None")
                return node

            # Validate after statements
            if not (afterstmts is None or (isinstance(afterstmts, list) and
                                          all(isinstance(stmt, ast.stmt) for stmt in afterstmts))):
                log.error("After statements must be a list of statement nodes or None")
                return node

            # Create the combined result
            combined = []
            if beforestmts:
                combined.extend(beforestmts)
            combined.append(node)
            if afterstmts:
                combined.extend(afterstmts)

            # If there's only one statement in the result, return it directly
            if len(combined) == 1:
                return combined[0]

            # Otherwise, return the list of statements
            return combined

        log.error("Around transformation must return a tuple of (beforestmts, afterstmts)")
        return node
