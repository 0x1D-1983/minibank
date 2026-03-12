"""Abstract repository for the Bank aggregate."""

from typing import Protocol

from domain.models import Bank


class BankRepository(Protocol):
    """Repository for loading and persisting the Bank aggregate."""

    def get(self) -> Bank:
        """Return the bank (with all accounts)."""
        ...

    def save(self, bank: Bank) -> None:
        """Persist the bank state."""
        ...
