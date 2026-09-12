import json
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

D0_INPUT_PATH = (
    PROJECT_ROOT
    / "pipeline"
    / "d0_raw"
    / "student_onboarding_batch.json"
)
OUTPUT_DIR = PROJECT_ROOT / "pipeline" / "output"

D1_OUTPUT_PATH = OUTPUT_DIR / "d1_valid_records.json"
QUARANTINE_OUTPUT_PATH = OUTPUT_DIR / "quarantine_records.json"


def format_validation_errors(errors):
    """Convert DRF validation errors into readable text."""
    messages = []

    for field, field_errors in errors.items():
        for error in field_errors:
            messages.append(f"{field}: {error}")

    return "; ".join(messages)


def process_batch(input_path=None, output_dir=None):
    input_path = Path(input_path) if input_path else D0_INPUT_PATH
    output_dir = Path(output_dir) if output_dir else OUTPUT_DIR

    d1_output_path = output_dir / "d1_valid_records.json"
    quarantine_output_path = output_dir / "quarantine_records.json"

    with input_path.open("r", encoding="utf-8") as file:
        batch = json.load(file)

    students = batch.get("students", [])
    valid_records = []
    quarantine_records = []

    print("Student Onboarding D0 -> DCYN -> D1 Pipeline")
    print("=" * 50)
    print(f"Input records: {len(students)}")
    print(f"D0 source: {input_path}")
    print()

    for index, student in enumerate(students, start=1):
        serializer = StudentOnboardingSerializer(data=student)

        if serializer.is_valid():
            validated_record = serializer.validated_data.copy()
            validated_record["access_scope"] = "ANALYTICS"

            valid_records.append(validated_record)

            print(f"Student {index}: ACCEPTED -> D1")
        else:
            error_message = format_validation_errors(serializer.errors)

            quarantine_records.append(
                {
                    "record_number": index,
                    "student": student,
                    "status": "QUARANTINED",
                    "validation_errors": serializer.errors,
                }
            )

            print(f"Student {index}: REJECTED -> QUARANTINE")
            print(f"           Reason: {error_message}")

    output_dir.mkdir(parents=True, exist_ok=True)

    with d1_output_path.open("w", encoding="utf-8") as file:
        json.dump(
            {
                "records": valid_records,
                "count": len(valid_records),
            },
            file,
            indent=2,
        )

    with quarantine_output_path.open("w", encoding="utf-8") as file:
        json.dump(
            {
                "records": quarantine_records,
                "count": len(quarantine_records),
            },
            file,
            indent=2,
        )

    print("\n" + "=" * 50)
    print(f"Total records: {len(students)}")
    print(f"Accepted:      {len(valid_records)}")
    print(f"Rejected:      {len(quarantine_records)}")
    print(f"D1 records:    {len(valid_records)}")
    print(f"Quarantined:   {len(quarantine_records)}")

    print("\nD1 output:")
    print(d1_output_path)

    print("\nQuarantine output:")
    print(quarantine_output_path)

    return {
        "total": len(students),
        "accepted": len(valid_records),
        "rejected": len(quarantine_records),
        "d1_records": len(valid_records),
        "quarantined": len(quarantine_records),
    }


if __name__ == "__main__":
    process_batch()