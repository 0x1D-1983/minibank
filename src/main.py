"""Entry point: demonstrates layered usage (repository + service)."""

import asyncio

from domain.models import CurrentAccount, SavingsAccount
from repositories.postgres import PostgresAccountRepository
from services.bank import Bank
from services.audit_logger import AuditLogger


async def main() -> None:

    repo = PostgresAccountRepository("postgresql://admin:***REMOVED***@localhost:5432/minibank")
    bank = Bank(repo, AuditLogger())
    await bank.add_account(SavingsAccount("Alice", 1, interest_rate=0.02))
    await bank.add_account(CurrentAccount("Bob", 2, overdraft_limit=100))

    await bank.deposit(1, 200)

    print(await bank.find_account(1))
    print(await bank.find_account(2))

    await bank.transfer(1, 2, 50)

    print("After transfer 50 from 1 -> 2:")
    print(await bank.find_account(1))
    print(await bank.find_account(2))

if __name__ == "__main__":
    asyncio.run(main())