"""Entry point: demonstrates layered usage (repository + service)."""

from domain.models import CurrentAccount, SavingsAccount
from repositories.in_memory import InMemoryAccountRepository
from services.bank import Bank


def main() -> None:    

    repo = InMemoryAccountRepository()

    bank = Bank(repo)
    bank.add_account(SavingsAccount("Alice", 1, interest_rate=0.02))
    bank.add_account(CurrentAccount("Bob", 2, overdraft_limit=100))

    # Deposit into Alice's account (via bank we already have)
    (bank.find_account(1)).deposit(200)

    print(f"Alice balance: {(bank.find_account(1)).balance}")
    print(f"Bob balance:   {(bank.find_account(2)).balance}")

    bank.transfer(1, 2, 50)

    print("After transfer 50 from 1 -> 2:")
    print(f"Alice balance: {(bank.find_account(1)).balance}")
    print(f"Bob balance:   {(bank.find_account(2)).balance}")

    asyncio.run(main())

