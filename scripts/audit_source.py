#!/usr/bin/env python3
"""Check owned Lean sources, complete root imports, and the coverage ledger.

Run after `lake build`. This structural guard complements the transitive kernel
axiom audit and the separately documented mathematical correspondence review.
It does not infer that a theorem has the meaning claimed by a ledger entry.
"""
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent.parent
PROJECT = "GaussianMomentsCounterexamples"
FORBIDDEN = re.compile(
    r"(?<![\w'])"
    r"(sorry|sorryAx|admit|axiom|unsafe|native_decide|implemented_by|extern|ofReduceBool|ofReduceNat)"
    r"(?![\w'])"
)


def lean_code(source: str) -> str:
    """Mask nested comments and literal strings without changing line numbers.

Interpolated strings are conservatively retained, including all embedded Lean
expressions. This intentionally rejects forbidden words in their literal text
as well. Ordinary and raw strings have no embedded executable expressions.
"""
    out = list(source)
    i = 0

    def mask(start: int, end: int) -> None:
        for j in range(start, end):
            if out[j] != "\n":
                out[j] = " "

    while i < len(source):
        start = i
        if source.startswith("--", i):
            end = source.find("\n", i)
            i = len(source) if end < 0 else end
            mask(start, i)
        elif source.startswith("/-", i):
            depth = 1
            i += 2
            while i < len(source) and depth:
                if source.startswith("/-", i):
                    depth += 1
                    i += 2
                elif source.startswith("-/", i):
                    depth -= 1
                    i += 2
                else:
                    i += 1
            if depth:
                raise ValueError("Unterminated Lean block comment")
            mask(start, i)
        elif raw := re.match(r'r(#+)?"', source[i:]):
            terminator = '"' + (raw[1] or "")
            end = source.find(terminator, i + len(raw[0]))
            if end < 0:
                raise ValueError("Unterminated Lean raw string")
            i = end + len(terminator)
            mask(start, i)
        elif source[i] == '"':
            interpolated = i > 0 and source[i - 1] == "!"
            i += 1
            braces = 0
            while i < len(source):
                if source[i] == "\\":
                    i += 2
                elif interpolated and source[i] == "{":
                    braces += 1
                    i += 1
                elif interpolated and source[i] == "}" and braces:
                    braces -= 1
                    i += 1
                elif source[i] == '"':
                    if not braces:
                        break
                    # A literal nested in an interpolated Lean expression.
                    i += 1
                    while i < len(source) and source[i] != '"':
                        i += 2 if source[i] == "\\" else 1
                    i += 1
                else:
                    i += 1
            if i >= len(source):
                raise ValueError("Unterminated Lean string")
            i += 1
            if not interpolated:
                mask(start, i)
        elif char := re.match(r"'(?:[^'\\\n]|\\(?:u[0-9a-fA-F]{4}|x[0-9a-fA-F]{2}|.))'", source[i:]):
            i += len(char[0])
            mask(start, i)
        else:
            i += 1
    return "".join(out)


def source_files() -> list[Path]:
    """Include ignored or untracked owned source; exclude dependency/build trees."""
    return sorted(p for p in ROOT.rglob("*.lean")
                  if not any(part.startswith(".") for part in p.relative_to(ROOT).parts))


def imports(code: str) -> list[str]:
    result = []
    for match in re.finditer(r"^\s*(?:(?:public|private)\s+)?import\s+([^\n]+)", code, re.M):
        for name in match[1].split():
            if not re.fullmatch(r"[\w.]+", name):
                raise ValueError(f"Unrecognized import syntax: {match[0].strip()}")
            result.append(name)
    return result


def check_lean() -> None:
    files = source_files()
    if not files:
        raise ValueError("No owned Lean sources")
    modules = {}
    for path in files:
        relative = path.relative_to(ROOT)
        code = lean_code(path.read_text(encoding="utf-8"))
        if match := FORBIDDEN.search(code):
            line = code.count("\n", 0, match.start()) + 1
            raise ValueError(f"Forbidden proof escape {match[0]}: {relative}:{line}")
        name = ".".join(relative.with_suffix("").parts)
        if relative.parts[0] == "scripts":
            # Proof-bearing auxiliary files must join the module-origin audit.
            # Audit scripts themselves only inspect the imported environment.
            declaration = re.search(
                r"^\s*(?:(?:private|protected|noncomputable|public)\s+)*"
                r"(?:theorem|lemma|def|abbrev|opaque|instance|class|structure|inductive|example)\b",
                code, re.M)
            if declaration:
                raise ValueError(f"Move auxiliary proof declarations into the audited library: {relative}")
        else:
            if name != PROJECT and not name.startswith(PROJECT + "."):
                raise ValueError(f"Owned mathematical module outside library: {relative}")
            modules[name] = code
    active, done = set(), set()

    def visit(name: str) -> None:
        if name in active:
            raise ValueError(f"Circular project import: {name}")
        if name in done:
            return
        if name not in modules:
            raise ValueError(f"Missing project module: {name}")
        active.add(name)
        for dependency in imports(modules[name]):
            if dependency == PROJECT or dependency.startswith(PROJECT + "."):
                visit(dependency)
            elif dependency.startswith("scripts."):
                raise ValueError(f"Mathematical module imports auxiliary script: {dependency}")
        active.remove(name)
        done.add(name)

    visit(PROJECT)
    if set(modules) != done:
        raise ValueError(f"Modules absent from root import closure: {sorted(set(modules) - done)}")
    print(f"Source audit passed: {len(files)} owned files, {len(done)} library modules in root closure.")


def check_ledger() -> None:
    ledger = (ROOT / "FORMALIZATION_STATUS.md").read_text(encoding="utf-8")
    sections = re.split(r"^###\s+`?([\w:-]+)`?\s*$", ledger, flags=re.M)
    ids = sections[1::2]
    if not ids or len(ids) != len(set(ids)):
        raise ValueError("Empty ledger or duplicate entry identifiers")
    entries, declarations = {}, set()
    required = {"Status", "Class", "Location", "Obligation", "Lean", "Dependencies", "Remaining"}
    for name, body in zip(ids, sections[2::2]):
        pairs = re.findall(r"^- ([A-Za-z]+):\s*(.+)$", body, re.M)
        fields = dict(pairs)
        if len(fields) != len(pairs) or not required <= fields.keys():
            raise ValueError(f"Incomplete or duplicate ledger fields: {name}")
        if fields["Status"] not in {"proved", "partial", "missing", "blocked"}:
            raise ValueError(f"Invalid ledger status: {name}")
        if fields["Class"] not in {"core", "supporting"}:
            raise ValueError(f"Invalid ledger classification: {name}")
        refs = [] if fields["Lean"] == "none" else [r.strip().strip("`") for r in fields["Lean"].split(",")]
        for ref in refs:
            if not re.fullmatch(PROJECT + r"\.[\w'.]+", ref):
                raise ValueError(f"Invalid project declaration reference: {name}: {ref}")
        if fields["Status"] == "proved" and not refs:
            raise ValueError(f"Proved ledger entry without declarations: {name}")
        declarations.update(refs)
        fields["deps"] = [] if fields["Dependencies"] == "none" else [
            r.strip().strip("`") for r in fields["Dependencies"].split(",")]
        entries[name] = fields
    active, done = set(), set()

    def visit(name: str) -> None:
        if name not in entries:
            raise ValueError(f"Missing ledger dependency: {name}")
        if name in active:
            raise ValueError(f"Circular ledger dependency: {name}")
        if name in done:
            return
        active.add(name)
        for dependency in entries[name]["deps"]:
            visit(dependency)
            if entries[name]["Status"] == "proved" and entries[dependency]["Status"] != "proved":
                raise ValueError(f"Proved entry {name} depends on {entries[dependency]['Status']} entry {dependency}")
        active.remove(name)
        done.add(name)

    for name in entries:
        visit(name)
    tex = (ROOT / "gaussian_moments_counterexamples.tex").read_text(encoding="utf-8")
    labels = re.findall(r"\\label\{((?:eq|prop|thm|cor|lem):[^}]+)\}", tex)
    locations = "\n".join(fields["Location"] for fields in entries.values())
    for label in labels:
        if not re.search(r"(?<![\w:-])" + re.escape(label) + r"(?![\w:-])", locations):
            raise ValueError(f"Manuscript label absent from ledger locations: {label}")
    if not declarations:
        raise ValueError("Ledger has no checked Lean references")
    # Lean, not lexical name matching, resolves every declaration reference.
    probe = f"import {PROJECT}\n" + "\n".join(f"#check {ref}" for ref in sorted(declarations)) + "\n"
    with tempfile.TemporaryDirectory(prefix="gaussian-coverage-") as tmp:
        path = Path(tmp) / "CoverageReferences.lean"
        path.write_text(probe, encoding="utf-8")
        result = subprocess.run(["lake", "env", "lean", str(path)], cwd=ROOT,
                                text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if result.returncode:
            raise ValueError("Lean ledger reference check failed:\n" + result.stdout)
    counts = {status: sum(fields["Status"] == status for fields in entries.values())
              for status in ("proved", "partial", "missing", "blocked")}
    print(f"Ledger audit passed: {len(entries)} entries, {counts}; acyclic dependencies; "
          f"{len(declarations)} elaborated declaration references; {len(labels)} labels covered.")


if __name__ == "__main__":
    try:
        check_lean()
        check_ledger()
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        raise SystemExit(f"Source/coverage audit failed: {error}") from error
