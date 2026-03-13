"""Entry point: demonstrates layered usage (repository + service)."""

from domain.models import CurrentAccount, SavingsAccount
from repositories.in_memory import InMemoryBankRepository
from services.bank import Bank
from services.transfer_service import TransferService


def main() -> None:    

    repo = InMemoryBankRepository()
    transfer_service = TransferService(repo)

    bank = Bank(repo)
    bank.add_account(SavingsAccount("Alice", 1, interest_rate=0.02))
    bank.add_account(CurrentAccount("Bob", 2, overdraft_limit=100))

    # Deposit into Alice's account (via bank we already have)
    (bank.find_by_id(1)).deposit(200)

    print(f"Alice balance: {(bank.find_by_id(1)).balance}")
    print(f"Bob balance:   {(bank.find_by_id(2)).balance}")

    transfer_service.transfer(1, 2, 50)

    print("After transfer 50 from 1 -> 2:")
    print(f"Alice balance: {(bank.find_by_id(1)).balance}")
    print(f"Bob balance:   {(bank.find_by_id(2)).balance}")

    asyncio.run(main())

