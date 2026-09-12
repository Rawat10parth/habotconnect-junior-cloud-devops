import unittest

from rest_framework import serializers

from student_onboarding.validators import validate_dcyn


class DCYNValidatorTests(unittest.TestCase):
    def test_true_is_accepted_as_yes(self):
        self.assertTrue(validate_dcyn(True))

    def test_false_is_accepted_as_no(self):
        self.assertFalse(validate_dcyn(False))

    def test_string_yes_is_rejected(self):
        with self.assertRaises(serializers.ValidationError):
            validate_dcyn("yes")

    def test_string_no_is_rejected(self):
        with self.assertRaises(serializers.ValidationError):
            validate_dcyn("no")

    def test_string_maybe_is_rejected(self):
        with self.assertRaises(serializers.ValidationError):
            validate_dcyn("maybe")

    def test_integer_is_rejected(self):
        with self.assertRaises(serializers.ValidationError):
            validate_dcyn(1)


if __name__ == "__main__":
    unittest.main()