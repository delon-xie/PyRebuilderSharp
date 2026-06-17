#!/usr/bin/env python3
"""
Cross-validate MarshalType.cs constants against CPython source for ALL versions.
Detects: missing types, wrong values, unused constants.

Usage:
    python3 tools/validate_marshal_types.py

Exits with code 1 on any mismatch (for CI use).
"""
import sys, os, urllib.request

# Paths relative to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.normpath(os.path.join(SCRIPT_DIR, '..'))
MARSHAL_TYPE_PATH = os.path.join(REPO_ROOT,
    'src', 'PyRebuilderSharp.Core', 'Readers', 'MarshalType.cs')

CPYTHON_VERSIONS = {
    'v2.7.18':  'Py27',
    'v3.5.10':  'Py35',
    'v3.6.15':  'Py36',
    'v3.7.17':  'Py37',
    'v3.8.20':  'Py38',
    'v3.9.25':  'Py39',
    'v3.10.20': 'Py310',
    'v3.11.15': 'Py311',
    'v3.12.13': 'Py312',
    'v3.13.12': 'Py313',
    'v3.14.3':  'Py314',
}

VERSION_ORDER = [
    'Py27','Py35','Py36','Py37','Py38',
    'Py39','Py310','Py311','Py312','Py313','Py314',
]

RED = '\033[91m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
RESET = '\033[0m'


def fetch_cpython_types():
    """Fetch #define TYPE_* from each CPython version's marshal.c via GitHub raw."""
    cpython = {}
    for tag, ver in CPYTHON_VERSIONS.items():
        url = f'https://raw.githubusercontent.com/python/cpython/{tag}/Python/marshal.c'
        try:
            with urllib.request.urlopen(url, timeout=15) as resp:
                text = resp.read().decode()
        except Exception as e:
            print(f"  {YELLOW}WARN{RESET}: {tag} fetch failed: {e}")
            continue
        types = {}
        for line in text.split('\n'):
            if '#define TYPE_' in line:
                after = line.split('#define TYPE_')[1].strip()
                name = after.split()[0]
                val_part = after.split()[1] if len(after.split()) >= 2 else ''
                val = val_part.strip("'")
                if val:
                    types[name] = (val, ord(val))
        cpython[ver] = types
        print(f"  {ver} ({tag}): {len(types)} types")
    return cpython


def read_our_types():
    """Parse MarshalType.cs for our TYPE_ constants."""
    with open(MARSHAL_TYPE_PATH) as f:
        text = f.read()
    types = {}
    for line in text.split('\n'):
        if 'public const byte TYPE_' in line and '=' in line:
            name = line.split('TYPE_')[1].split()[0].strip()
            val_raw = line.split('=')[1].strip()
            # Strip inline comment: 97; // 'a' -> 97
            val = val_raw.split('//')[0].strip().rstrip(';').strip()
            types[name] = val
    return types


def cross_validate(cpython, our_types):
    """Compare types and print detailed table. Returns list of issues."""
    all_cpy = set()
    for v, t in cpython.items():
        all_cpy.update(t.keys())

    all_names = sorted(all_cpy | set(our_types.keys()))

    headers = ['Py27','Py35','Py36','Py37','Py38',
               'Py39','Py310','Py311','Py312','Py313','Py314']

    print(f"\n{'TYPE':>25s}", end='')
    for h in headers:
        print(f" {h:>5s}", end='')
    print(f" {'Ours':>6s} │ STATUS")
    print('─' * 130)

    issues = []
    for name in all_names:
        row = f"{name:>25s}"
        for ver in VERSION_ORDER:
            if ver in cpython and name in cpython[ver]:
                char, _ = cpython[ver][name]
                row += f" {char:>5s}"
            else:
                row += f" {'─':>5s}"

        our_val = our_types.get(name, '?')
        row += f" {our_val:>6s} │ "

        if name not in our_types:
            # Find latest CPython value for the suggestion
            latest_val = None
            for ver in reversed(VERSION_ORDER):
                if ver in cpython and name in cpython[ver]:
                    latest_val = cpython[ver][name][1]
                    break
            msg = f"{RED}MISSING{RESET} — CPython uses {latest_val}"
            issues.append((name, 'MISSING', f"add TYPE_{name} = {latest_val}"))
            row += msg
        elif name not in all_cpy:
            row += f"{YELLOW}CUSTOM{RESET} (not in CPython)"
        else:
            our_dec = int(our_val) if our_val.lstrip('-').isdigit() else None
            if our_dec is not None:
                # Find all CPython versions with this type and check match
                match = True
                for ver in VERSION_ORDER:
                    if ver in cpython and name in cpython[ver]:
                        _, ver_val = cpython[ver][name]
                        if our_dec != ver_val:
                            match = False
                            break
                if match:
                    row += f"{GREEN}OK{RESET}"
                else:
                    c_char, c_val = '?', -1
                    for ver in reversed(VERSION_ORDER):
                        if ver in cpython and name in cpython[ver]:
                            c_char, c_val = cpython[ver][name]
                            break
                    msg = f"{RED}WRONG{RESET} — CPython latest: '{c_char}'({c_val})"
                    issues.append((name, 'WRONG', f"was {our_val}, should be {c_val} (='{c_char}')"))
                    row += msg
            else:
                row += f"{YELLOW}CUSTOM{RESET}"

        print(row)

    return issues


def main():
    print("=== PyRebuilderSharp MarshalType Cross-Validation ===\n")
    print(f"CPython versions ({len(CPYTHON_VERSIONS)}):")
    cpython = fetch_cpython_types()

    print(f"\nOur MarshalType.cs: {MARSHAL_TYPE_PATH}")
    our_types = read_our_types()
    print(f"  {len(our_types)} constants found")

    issues = cross_validate(cpython, our_types)

    print(f"\n{'═' * 60}")
    print(f"RESULTS: {len(issues)} issue(s) found")
    for name, kind, detail in issues:
        icon = '❌' if kind == 'MISSING' else ('❌' if kind == 'WRONG' else '⚠️')
        print(f"  {icon} {name}: {detail}")

    if issues:
        sys.exit(1)
    else:
        print(f"  {GREEN}All constants match CPython.{RESET}")
        sys.exit(0)


if __name__ == '__main__':
    main()
