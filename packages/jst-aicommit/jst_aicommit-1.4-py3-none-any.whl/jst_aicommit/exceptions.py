class JstException(Exception):
    """Base class for all exceptions in the JST library."""

    ERROR_MATCH = 1000

    def __init__(self, message, code=None):
        """Initialize the exception with a message and optional code (default is None)."""
        self.message = message
        self.code = code