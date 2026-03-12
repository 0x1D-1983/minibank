"""Domain exceptions for MiniBank."""


class InsufficientFundsError(Exception):
    """Raised when withdrawal would exceed account balance (no overdraft)."""
    pass


class AccountNotFoundError(Exception):
    """Raised when an account does not exist."""
    pass


class InvalidAmountError(Exception):
    """Raised when an amount is not valid (e.g. non-positive)."""
    pass


class OverdraftError(Exception):
    """Raised when withdrawal would exceed overdraft limit."""
    pass
