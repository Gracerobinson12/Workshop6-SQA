"""
verification.py
---------------
Verification Script: "Are we building the product right?"
Reads test_cases.json and requirements.json to verify that every
requirement has at least one corresponding test case.
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


def run_verification(requirements, test_cases):
    results = []

    # Build set of requirement_ids covered by test cases
    covered_ids = set(tc["requirement_id"] for tc in test_cases)

    for req in requirements:
        req_id = req["requirement_id"]
        covered = req_id in covered_ids

        results.append({
            "requirement_id": req_id,
            "description": req.get("description", ""),
            "source": req.get("source", ""),
            "has_test_case": covered,
            "status": "PASS" if covered else "FAIL"
        })

    return results


def main():
    print("=" * 60)
    print("  VERIFICATION - Hazard Analysis Requirements")
    print("=" * 60)

    requirements = load_json("requirements.json")
    test_cases = load_json("test_cases.json")

    results = run_verification(requirements, test_cases)

    passed = 0
    failed = 0

    for r in results:
        icon = "✅" if r["status"] == "PASS" else "❌"
        print(f"\n{icon} [{r['status']}] {r['requirement_id']}")
        print(f"   Description : {r['description']}")
        print(f"   Source      : {r['source']}")
        print(f"   Test Case   : {'Found' if r['has_test_case'] else 'MISSING'}")

        if r["status"] == "PASS":
            passed += 1
        else:
            failed += 1

    print("\n" + "=" * 60)
    print(f"  Results: {passed} PASSED | {failed} FAILED")
    print("=" * 60)

    if failed > 0:
        print("\n[VERIFICATION FAILED] Some requirements have no test cases.")
        sys.exit(1)
    else:
        print("\n[VERIFICATION PASSED] All requirements have test cases.")
        sys.exit(0)


if __name__ == "__main__":
    main()
