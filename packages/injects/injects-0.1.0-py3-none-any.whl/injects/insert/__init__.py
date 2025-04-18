# ~/injects/src/injects/insert/__init__.py
"""
Insertion strategies for the transformation pipeline.
"""
from .base import (
    InsertionStrategy, ReplaceStrategy,
    WrapStrategy, ModifyStrategy
)
from .position import (
    BeforeStrategy, AfterStrategy, AroundStrategy
)
from .transform import create

# convenience
replace = ReplaceStrategy()
before = BeforeStrategy()
after = AfterStrategy()
around = AroundStrategy()
modify = ModifyStrategy()
wrap = WrapStrategy()

# aliases
Replace = ReplaceStrategy
Before = BeforeStrategy
After = AfterStrategy
Around = AroundStrategy
Modify = ModifyStrategy
Wrap = WrapStrategy
