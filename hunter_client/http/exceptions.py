"""Custom exceptions for API client."""


class HunterAPIError(Exception):
    """Base exception for Hunter API failures."""


class HunterHTTPError(HunterAPIError):
    """HTTP level failure."""
