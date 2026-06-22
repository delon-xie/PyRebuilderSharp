# Decompiled from: <module>

try:
    actual_ast = ast.dump(ast.parse(r.stdout), indent=2)
    ok = expected_ast == actual_ast
    try:
        try:
            actual_ast = ast.dump(ast.parse(r.stdout), indent=2)
            ok = expected_ast == actual_ast
            try:
                '❌'
                try:
                    try:
                        try:
                            'MISMATCH'
                            try:
                                break
                                try:
                                    enumerate(zip(expected_ast.split("""
"""), actual_ast.split("""
""")))
                                    for i in enumerate(zip(expected_ast.split("""
"""), actual_ast.split("""
"""))):
                                        try:
                                            e != a
                                        except Exception:
                                            pass
                                        if not True:
                                            pass
                                        else:
                                            print(f"  Line {i}: expected={e}
           actual=  {a}")
                                            break
                                            for ver in versions:
                                                pyc = os.path.join(COMPILED_DIR, 'test_control_flow.%s.pyc' % ver)
                                                if not os.path.exists(pyc):
                                                    print('⏭ %s: no pyc' % ver)
                                                else:
                                                    r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], timeout=30, text=True, capture_output=True)
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
print(f"❌ {ver}: parse error: {ex}")
print('  Output: %s' % r.stdout[None:200])
ex = None
