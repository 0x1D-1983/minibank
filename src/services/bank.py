from typing import Optional

from domain.models import Account, AccountAction
from repositories.base import AccountRepository
from domain.exceptions import AccountNotFoundError
from services.audit_logger import AuditLogger


class Bank:
    def __init__(self, account_repo: AccountRepository, logger: AuditLogger) -> None:
        self._accounts = account_repo
        self._logger = logger

    async def add_account(self, account: Account) -> None:
        await self._accounts.add_account(account)

    async def find_account(self, account_number: int) -> Optional[Account]:
        return await self._accounts.find_by_id(account_number)

    async def total_deposits(self) -> float:
        accounts = await self._accounts.all()
        return sum(a.balance for a in accounts)

    async def get_accounts_by_owner(self, owner: str) -> list[Account]:
        return await self._accounts.find_by_owner(owner)
    
    async def deposit(self, account_number: int, amount: float) -> None:
        """
            Deposit amount
        """

        account = await self.find_account(account_number)
        if account is None:
            raise AccountNotFoundError("Account doesn't exist")
        account.deposit(amount)
        await self._accounts.update_account(account)
        await self._logger.log(account_number, AccountAction.DEPOSIT, amount)

    async def withdraw(self, account_number: int, amount: float) -> None:
        """
            Withdraw amount
        """

        account = await self.find_account(account_number)
        if account is None:
            raise AccountNotFoundError("Account doesn't exist")
        account.withdraw(amount)
        await self._accounts.update_account(account)
        await self._logger.log(account_number, AccountAction.WITHDRAW, amount)

    async def transfer(
        self,
        from_account_number: int,
        to_account_number: int,
        amount: float,
    ) -> None:
        """
        Transfer amount from one account to another.
        Locks accounts in a consistent order to prevent deadlock.
        """

        from_account = await self.find_account(from_account_number)
        if from_account is None:
            raise AccountNotFoundError("Source account doesn't exist")
        to_account = await self.find_account(to_account_number)
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
        await self._accounts.update_account(from_account)
        await self._accounts.update_account(to_account)
        await self._logger.log(from_account_number, AccountAction.TRANSFER, -amount)
        await self._logger.log(to_account_number, AccountAction.TRANSFER, amount)
