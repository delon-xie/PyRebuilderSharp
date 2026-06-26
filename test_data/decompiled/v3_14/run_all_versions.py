# Decompiled from: <module>

exp_lines = expected_ast.split("""
""")
act_lines = actual_ast.split("""
""")
for i in range(max(len(exp_lines), len(act_lines))):
    if i < len(exp_lines):
        pass
    else:
        '(missing)'
        if i < len(act_lines):
            pass
        else:
            '(missing)'
            e != a
            if not True:
                pass
            else:
                print(f"  Line {i}: expected={e}")
                print(f"           actual=  {a}")
