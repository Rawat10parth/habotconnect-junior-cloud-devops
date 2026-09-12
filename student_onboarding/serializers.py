from rest_framework import serializers

from .models import StudentOnboarding
from .validators import validate_phone, validate_student_name


class StrictBooleanField(serializers.BooleanField):
    """
    Accept only actual JSON boolean values: true or false.
    Strings such as "yes", "no", "true", and "false" are rejected.
    """

    def to_internal_value(self, data):
        if not isinstance(data, bool):
            self.fail("invalid")

        return data


class StudentOnboardingSerializer(serializers.ModelSerializer):
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
        max_length=10,
        validators=[validate_phone],
    )

    age = serializers.IntegerField(
        required=True,
        min_value=18,
        max_value=60,
    )

    has_passport = StrictBooleanField(required=True)

    has_academic_documents = StrictBooleanField(required=True)

    english_proficiency = StrictBooleanField(required=True)

    willing_to_relocate = StrictBooleanField(required=True)

    has_relevant_experience = StrictBooleanField(required=True)

    class Meta:
        model = StudentOnboarding
        fields = [
            "student_name",
            "email",
            "phone",
            "age",
            "has_passport",
            "has_academic_documents",
            "english_proficiency",
            "willing_to_relocate",
            "has_relevant_experience",
        ]

    def to_internal_value(self, data):
        """
        Reject fields that are not explicitly defined in the schema.
        """

        unexpected_fields = set(data.keys()) - set(self.fields.keys())

        if unexpected_fields:
            raise serializers.ValidationError(
                {
                    "non_field_errors": [
                        f"Unexpected fields: {', '.join(sorted(unexpected_fields))}"
                    ]
                }
            )

        return super().to_internal_value(data)

    def validate(self, attrs):
        """
        Final deterministic DCYN decision.

        DCYN fields must be real JSON booleans.
        String representations such as "yes", "no",
        "true", or "false" are rejected.
        """

        dcyn_fields = (
            "has_passport",
            "has_academic_documents",
            "english_proficiency",
            "willing_to_relocate",
            "has_relevant_experience",
        )

        for field in dcyn_fields:
            raw_value = self.initial_data.get(field)

            if not isinstance(raw_value, bool):
                raise serializers.ValidationError(
                    {
                        field: (
                            "DCYN value must be a JSON boolean: "
                            "true or false."
                        )
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