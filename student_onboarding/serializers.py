from rest_framework import serializers

from .validators import (
    validate_age,
    validate_dcyn,
    validate_phone,
    validate_student_name,
)


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

    has_passport = serializers.BooleanField(
        required=True,
        validators=[validate_dcyn],
    )

    has_academic_documents = serializers.BooleanField(
        required=True,
        validators=[validate_dcyn],
    )

    english_proficiency = serializers.BooleanField(
        required=True,
        validators=[validate_dcyn],
    )

    willing_to_relocate = serializers.BooleanField(
        required=True,
        validators=[validate_dcyn],
    )

    has_relevant_experience = serializers.BooleanField(
        required=True,
        validators=[validate_dcyn],
    )

    def validate(self, attrs):
        """
        Final deterministic DCYN decision.

        All mandatory onboarding conditions must be satisfied.
        """
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