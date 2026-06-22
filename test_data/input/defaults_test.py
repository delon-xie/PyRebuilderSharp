"""Test default parameter values"""
def has_defaults(a, b=1, c="hello"):
    return a + b

def has_multiple_defaults(x=10, y=20, z=30):
    return x + y + z

def has_none_default(a=None):
    return a is None
