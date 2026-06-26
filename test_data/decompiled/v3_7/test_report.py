# Decompiled from: <module>

import subprocess
import os
result = subprocess.run(['python3', 'tests/run_tests.py'], capture_output=True, text=True)
output = result.stdout + result.stderr
test_groups = {}
current_group = None
passed_groups = [print(f"
总计: {len(passed_groups)} 组通过, {len(failed_groups)} 组失败") for line in output.split("""
""") if line.startswith('***') if current_group and line.strip().endswith('.3.10.pyc')]
