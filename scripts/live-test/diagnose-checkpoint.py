#!/usr/bin/env python3
"""diagnose-checkpoint.py — authoritative failure report for a failed run.

Reads .oxo-flow/checkpoint.json (the engine's own record): failed_rules
names the rules that actually failed (not the decoy last-scheduled rule
in the log), and rule_runs[<rule>].stderr_tail carries the evidence.

Usage: diagnose-checkpoint.py [repo-dir]   (default: current directory)
"""
import json
import os
import sys

def main() -> int:
    repo = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    path = os.path.join(repo, ".oxo-flow", "checkpoint.json")
    if not os.path.exists(path):
        print(f"no checkpoint at {path}", file=sys.stderr)
        return 1
    d = json.load(open(path))
    failed = d.get("failed_rules", [])
    print(f"failed_rules: {failed}")
    runs = d.get("rule_runs", {})
    for k, v in runs.items():
        if v.get("exit_code") in (0, "0") or v.get("exit_code") is None:
            continue
        stderr = str(v.get("stderr_tail", ""))
        print(f"\n== {k} | exit {v.get('exit_code')}")
        print(stderr[-800:])
    if not failed:
        print("no failed_rules recorded — the run may have been killed"
              " externally (OOM, parking, lane kill) or aborted at the"
              " graph level.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
