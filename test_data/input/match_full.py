"""Test file for full match/case decompilation"""
def test_match(x):
    match x:
        case 1:
            return "one"
        case 2:
            return "two"
        case _:
            return "other"

def test_match_with_guard(x):
    match x:
        case str() as s if len(s) > 5:
            return "long string"
        case str():
            return "short string"
        case int():
            return "integer"
        case _:
            return "unknown"
