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

from pipeline.process_onboarding import process_batch


class BatchPipelineTests(unittest.TestCase):
    def test_ten_student_batch_is_processed_correctly(self):
        project_root = Path(__file__).resolve().parents[1]
        batch_path = project_root / "schema" / "student_onboarding_batch.json"

        with batch_path.open("r", encoding="utf-8") as file:
            batch = json.load(file)

        self.assertEqual(len(batch["students"]), 10)

        result = process_batch()

        self.assertEqual(result["total"], 10)
        self.assertEqual(result["accepted"], 6)
        self.assertEqual(result["rejected"], 4)
        self.assertEqual(result["d1_records"], 6)
        self.assertEqual(result["quarantined"], 4)


if __name__ == "__main__":
    unittest.main()