# ~/injects/src/injects/__init__.py
"""
injects - Runtime dynamic code injection and manipulation via decorators

Core functionality for building code transformation decorators.
"""
from __future__ import annotations
import ast, inspect, typing as t, functools, sys

# Import core components
from injects.core.transformer import CodeTransformer
from injects.logs import log

# Re-export submodules for convenient access
from injects import patterns
from injects import conditionals
from injects import insert
from injects import transforms
from injects import utils

__version__ = "0.1.0"

def build(
    transformer: t.Callable,
    pattern: t.Optional[t.Any] = None,
    condition: t.Optional[t.Any] = None,
    position: t.Optional[t.Any] = None,
    options: t.Optional[t.Dict[str, t.Any]] = None
) -> t.Callable[[t.Callable], t.Callable]:
    """
    Create a decorator that transforms functions based on the given parameters.

    Args:
        transformer: The transformation function to apply
        pattern: Pattern to match in code
        condition: When to apply transformation
        position: Where to insert transformed code
        options: Additional configuration options

    Returns:
        A decorator function that transforms the decorated function
    """
    options = options or {}

    def decorator(func: t.Callable) -> t.Callable:
        # Skip transformation if not enabled
        if options.get('disabled', False):
            return func

        # Get the source code
        try:
            source = inspect.getsource(func)
        except Exception as e:
            log.error(f"Could not get source for {func.__name__}: {e}")
            return func

        # Parse the source into an AST
        try:
            tree = ast.parse(source)
        except SyntaxError as e:
            log.error(f"Could not parse source for {func.__name__}: {e}")
            return func

        # Create and apply the transformer
        transformer_instance = CodeTransformer(
            transfunc=transformer,
            transargs=options.get('args', ()),
            transkwargs=options.get('kwargs', {}),
            pattern=pattern,
            conditions=condition,
            positions=position
        )

        # Transform the AST
        try:
            transformedtree = transformer_instance.visit(tree)
            ast.fix_missing_locations(transformedtree)
        except Exception as e:
            log.error(f"Error transforming {func.__name__}: {e}")
            return func

        # Execute the transformed code
        try:
            # Create a new namespace for execution
            namespace = {}

            # Include the original function's globals
            namespace.update(func.__globals__)

            # Execute the transformed code in the namespace
            exec(compile(transformedtree, filename=func.__code__.co_filename, mode='exec'), namespace)

            # Get the transformed function from the namespace
            transformedfunc = namespace[func.__name__]

            # Copy metadata from the original function
            functools.update_wrapper(transformedfunc, func)

            return transformedfunc
        except Exception as e:
            log.error(f"Error executing transformed {func.__name__}: {e}")
            return func

    return decorator

def injector(
    pattern: t.Optional[t.Any] = None,
    condition: t.Optional[t.Any] = None,
    position: t.Optional[t.Any] = None,
    options: t.Optional[t.Dict[str, t.Any]] = None
) -> t.Callable[[t.Callable], t.Callable]:
    """
    Decorator that converts a function into a transformer.

    Args:
        pattern: Pattern to match in code
        condition: When to apply transformation
        position: Where to insert transformed code
        options: Additional configuration options

    Returns:
        A decorator factory that creates transformation decorators
    """
    options = options or {}

    def decorator(transformerfunc: t.Callable) -> t.Callable:
        # Create a build decorator with the transformer function
        return build(
            transformer=transformerfunc,
            pattern=pattern,
            condition=condition,
            position=position,
            options=options
        )

    return decorator
