class User:
    def __init__(self, email, password, pix_key) -> None:
        self.email = email
        self.password = password
        self.pix_key = pix_key

    def __str__(self) -> str:
        return f"USER - email={self.email}, password={self.password}, pix_key={self.pix_key}"