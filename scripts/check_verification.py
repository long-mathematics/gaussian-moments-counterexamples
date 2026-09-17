#!/usr/bin/env python3
"""Run the exact verifier and require byte-for-byte reference output."""

import difflib
import os
from pathlib import Path
import subprocess
import sys


SCRIPTS = Path(__file__).resolve().parent
STEM = "verify_gaussian_moments_counterexamples"


def main() -> int:
    expected = (SCRIPTS / f"{STEM}.txt").read_bytes()
    env = dict(os.environ)
    env.pop("PYTHONOPTIMIZE", None)
    env["PYTHONHASHSEED"] = "0"
    try:
        run = subprocess.run(
            [sys.executable, "-u", str(SCRIPTS / f"{STEM}.py")],
            cwd=SCRIPTS.parent,
            env=env,
            capture_output=True,
            timeout=1200,
        )
    except subprocess.TimeoutExpired:
        print(f"FAIL {STEM}: timed out after 1200 seconds")
        return 1

    if run.returncode != 0 or run.stdout != expected or run.stderr:
        diff = "".join(
            difflib.unified_diff(
                expected.decode().splitlines(keepends=True),
                run.stdout.decode(errors="replace").splitlines(keepends=True),
                fromfile=f"{STEM}.txt (recorded)",
                tofile=f"{STEM}.txt (fresh)",
            )
        )
        print(f"FAIL {STEM}: exit {run.returncode}")
        print(diff, end="")
        print(run.stderr.decode(errors="replace"), end="")
        return 1

    print(f"PASS {STEM}: exact output match")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

