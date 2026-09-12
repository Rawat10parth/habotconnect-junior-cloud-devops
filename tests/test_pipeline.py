import json
import tempfile
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

        source_path = (
            project_root
            / "schema"
            / "student_onboarding_batch.json"
        )

        with source_path.open("r", encoding="utf-8") as file:
            batch = json.load(file)

        self.assertEqual(len(batch["students"]), 10)

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            d0_path = temp_path / "d0_raw"
            output_path = temp_path / "output"

            d0_path.mkdir()

            d0_input = d0_path / "student_onboarding_batch.json"

            with d0_input.open("w", encoding="utf-8") as file:
                json.dump(batch, file, indent=2)

            result = process_batch(
                input_path=d0_input,
                output_dir=output_path,
            )

            self.assertEqual(result["total"], 10)
            self.assertEqual(result["accepted"], 6)
            self.assertEqual(result["rejected"], 4)
            self.assertEqual(result["d1_records"], 6)
            self.assertEqual(result["quarantined"], 4)

            self.assertTrue(
                (output_path / "d1_valid_records.json").exists()
            )

            self.assertTrue(
                (output_path / "quarantine_records.json").exists()
            )


if __name__ == "__main__":
    unittest.main()