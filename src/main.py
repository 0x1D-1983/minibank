"""Entry point: demonstrates layered usage (repository + service)."""

from domain.models import Bank, CurrentAccount, SavingsAccount
from repositories.in_memory import InMemoryBankRepository
from services.transfer_service import TransferService


def main() -> None:
    bank = Bank()
    bank.add_account(SavingsAccount("Alice", 1, interest_rate=0.02))
    bank.add_account(CurrentAccount("Bob", 2, overdraft_limit=100))

    repo = InMemoryBankRepository(bank)
    transfer_service = TransferService(repo)

    # Deposit into Alice's account (via bank we already have)
    bank.find_account(1).deposit(200)

    print(f"Alice balance: {bank.find_account(1).balance}")
    print(f"Bob balance:   {bank.find_account(2).balance}")

    transfer_service.transfer(1, 2, 50)

    print("After transfer 50 from 1 -> 2:")
    print(f"Alice balance: {bank.find_account(1).balance}")
    print(f"Bob balance:   {bank.find_account(2).balance}")


if __name__ == "__main__":
    main()
