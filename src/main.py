"""Entry point: demonstrates layered usage (repository + service)."""

import asyncio

from domain.models import CurrentAccount, SavingsAccount
from repositories.in_memory import InMemoryAccountRepository
from services.bank import Bank
from services.audit_logger import AuditLogger


async def main() -> None:

    repo = InMemoryAccountRepository()

    bank = Bank(repo, AuditLogger())
    bank.add_account(SavingsAccount("Alice", 1, interest_rate=0.02))
    bank.add_account(CurrentAccount("Bob", 2, overdraft_limit=100))

    # Deposit into Alice's account (via bank we already have)
    await bank.deposit(1, 200)

    print(f"{bank.find_account(1)}")
    print(f"{bank.find_account(2)}")

    await bank.transfer(1, 2, 50)

    print("After transfer 50 from 1 -> 2:")
    print(f"{bank.find_account(1)}")
    print(f"{bank.find_account(2)}")

if __name__ == "__main__":
    asyncio.run(main())