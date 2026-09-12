import json
import sys
from pathlib import Path

from django.conf import settings

if not settings.configured:
    settings.configure(
        SECRET_KEY="test-secret-key",
        USE_I18N=False,
        DEFAULT_CHARSET="utf-8",
    )

import django

django.setup()

from student_onboarding.serializers import StudentOnboardingSerializer


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PAYLOAD_PATH = PROJECT_ROOT / "schema" / "student_onboarding.json"


def run_validation_demo():
    with PAYLOAD_PATH.open("r", encoding="utf-8") as file:
        valid_payload = json.load(file)

    invalid_cases = {
        "Invalid phone": {
            **valid_payload,
            "phone": "12345",
        },
        "Invalid age": {
            **valid_payload,
            "age": 17,
        },
        "DCYN string YES": {
            **valid_payload,
            "has_passport": "yes",
        },
        "DCYN string NO": {
            **valid_payload,
            "has_passport": "no",
        },
        "Unexpected field": {
            **valid_payload,
            "unexpected_field": "not allowed",
        },
        "Failed DCYN requirement": {
            **valid_payload,
            "has_passport": False,
        },
    }

    print("Student Onboarding Poka-Yoke Validation Demo")
    print("=" * 50)

    all_passed = True

    for name, payload in invalid_cases.items():
        serializer = StudentOnboardingSerializer(data=payload)
        accepted = serializer.is_valid()

        expected_result = "REJECT"
        actual_result = "ACCEPT" if accepted else "REJECT"

        passed = actual_result == expected_result

        print(f"\nTest:     {name}")
        print(f"Expected: {expected_result}")
        print(f"Actual:   {actual_result}")
        print(f"Result:   {'PASS' if passed else 'FAIL'}")

        if not passed:
            print(f"Errors:   {serializer.errors}")
            all_passed = False

    print("\n" + "=" * 50)

    if all_passed:
        print("ALL FAILURE-PATH TESTS PASSED")
        print("Invalid onboarding data was rejected as expected.")
        return 0

    print("FAILURE-PATH TEST FAILED")
    print("An invalid onboarding payload was incorrectly accepted.")
    return 1


if __name__ == "__main__":
    sys.exit(run_validation_demo())