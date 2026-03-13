"""Abstract repository for the Bank aggregate."""

from typing import Optional, Protocol

from domain.models import Account


class AccountRepository(Protocol):
    """Repository for loading and persisting the accounts."""

    def add_account(self, account: Account) -> None:
        """
            Saves an account
        """

    def find_by_id(self, account_number: int) -> Optional[Account]:
        """
            Finds an account by id
        """

    def find_by_owner(self, owner: str) -> list[Account]:
        """
            Finds accounts by owner
        """

    def all(self) -> list[Account]:
        """
            Returns all accounts
        """
