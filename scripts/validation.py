"""
validation.py
-------------
Validation Script: "Are we building the right product?"
Reads requirements.json and expected_structure.json to validate that
requirements.json contains all expected sub-requirements (A, B, C)
for each parent requirement defined in expected_structure.json.
"""

import json
import sys


def load_json(filepath):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] File not found: {filepath}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON in {filepath}: {e}")
        sys.exit(1)


def run_validation(requirements, expected_structure):
    results = []

    # Build a mapping: parent -> list of sub-suffixes present
    # e.g. "REQ-HAZ-001" -> ["A", "B", "C"]
    parent_map = {}
    for req in requirements:
        parent = req.get("parent")
        req_id = req.get("requirement_id", "")
        if parent:
            suffix = req_id.replace(parent, "").strip()
            parent_map.setdefault(parent, []).append(suffix)

    for parent_id, expected_suffixes in expected_structure.items():
        actual_suffixes = parent_map.get(parent_id, [])
        missing = [s for s in expected_suffixes if s not in actual_suffixes]

        passed = len(missing) == 0
        results.append({
            "parent_id": parent_id,
            "expected": expected_suffixes,
            "actual": actual_suffixes,
            "missing": missing,
            "status": "PASS" if passed else "FAIL"
        })

    return results


def main():
    print("=" * 60)
    print("  VALIDATION - Requirements Structure Check")
    print("=" * 60)

    requirements = load_json("requirements.json")
    expected_structure = load_json("expected_structure.json")

    results = run_validation(requirements, expected_structure)

    passed = 0
    failed = 0

    for r in results:
        icon = "✅" if r["status"] == "PASS" else "❌"
        print(f"\n{icon} [{r['status']}] {r['parent_id']}")
        print(f"   Expected sub-requirements : {r['expected']}")
        print(f"   Actual sub-requirements   : {r['actual']}")
        if r["missing"]:
            print(f"   Missing                   : {r['missing']}")

        if r["status"] == "PASS":
            passed += 1
        else:
            failed += 1

    print("\n" + "=" * 60)
    print(f"  Results: {passed} PASSED | {failed} FAILED")
    print("=" * 60)

    if failed > 0:
        print("\n[VALIDATION FAILED] requirements.json is missing expected sub-requirements.")
        sys.exit(1)
    else:
        print("\n[VALIDATION PASSED] requirements.json matches expected structure.")
        sys.exit(0)


if __name__ == "__main__":
    main()
