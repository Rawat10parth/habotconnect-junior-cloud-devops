from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class StudentOnboarding(models.Model):
    student_name = models.CharField(
        max_length=100,
    )

    email = models.EmailField(
        max_length=254,
    )

    phone = models.CharField(
        max_length=10,
    )

    age = models.IntegerField(
        validators=[
            MinValueValidator(18),
            MaxValueValidator(60),
        ]
    )

    has_passport = models.BooleanField()

    has_academic_documents = models.BooleanField()

    english_proficiency = models.BooleanField()

    willing_to_relocate = models.BooleanField()

    has_relevant_experience = models.BooleanField()

    class Meta:
        app_label = "student_onboarding"