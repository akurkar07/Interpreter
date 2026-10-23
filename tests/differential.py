"""Differential test: every example must produce identical output on all three backends.

For each examples/*.pas file this script runs
  1. the tree-walking interpreter,
  2. the Python stack VM on bytecode emitted from the same source, and
  3. the native C VM (build/vm) on the same bytecode,
and fails if any backend's output differs from the interpreter's.

Usage:  python tests/differential.py            (expects build/vm to exist)
        python tests/differential.py --no-native (skip the C VM)
"""

from __future__ import annotations

import contextlib
import io
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from pascal.main import compile_script, run_script, run_vm_script  # noqa: E402

EXAMPLES = sorted((ROOT / "examples").glob("*.pas"))
NATIVE_VM = ROOT / "build" / ("vm.exe" if sys.platform == "win32" else "vm")


def capture(fn, *args) -> str:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn(*args)
    return buf.getvalue()


def interpreter_output(source: Path) -> str:
    out = capture(run_script, source)
    # run_script prints a "Running NAME..." banner before the program's own output.
    return out.split("\n", 1)[1] if out.startswith("Running ") else out


def python_vm_output(bytecode: Path) -> str:
    return capture(run_vm_script, bytecode)


def native_vm_output(bytecode: Path) -> str:
    result = subprocess.run(
        [str(NATIVE_VM), str(bytecode)], capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"native VM exited {result.returncode} on {bytecode.name}: {result.stderr.strip()}"
        )
    return result.stdout


def main() -> int:
    use_native = "--no-native" not in sys.argv
    if use_native and not NATIVE_VM.exists():
        print(f"native VM not found at {NATIVE_VM}; build it with `make` or pass --no-native")
        return 2

    failures = 0
    for source in EXAMPLES:
        capture(compile_script, source)
        bytecode = source.with_suffix(".pbc")

        expected = interpreter_output(source)
        checks = {"python-vm": python_vm_output(bytecode)}
        if use_native:
            try:
                checks["native-vm"] = native_vm_output(bytecode)
            except RuntimeError as err:
                checks["native-vm"] = f"<{err}>"

        bad = [name for name, got in checks.items() if got != expected]
        status = "ok" if not bad else f"MISMATCH ({', '.join(bad)})"
        for name in bad:
            if checks[name].startswith("<native VM exited"):
                status += f" {checks[name]}"
        print(f"{source.name:28s} {status}")
        failures += len(bad)

    backends = 3 if use_native else 2
    print(f"\n{len(EXAMPLES)} programs x {backends} backends, {failures} mismatches")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
