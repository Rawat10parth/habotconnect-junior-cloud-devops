from rest_framework import serializers


def validate_student_name(value):
    if not value.strip():
        raise serializers.ValidationError(
            "Student name cannot be blank."
        )

    if len(value.strip()) < 2:
        raise serializers.ValidationError(
            "Student name must contain at least 2 characters."
        )

    return value.strip()


def validate_phone(value):
    if not value.isdigit():
        raise serializers.ValidationError(
            "Phone number must contain digits only."
        )

    if len(value) != 10:
        raise serializers.ValidationError(
            "Phone number must contain exactly 10 digits."
        )

    return value


def validate_age(value):
    if value < 18 or value > 60:
        raise serializers.ValidationError(
            "Age must be between 18 and 60."
        )

    return value


def validate_dcyn(value):
    if not isinstance(value, bool):
        raise serializers.ValidationError(
            "DCYN fields must contain only true or false."
        )

    return value