class TokenExpiredException(Exception):
    def __init__(self, message: str = "Token expired"):
        self.message = message
        super().__init__(self.message)
