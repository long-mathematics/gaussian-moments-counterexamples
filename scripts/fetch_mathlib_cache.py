#!/usr/bin/env python3
"""Fetch the pinned cache for direct Mathlib imports and their dependencies.

The Mathlib cache tool does not follow this project's own root import graph.
Enumerating direct library imports avoids downloading all of Mathlib and never
substitutes dependency caches for building this project's proofs.
"""
import os
import subprocess
from audit_source import ROOT, imports, lean_code, source_files


def main() -> None:
    modules = sorted({name for path in source_files()
                      for name in imports(lean_code(path.read_text(encoding="utf-8")))
                      if name.startswith("Mathlib.")})
    if not modules:
        raise SystemExit("No direct Mathlib imports found")
    print(f"Fetching pinned cache for {len(modules)} direct Mathlib imports and their dependencies.", flush=True)
    subprocess.run(["lake", "exe", "cache", "get", *modules], cwd=ROOT, check=True,
                   env={**os.environ, "MATHLIB_NO_CACHE_ON_UPDATE": "1"})


if __name__ == "__main__":
    main()
