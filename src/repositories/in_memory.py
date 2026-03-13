from typing import Optional

from repositories.base import AccountRepository
from domain.models import Account


class InMemoryBankRepository(AccountRepository):

    def __init__(self) -> None:
        self.accounts: list[Account] = []

    def add_account(self, account: Account) -> None:
        """
            Adds a new account
        """

        self.accounts.append(account)

    def find_by_id(self, account_number: int) -> Optional[Account]:
        """
            Gets account by account number
        """

        return next((a for a in self.accounts if a.account_number == account_number), None)

    def find_by_owner(self, owner: str) -> list[Account]:
        """
            Returns all accounts owned by the given owner.
        """

        return [a for a in self.accounts if a.owner == owner]

    def all(self) -> list[Account]:
        """
            List all accounts
        """
        return self.accounts
