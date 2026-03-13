from typing import Optional

from domain.models import Account
from repositories.base import AccountRepository


class Bank:
    def __init__(self, account_repo: AccountRepository) -> None:
        self.accounts = account_repo

    def add_account(self, account: Account) -> None:
        """
            Adds a new account
        """

        self.accounts.add_account(account)

    def find_account(self, account_number: int) -> Optional[Account]:
        """
            Gets account by account number
        """

        return self.accounts.find_by_id(account_number)
    
    def total_deposits(self) -> float:
        """
            Gets the total balance across all accounts at the bank
        """

        return sum(a.balance for a in self.accounts.all())
    
    def get_accounts_by_owner(self, owner: str) -> list[Account]:
        """
            Returns all accounts owned by the given owner.
        """
        
        return self.accounts.find_by_owner(owner)
