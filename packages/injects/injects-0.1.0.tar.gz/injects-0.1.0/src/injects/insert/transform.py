# ~/injects/src/injects/insert/transform.py
"""
Transformation helpers for insertion strategies.
"""
from __future__ import annotations
import ast, typing as t

class create:
    class statementof:
        @staticmethod
        def expression(expr: ast.expr) -> ast.Expr:
            """
            Convert an expression into an expression statement.

            Args:
                expr: The expression to convert

            Returns:
                ast.Expr: An expression statement containing the expression
            """
            stmt = ast.Expr(value=expr)
            ast.fix_missing_locations(stmt)
            return stmt

        @staticmethod
        def printing(value: ast.expr) -> ast.Expr:
            """
            Create a print statement (for debugging).

            Args:
                value: The expression to print

            Returns:
                ast.Expr: A print statement expression
            """
            call = create.callof.function('print', [value])
            return create.statementof.expression(call)

        @staticmethod
        def assignment(target: str, value: ast.expr) -> ast.Assign:
            """
            Create an assignment statement.

            Args:
                target: The name of the variable to assign to
                value: The expression to assign

            Returns:
                ast.Assign: An assignment statement
            """
            assign = ast.Assign(
                targets=[ast.Name(id=target, ctx=ast.Store())],
                value=value
            )

            ast.fix_missing_locations(assign)
            return assign

    class callof:
        @staticmethod
        def function(func_name: str, args: t.Optional[t.List[ast.expr]] = None,
                    keywords: t.Optional[t.List[ast.keyword]] = None) -> ast.Call:
            """
            Create a function call expression.

            Args:
                func_name: The name of the function to call
                args: List of positional arguments
                keywords: List of keyword arguments

            Returns:
                ast.Call: A function call expression
            """
            args = args or []
            keywords = keywords or []

            call = ast.Call(
                func=ast.Name(id=func_name, ctx=ast.Load()),
                args=args,
                keywords=keywords
            )

            ast.fix_missing_locations(call)
            return call

        @staticmethod
        def method(obj: str, method: str, args: t.Optional[t.List[ast.expr]] = None,
                  keywords: t.Optional[t.List[ast.keyword]] = None) -> ast.Call:
            """
            Create a method call expression.

            Args:
                obj: The object on which to call the method
                method: The name of the method to call
                args: List of positional arguments
                keywords: List of keyword arguments

            Returns:
                ast.Call: A method call expression
            """
            args = args or []
            keywords = keywords or []

            call = ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id=obj, ctx=ast.Load()),
                    attr=method,
                    ctx=ast.Load()
                ),
                args=args,
                keywords=keywords
            )

            ast.fix_missing_locations(call)
            return call
