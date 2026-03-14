"""Abstract repository for the Bank aggregate."""

from typing import Optional, Protocol

from domain.models import Account


class AccountRepository(Protocol):
    """Repository for loading and persisting the accounts (async)."""

    async def add_account(self, account: Account) -> None:
        """Saves an account."""
        ...

    async def find_by_id(self, account_number: int) -> Optional[Account]:
        """Finds an account by id."""
        ...

    async def find_by_owner(self, owner: str) -> list[Account]:
        """Finds accounts by owner."""
        ...

    async def all(self) -> list[Account]:
        """Returns all accounts."""
        ...

    async def update_account(self, account: Account) -> None:
        """Persists balance (and optionally other) changes for an existing account."""
        ...
