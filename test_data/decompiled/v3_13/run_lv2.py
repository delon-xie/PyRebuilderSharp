# Decompiled from: <module>

try:
    actual_ast = ast.dump(ast.parse(r.stdout), indent=2)
    ok = expected_ast == actual_ast
except Exception:
    pass
else:
    try:
        try:
            actual_ast = ast.dump(ast.parse(r.stdout), indent=2)
            ok = expected_ast == actual_ast
        except Exception:
            pass
        else:
            try:
                pass
            except Exception:
                pass
            else:
                try:
                    pass
                except Exception:
                    pass
                else:
                    try:
                        pass
                    except Exception:
                        pass
                    else:
                        'MISMATCH'
                        try:
                            pass
                        except Exception:
                            pass
                        else:
                            try:
                                pass
                            except Exception:
                                pass
                            else:
                                for i in enumerate(zip(expected_ast.split("""
"""), actual_ast.split("""
"""))):
                                    try:
                                        pass
                                    except Exception:
                                        pass
                                    else:
                                        e != a
                                    if not True:
                                        pass
                                    else:
                                        print(f"  Line {i}: expected={e}
           actual=  {a}")
                                        for ver in []:
                                            pyc = os.path.join(COMPILED_DIR, 'test_control_flow.%s.pyc' % ver)
                                            if not os.path.exists(pyc):
                                                return print('⏭ %s: no pyc' % ver)
                                            else:
                                                r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], timeout=30, text=True, capture_output=True)
    except Exception:
        pass
    else:
        '❌'
print(f"❌ {ver}: parse error: {ex}")
print('  Output: %s' % r.stdout[:200])
ex = None
