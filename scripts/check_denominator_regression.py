"""Offline regression for denominator language; never calls a model API."""
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
spec = importlib.util.spec_from_file_location("assistant", ROOT / "19_metric_assistant.py")
assistant = importlib.util.module_from_spec(spec)
spec.loader.exec_module(assistant)

cases = json.loads((ROOT / "evals/denominator_regression.json").read_text(encoding="utf-8"))
failures = []
for case in cases:
    result = assistant.answer(case["question"])
    if result["status"] != case["expected_status"]:
        failures.append(f"{case['id']}: status={result['status']} expected={case['expected_status']}")
        continue
    expected_field = case.get("expected_share_field")
    if expected_field and result.get("share_field") != expected_field:
        failures.append(f"{case['id']}: share_field={result.get('share_field')} expected={expected_field}")

if failures:
    raise AssertionError("\n".join(failures))
print(f"PASS: {len(cases)}/{len(cases)} denominator-language regression cases passed; no model API called.")
