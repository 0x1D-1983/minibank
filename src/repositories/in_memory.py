from typing import Optional

from domain.models import Account
from repositories.base import AccountRepository


class InMemoryAccountRepository(AccountRepository):
    def __init__(self) -> None:
        self.accounts: list[Account] = []

    async def add_account(self, account: Account) -> None:
        self.accounts.append(account)

    async def find_by_id(self, account_number: int) -> Optional[Account]:
        return next((a for a in self.accounts if a.account_number == account_number), None)

    async def find_by_owner(self, owner: str) -> list[Account]:
        return [a for a in self.accounts if a.owner == owner]

    async def all(self) -> list[Account]:
        return self.accounts

    async def update_account(self, account: Account) -> None:
        pass  # in-memory account is already the live object
