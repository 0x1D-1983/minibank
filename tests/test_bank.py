"""Tests for Bank service."""

from domain.models import CurrentAccount, SavingsAccount
from repositories.in_memory import InMemoryBankRepository
from services.bank import Bank as BankService


class TestBank:
    def test_add_and_find_account(self) -> None:
        repo = InMemoryBankRepository()
        bank = BankService(repo)
        acc = SavingsAccount("Alice", 1, interest_rate=0.02)
        bank.add_account(acc)
        assert bank.find_account(1) is acc
        assert bank.find_account(999) is None

    def test_total_deposits(self) -> None:
        repo = InMemoryBankRepository()
        bank = BankService(repo)
        bank.add_account(SavingsAccount("A", 1, 0.02))
        bank.add_account(CurrentAccount("B", 2, 100))
        (bank.find_account(1)).deposit(50)
        (bank.find_account(2)).deposit(30)
        assert bank.total_deposits() == 80

    def test_get_accounts_by_owner(self) -> None:
        repo = InMemoryBankRepository()
        bank = BankService(repo)
        bank.add_account(SavingsAccount("Alice", 1, 0.02))
        bank.add_account(CurrentAccount("Alice", 2, 100))
        bank.add_account(CurrentAccount("Bob", 3, 50))
        alice_accounts = bank.get_accounts_by_owner("Alice")
        assert len(alice_accounts) == 2
        assert {a.account_number for a in alice_accounts} == {1, 2}
