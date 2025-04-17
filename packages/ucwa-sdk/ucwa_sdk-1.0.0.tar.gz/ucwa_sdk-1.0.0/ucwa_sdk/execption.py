class UCWAError(Exception):
    """Base exception for UCWA SDK"""
    pass

class AuthenticationError(UCWAError):
    pass

class RateLimitError(UCWAError):
    pass

class NotFoundError(UCWAError):
    pass

class ServerError(UCWAError):
    pass
