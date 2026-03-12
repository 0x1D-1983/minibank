from abc import ABC, abstractmethod
import threading
from typing import Optional

class InsufficientFundsError(Exception):
    pass

class AccountNotFoundError(Exception):
    pass

class InvalidAmountError(Exception):
    """Raised when an amount is not valid (e.g. non-positive)."""
    pass

class OverdraftError(Exception):
    pass

class Account(ABC):
    owner: str
    account_number: int
    _balance: float
    history: list[str]
    _lock: threading.RLock

    def __init__(self, owner: str, account_number: int) -> None:
        self.owner = owner
        self.account_number = account_number
        self._balance = 0
        self.history = []
        self._lock = threading.RLock()

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise InvalidAmountError(f"Deposit amount must be positive, got {amount}")
        
        with self._lock:
            self._balance += amount
            self.history.append(f"DEPOSIT: +{amount:.2f}")
    
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
                self.history.append(f"WITHDRAW: -{amount:.2f}")
            else:
                raise InsufficientFundsError("Insufficient balance")
    
    def apply_interest(self) -> None:
        with self._lock:
            interest = self._balance * self.interest_rate
            self._balance += interest
            self.history.append(f"INTEREST: +{interest:.2f}")

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
                self.history.append(f"WITHDRAW: -{amount:.2f}")
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
        """
            Gets account by owner name
        """

        return [a for a in self.accounts if a.owner == owner]
    
    def transfer(self, from_account_number: int, to_account_number: int, amount: float) -> None:
        """
            Transfers funds from a source account to a destination account
        """

        from_account = self.find_account(from_account_number)
        if from_account is None:
            raise AccountNotFoundError("Source account doesn't exist")
        
        to_account = self.find_account(to_account_number)
        if to_account is None:
            raise AccountNotFoundError("Destination account doesn't exist")
        
        # Always acquire locks in account_number order — prevents deadlock
        first, second = sorted([from_account, to_account], key=lambda a: a.account_number)

        with first._lock:
            with second._lock:
                from_account.withdraw(amount) # if this fails it throws an exception so it won't continue to destination account
                to_account.deposit(amount)
