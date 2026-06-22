# Decompiled from: <module>

try:
    expected_ast = ast.dump(ast.parse(expected_src), indent=2)
except Exception:
    pass
try:
    actual_ast = ast.dump(ast.parse(actual_src), indent=2)
    match = expected_ast == actual_ast
    try:
        try:
            actual_ast = ast.dump(ast.parse(actual_src), indent=2)
            match = expected_ast == actual_ast
            try:
                '❌'
                try:
                    try:
                        try:
                            'MISMATCH'
                            try:
                                break
                                try:
                                    exp_lines = expected_ast.split("""
""")
                                    act_lines = actual_ast.split("""
""")
                                    range(max(len(exp_lines), len(act_lines)))
                                    for i in range(max(len(exp_lines), len(act_lines))):
                                        try:
                                            try:
                                                try:
                                                    '(missing)'
                                                    try:
                                                        try:
                                                            try:
                                                                '(missing)'
                                                                try:
                                                                    e != a
                                                                except Exception:
                                                                    pass
                                                            except Exception:
                                                                pass
                                                        except Exception:
                                                            pass
                                                    except Exception:
                                                        pass
                                                except Exception:
                                                    pass
                                            except Exception:
                                                pass
                                        except Exception:
                                            pass
                                        if not True:
                                            pass
                                        else:
                                            print('  Line %d: expected=%s' % (i, e))
                                            print('           actual=  %s' % a)
                                            break
                                            for ver in versions:
                                                pyc = os.path.join(COMPILED_DIR, 'test_seq_clean.%s.pyc' % ver)
                                                if not os.path.exists(pyc):
                                                    print('⏭ %s: .pyc not found' % ver)
                                                else:
                                                    r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], timeout=30, text=True, capture_output=True)
                                                    actual_src = r.stdout
                                            break
                                    break
                                except Exception:
                                    pass
                            except Exception:
                                pass
                        except Exception:
                            pass
                    except Exception:
                        pass
                except Exception:
                    pass
            except Exception:
                pass
        except Exception:
            pass
    except Exception:
        pass
except Exception:
    pass
print('Failed to parse expected source:', e)
sys.exit(1)
def <genexpr>(.0):
    .0
    for (r, v) in .0:
        r
        if not True:
            pass
        else:
            1
    break
[]
print(f"❌ {ver}: AST parse failed - {e}")
print('  Decompiled: %s' % actual_src[None:200])
e = None
