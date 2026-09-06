from pathlib import Path
import ast
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
contracts = list((root / "contracts").glob("*.py"))
if len(contracts) != 1:
    raise SystemExit(f"expected exactly one deployable source, found {len(contracts)}")
ast.parse(contracts[0].read_text(encoding="utf-8"))
subprocess.run([sys.executable, "-m", "pytest", "tests", "-q"], cwd=root, check=True)
print("preflight passed")
