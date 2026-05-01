class Validators:
    @staticmethod
    def validate_email(email: str) -> bool:
        import re
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(email_regex, email) is not None

    @staticmethod
    def validate_password(password: str) -> bool:
        import re
        password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$'
        return re.match(password_regex, password) is not None