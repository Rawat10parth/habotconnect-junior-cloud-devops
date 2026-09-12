import json
import unittest
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


class StudentOnboardingSerializerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        project_root = Path(__file__).resolve().parents[1]
        payload_path = project_root / "schema" / "student_onboarding.json"

        with payload_path.open("r", encoding="utf-8") as file:
            cls.valid_payload = json.load(file)

    def test_valid_onboarding_payload_is_accepted(self):
        serializer = StudentOnboardingSerializer(data=self.valid_payload)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

    def test_invalid_phone_is_rejected(self):
        payload = self.valid_payload.copy()
        payload["phone"] = "12345"

        serializer = StudentOnboardingSerializer(data=payload)

        self.assertFalse(serializer.is_valid())
        self.assertIn("phone", serializer.errors)

    def test_invalid_age_is_rejected(self):
        payload = self.valid_payload.copy()
        payload["age"] = 17

        serializer = StudentOnboardingSerializer(data=payload)

        self.assertFalse(serializer.is_valid())
        self.assertIn("age", serializer.errors)

    def test_missing_required_field_is_rejected(self):
        payload = self.valid_payload.copy()
        del payload["email"]

        serializer = StudentOnboardingSerializer(data=payload)

        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_failed_dcyn_requirement_is_rejected(self):
        payload = self.valid_payload.copy()
        payload["has_passport"] = False

        serializer = StudentOnboardingSerializer(data=payload)

        self.assertFalse(serializer.is_valid())
        self.assertIn("has_passport", serializer.errors)


if __name__ == "__main__":
    unittest.main()