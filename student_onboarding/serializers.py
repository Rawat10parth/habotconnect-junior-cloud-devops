from rest_framework import serializers

from .validators import (
    validate_age,
    validate_phone,
    validate_student_name,
)


class StrictBooleanField(serializers.BooleanField):
    """
    Accept only actual JSON boolean values: true or false.
    Strings such as "yes", "no", "true", and "false" are rejected.
    """

    def to_internal_value(self, data):
        if not isinstance(data, bool):
            self.fail("invalid")

        return data


class StudentOnboardingSerializer(serializers.Serializer):
    student_name = serializers.CharField(
        required=True,
        min_length=2,
        max_length=100,
        validators=[validate_student_name],
    )

    email = serializers.EmailField(
        required=True,
        max_length=254,
    )

    phone = serializers.CharField(
        required=True,
        validators=[validate_phone],
    )

    age = serializers.IntegerField(
        required=True,
        validators=[validate_age],
    )

    has_passport = StrictBooleanField(required=True)

    has_academic_documents = StrictBooleanField(required=True)

    english_proficiency = StrictBooleanField(required=True)

    willing_to_relocate = StrictBooleanField(required=True)

    has_relevant_experience = StrictBooleanField(required=True)

    def validate(self, attrs):
        """
        Enforce the exact input schema and deterministic DCYN decision.
        """

        expected_fields = {
            "student_name",
            "email",
            "phone",
            "age",
            "has_passport",
            "has_academic_documents",
            "english_proficiency",
            "willing_to_relocate",
            "has_relevant_experience",
        }

        unexpected_fields = set(self.initial_data.keys()) - expected_fields

        if unexpected_fields:
            raise serializers.ValidationError(
                {
                    "non_field_errors": [
                        "Unexpected fields: "
                        + ", ".join(sorted(unexpected_fields))
                    ]
                }
            )

        required_positive_conditions = (
            "has_passport",
            "has_academic_documents",
            "english_proficiency",
        )

        for field in required_positive_conditions:
            if attrs[field] is not True:
                raise serializers.ValidationError(
                    {field: "This onboarding requirement must be YES."}
                )

        return attrs