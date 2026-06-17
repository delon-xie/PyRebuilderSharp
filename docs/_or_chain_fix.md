# OR Chain Fix — Final Analysis

## Problem
3.13+ `return a or b or c` produces `if a or c: return` — `b` is lost.

## Root Cause
Block C (POP_TOP + LOAD_FAST c) leaves `Name('c')` on StackMachine's `_exprStack`, but `HasResults` only checks `_results`. The value is never emitted.

## Solution (user-approved approach)
Don't touch blocks or control flow. Just capture leftover `_exprStack`:

In `BlockDecompiler.cs` line 51-54, AFTER the existing HasResults loop:
```csharp
// Also capture expressions on _exprStack (e.g. OR chain terminal LOAD_FAST c)
while (stackMachine.ExprStackCount > 0)
{
    stmts.Add(new ExprStmt(stackMachine.PopExpr()));
}
```

## What to revert
1. BlockScanner.cs: Remove POP_TOP→RETURN_VALUE merge (lines 353-365)
2. AstBuilder.cs: Remove OR terminal detection (lines 2212-2220 in BuildIfElse)
3. AstBuilder.cs: Remove RebuildChainBools Rule 2 (the Or/Not detection)

## Regression risk
Minimal — only affects blocks with leftover `_exprStack` after all instructions,
which only happens in AND/OR chain terminal blocks (POP_TOP + LOAD_FAST).
