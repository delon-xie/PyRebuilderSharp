import subprocess, os, glob os.chdir("/Users/admin/codes/Tools/PyRebuilderSharp") 
# Test mid-size files (30-200 source lines) 
input_files = sorted(glob.glob("test_data/input/*.py")) 
seen_bases = set() 
targets = [] 
for f in input_files: 
    base = os.path.splitext(os.path.basename(f))[0] 
    if base in seen_bases: 
        continue 
    seen_bases.add(base) 
    pyc = f"test_data/compiled/{base}.3.10.pyc" 
    if os.path.exists(pyc): 
        src_lines = sum(1 for _ in open(f)) 
    if 30 <= src_lines <= 200 and base != "abc": 
        targets.append((src_lines, base, f)) 
        print(f"Testing {len(targets)} mid-size files...\n") 
        results = [] 
        for src_lines, base, src_path in targets: 
            pyc_path = f"test_data/compiled/{base}.3.10.pyc" 
            r = subprocess.run( 
                [
                    "dotnet", 
                    "run", 
                    "--project", 
                    "src/PyRebuilderSharp.Cli", 
                    "-c", 
                    "Release", 
                    "--", 
                    pyc_path
                ], 
                capture_output=True, 
                text=True, 
                timeout=30, 
                cwd="/Users/admin/codes/Tools/PyRebuilderSharp" 
            ) 
            dec_lines = r.stdout.count('\n') 
            src_count = sum(1 for _ in open(src_path)) 
            orphans = r.stderr.count("unprocessed") 
            crashes = len(glob.glob(os.path.expanduser("~/.pyrebuilder/crashes/crash_*.json"))) 
            status = "✅" 
            warns = [] 
            if dec_lines == 0: 
                status, warns = "❌", ["0 lines"] 
            elif dec_lines < src_count * 0.3: 
                status, warns = "⚠️", [f"truncated ({dec_lines}/{src_count})"] 
                if orphans > 0: 
                    warns.append(f"orphans={orphans}") 
                    if crashes > 0: 
                        warns.append(f"crashes={crashes}") 
                        results.append((status, base, dec_lines, src_count, orphans, "; ".join(warns))) 
                        # Print results 
                        for status, base, dec, src, orphans, detail in results: 
                            print(f"{status:>4} {base:30s} {dec:>4}/{src:<4} orp={orphans} {detail[:40]}") 
                        # Summary 
                        passed = sum(1 for r in results if r[0] == "✅") 
                        warned = sum(1 for r in results if r[0] == "⚠️") 
                        failed = sum(1 for r in results if r[0] == "❌") 
                        print(f"\n✅ {passed} ⚠️ {warned} ❌ {failed}") 