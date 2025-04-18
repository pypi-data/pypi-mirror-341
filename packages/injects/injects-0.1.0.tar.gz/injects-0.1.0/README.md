# injects

*Runtime dynamic code injection and manipulation via decorators*

## Core Concept

`injects` is a metaprogramming framework that enables dynamic code transformation at runtime through a composable decorator system. Unlike traditional decorators that simply wrap functions, `injects` modifies the actual implementation of decorated functions through AST manipulation.

## Core Design Philosophy

- **Minimal Core**: Focus on providing essential transformation capabilities
- **Composable**: Build complex transformations from simple components
- **Extensible**: Easy to extend with custom patterns, conditions, and transformers
- **Explicit**: Clear about what is being transformed and how

## Installation

```bash
pip install injects
```

## Basic Usage

```python
import injects
from injects.patterns.function import FunctionCallPattern
from injects.insert import before

# Define a transformation that logs function calls
def log_call(node):
    """Create a log statement for function calls"""
    import ast

    # Extract function name from call node
    if isinstance(node.func, ast.Name):
        func_name = node.func.id
    elif isinstance(node.func, ast.Attribute):
        func_name = f"{ast.unparse(node.func.value)}.{node.func.attr}"
    else:
        func_name = "unknown"

    # Create a print statement
    return ast.parse(f"print(f'Calling {func_name}')").body[0]

# Apply to a function - logs all database function calls
@injects.build(
    log_call,
    pattern=FunctionCallPattern("db_.*"),
    position=before
)
def get_user(user_id):
    """Get user data from database"""
    user = db_fetch_user(user_id)
    return db_enrich_user(user)

# Result: logs "Calling db_fetch_user" and "Calling db_enrich_user" when executed
```

## Creating Composable Transformers

The real power of `injects` comes from its composability. Create reusable transformers and combine them:

```python
import injects
from injects.patterns.function import FunctionCallPattern, ReturnPattern
from injects.insert import before, after, around
from injects.conditionals import InstanceOf
import ast

# Create reusable transformers

# 1. Log database calls
db_logger = injects.build(
    log_call,  # Reuse the transformer from above
    pattern=FunctionCallPattern("db_.*"),
    position=before
)

# 2. Validate return values aren't None
def validate_return(node):
    """Add validation to ensure return values aren't None"""
    validation = ast.parse("""
if result is None:
    raise ValueError("Function returned None unexpectedly")
""").body
    return validation

return_validator = injects.build(
    validate_return,
    pattern=ReturnPattern(),
    position=before
)

# 3. Time function execution
def add_timing(node):
    """Add timing code around function execution"""
    start_time = ast.parse("import time\nstart_time = time.time()").body
    end_time = ast.parse("""
end_time = time.time()
print(f"Function executed in {end_time - start_time:.4f} seconds")
""").body
    return start_time, end_time  # for 'around' position, return (before, after)

function_timer = injects.build(
    add_timing,
    pattern=InstanceOf(ast.FunctionDef),
    position=around
)

# Apply multiple transformers to a function
@db_logger
@return_validator
@function_timer
def process_user_data(user_id):
    user = db_fetch_user(user_id)
    processed = transform_user_data(user)
    db_save_user(processed)
    return processed
```

## Pattern Shortcuts

Create intuitive pattern matchers with less code:

```python
from injects.patterns.function import FunctionCallPattern
from injects.patterns.variable import VariableAssignmentPattern
import re

# Match specific function calls
db_calls = FunctionCallPattern("db_.*")
api_calls = FunctionCallPattern("api_.*")

# Combine patterns
data_calls = db_calls | api_calls

# Create patterns for variable assignments
temp_vars = VariableAssignmentPattern("temp_.*")
result_vars = VariableAssignmentPattern("result.*")

# Match any call to print or logging functions
log_pattern = FunctionCallPattern("print") | FunctionCallPattern("log.*")
```

## Conditional Transformations

Apply transformations based on specific conditions:

```python
from injects.conditionals import InstanceOf, AttributeValue, HasAttribute
import ast

# Only apply to specific AST node types
name_nodes = InstanceOf(ast.Name)
call_nodes = InstanceOf(ast.Call)

# Check for specific attribute values
db_name = AttributeValue("id", "db", ast.Name)

# Check if an attribute exists
has_value = HasAttribute("value")

# Combine conditions with logical operators
complex_condition = name_nodes & ~db_name | (call_nodes & has_value)

# Apply a transformation with the condition
@injects.build(
    transformer=log_call,
    pattern=FunctionCallPattern(),
    condition=complex_condition,
    position=before
)
def process_data():
    data = db.fetch_all()
    return transform(data)
```

## Creating Custom Injection Points

The insertion system provides full control over how code is injected:

```python
from injects.insert import before, after, replace, around

# Insert logging before function calls
@injects.build(log_call, pattern=FunctionCallPattern(), position=before)

# Add validation after function calls
@injects.build(validate_result, pattern=FunctionCallPattern(), position=after)

# Replace problematic function calls with safe alternatives
@injects.build(make_safe, pattern=FunctionCallPattern("unsafe_.*"), position=replace)

# Add try/except handling around database operations
@injects.build(add_error_handling, pattern=FunctionCallPattern("db_.*"), position=around)
```

## The Injector Pattern

Turn any function into a reusable transformer with the `injector` decorator:

```python
import injects
from injects.patterns.function import FunctionCallPattern
from injects.insert import before

# Create a reusable transformer for logging
@injects.injector(
    pattern=FunctionCallPattern(),
    position=before
)
def debug_log(node):
    """Log function calls with full detail for debugging"""
    import ast
    func_name = ast.unparse(node.func)
    args_repr = ", ".join(ast.unparse(arg) for arg in node.args)

    return ast.parse(f"print(f'DEBUG: Calling {func_name}({args_repr})')").body[0]

# Now use debug_log as a decorator
@debug_log
def important_function():
    result = calculate_value()
    return process_result(result)
```

## Core Components

The library is built around four key components:

- **Transformer Functions**: Define what transformation to apply
- **Pattern Matchers**: Specify where to apply transformations
- **Condition Checkers**: Control when transformations are applied
- **Position Specifiers**: Determine how transformations are injected

## Extension System

The core functionality can be extended with specialized modules:

- **injects.patterns**: Common code patterns to match
- **injects.conditionals**: Predefined conditions for transformations
- **injects.transforms**: Ready-to-use transformation functions
- **injects.insert**: Insertion logic components
- **injects.utils**: Helper utilities for common tasks

## Project Status

`injects` is currently in early development (v0.1.0). The core functionality is implemented, with more features planned in future releases.
