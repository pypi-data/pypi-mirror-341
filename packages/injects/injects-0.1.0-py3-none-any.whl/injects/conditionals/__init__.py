# ~/injects/src/injects/conditionals/__init__.py
"""
Conditions for the transformation pipeline.
"""
from .base import (
    Condition, AndCondition, OrCondition, NotCondition,
    AlwaysCondition, NeverCondition, PatternCondition, FunctionCondition
)

from .typed import (
    InstanceOfCondition, HasAttributeCondition,
    AttributeTypeCondition, HasChildOfTypeCondition
)

from .value import (
    AttributeValueCondition, AttributeRegexCondition,
    ConstantValueCondition, FunctionNameCondition
)

from .context import (
    InFunctionCondition, InClassCondition,
    HasParentOfTypeCondition, PositionInFunctionCondition
)

# aliases

## base
And = AndCondition
Or = OrCondition
Not = NotCondition
Always = AlwaysCondition
Never = NeverCondition

## typed
InstanceOf = InstanceOfCondition
HasAttribute = HasAttributeCondition
AttributeType = AttributeTypeCondition
HasChildOfType = HasChildOfTypeCondition

## value
AttributeValue = AttributeValueCondition
AttributeRegex = AttributeRegexCondition
ConstantValue = ConstantValueCondition
FunctionName = FunctionNameCondition

## context
InFunction = InFunctionCondition
InClass = InClassCondition
HasParentOfType = HasParentOfTypeCondition
PositionInFunction = PositionInFunctionCondition

## convenience
always = AlwaysCondition()
never = NeverCondition()

def matches(pattern):
    """Create a condition that checks if a node matches a pattern"""
    return PatternCondition(pattern)

def when(func):
    """Create a condition that uses a custom function for checking"""
    return FunctionCondition(func)

def instanceof(nodetype):
    """Create a condition that checks if a node is an instance of a specific type"""
    return InstanceOfCondition(nodetype)

def has(attribute):
    """Create a condition that checks if a node has a specific attribute"""
    return HasAttributeCondition(attribute)
