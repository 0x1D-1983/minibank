from abc import ABC, abstractmethod
from enum import Enum
import threading
from typing import Optional

from domain.exceptions import (
    InsufficientFundsError,
    InvalidAmountError,
    OverdraftError,
)

class AccountAction(Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"
    INTEREST = "INTEREST"
    TRANSFER = "TRANSFER"


class Account(ABC):

    def __init__(self, owner: str, account_number: int) -> None:
        self.owner: str = owner
        self.account_number: int = account_number
        self._balance: float = 0
        self.history: list[str] = []
        self._lock: threading.RLock = threading.RLock()

    @property
    def balance(self) -> float:
        with self._lock:
            return self._balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise InvalidAmountError(f"Deposit amount must be positive, got {amount}")
        
        with self._lock:
            self._balance += amount
            self.history.append(f"{AccountAction.DEPOSIT.value}: +{amount:.2f}")
    
    @abstractmethod
    def withdraw(self, amount: float) -> None:
        ...

class SavingsAccount(Account):
    interest_rate: float

    def __init__(self, owner: str, account_number: int, interest_rate: float) -> None:
        super().__init__(owner, account_number)
        self.interest_rate = interest_rate
    
    def withdraw(self, amount: float) -> None:
        """
            Withdraws amount
        """

        if amount <= 0:
            raise InvalidAmountError(f"Withdrawal amount must be positive, got {amount}")

        with self._lock:
            if self._balance >= amount:
                self._balance -= amount
                self.history.append(f"{AccountAction.WITHDRAW.value}: -{amount:.2f}")
            else:
                raise InsufficientFundsError("Insufficient balance")
    
    def apply_interest(self) -> None:
        with self._lock:
            interest = self._balance * self.interest_rate
            self._balance += interest
            self.history.append(f"{AccountAction.INTEREST.value}: +{interest:.2f}")

class CurrentAccount(Account):
    overdraft_limit: float

    def __init__(self, owner: str, account_number: int, overdraft_limit: float) -> None:
        super().__init__(owner, account_number)
        self.overdraft_limit = overdraft_limit
    
    def withdraw(self, amount: float) -> None:
        """
            Withdraws amount with overdraft
        """

        if amount <= 0:
            raise InvalidAmountError(f"Withdrawal amount must be positive, got {amount}")

        with self._lock:
            if self._balance + self.overdraft_limit >= amount:
                self._balance -= amount
                self.history.append(f"{AccountAction.WITHDRAW.value}: -{amount:.2f}")
            else:
                raise OverdraftError("Overdraft limit exceeded")
        
class Bank:
    accounts: list[Account]

    def __init__(self) -> None:
        self.accounts = []

    def add_account(self, account: Account) -> None:
        """
            Adds a new account
        """

        self.accounts.append(account)

    def find_account(self, account_number: int) -> Optional[Account]:
        """
            Gets account by account number
        """

        return next((a for a in self.accounts if a.account_number == account_number), None)
    
    def total_deposits(self) -> float:
        """
            Gets the total balance across all accounts at the bank
        """

        return sum(a.balance for a in self.accounts)
    
    def get_accounts_by_owner(self, owner: str) -> list[Account]:
        """Returns all accounts owned by the given owner."""
        return [a for a in self.accounts if a.owner == owner]
