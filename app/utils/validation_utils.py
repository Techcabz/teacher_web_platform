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
    def format_file_size(size_in_bytes):
        """Convert bytes to KB, MB, or GB dynamically."""
        if size_in_bytes < 1024:
            return f"{size_in_bytes} B"
        elif size_in_bytes < 1024 * 1024:
            return f"{size_in_bytes / 1024:.2f} KB"
        elif size_in_bytes < 1024 * 1024 * 1024:
            return f"{size_in_bytes / (1024 * 1024):.2f} MB"
        else:
            return f"{size_in_bytes / (1024 * 1024 * 1024):.2f} GB"
