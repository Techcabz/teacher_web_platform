import re

class Validation:
    @staticmethod
    def is_valid_name(name):
        """Check if the name contains only alphabetic characters."""
        name_pattern = r"^[A-Za-z\s]+$"  # Allow spaces
        return bool(re.match(name_pattern, name))

    @staticmethod
    def has_repeated_characters(name, threshold=3):
        """Check if the name has three or more consecutive repeated characters."""
        return bool(re.search(r"(.)\1{" + str(threshold - 1) + r",}", name))

    @staticmethod
    def is_valid_number(value):
        """Check if the value is a positive integer."""
        return value.isdigit() and int(value) > 0

    @staticmethod
    def is_strong_password(password):
        """
        Check if the password is strong:
        - At least 8 characters long
        - Contains at least one uppercase letter
        - Contains at least one lowercase letter
        - Contains at least one digit
        - Contains at least one special character (@, #, $, etc.)
        """
        password_pattern = (
            r"^(?=.*[A-Z])"       # At least one uppercase letter
            r"(?=.*[a-z])"        # At least one lowercase letter
            r"(?=.*\d)"           # At least one digit
            r"(?=.*[@$!%*?&])"    # At least one special character
            r"[A-Za-z\d@$!%*?&]{8,}$"  # Minimum 8 characters
        )
        return bool(re.match(password_pattern, password))
