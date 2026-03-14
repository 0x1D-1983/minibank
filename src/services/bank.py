from typing import Optional

from domain.models import Account
from repositories.base import AccountRepository
from domain.exceptions import AccountNotFoundError


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

    def transfer(
        self,
        from_account_number: int,
        to_account_number: int,
        amount: float,
    ) -> None:
        """
        Transfer amount from one account to another.
        Locks accounts in a consistent order to prevent deadlock.
        """

        from_account = self.find_account(from_account_number)
        if from_account is None:
            raise AccountNotFoundError("Source account doesn't exist")

        to_account = self.find_account(to_account_number)
        if to_account is None:
            raise AccountNotFoundError("Destination account doesn't exist")

        # Always acquire locks in account_number order — prevents deadlock
        first, second = sorted(
            [from_account, to_account],
            key=lambda a: a.account_number,
        )

        with first._lock:
            with second._lock:
                from_account.withdraw(amount)
                to_account.deposit(amount)
