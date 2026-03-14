"""Tests for Bank service."""

from domain.models import CurrentAccount, SavingsAccount
from repositories.in_memory import InMemoryAccountRepository
from services.bank import Bank as BankService
import pytest
from domain.exceptions import AccountNotFoundError, InsufficientFundsError


class TestBank:
    def test_add_and_find_account(self) -> None:
        repo = InMemoryAccountRepository()
        bank = BankService(repo)
        acc = SavingsAccount("Alice", 1, interest_rate=0.02)
        bank.add_account(acc)
        assert bank.find_account(1) is acc
        assert bank.find_account(999) is None

    def test_total_deposits(self) -> None:
        repo = InMemoryAccountRepository()
        bank = BankService(repo)
        bank.add_account(SavingsAccount("A", 1, 0.02))
        bank.add_account(CurrentAccount("B", 2, 100))
        (bank.find_account(1)).deposit(50)
        (bank.find_account(2)).deposit(30)
        assert bank.total_deposits() == 80

    def test_get_accounts_by_owner(self) -> None:
        repo = InMemoryAccountRepository()
        bank = BankService(repo)
        bank.add_account(SavingsAccount("Alice", 1, 0.02))
        bank.add_account(CurrentAccount("Alice", 2, 100))
        bank.add_account(CurrentAccount("Bob", 3, 50))
        alice_accounts = bank.get_accounts_by_owner("Alice")
        assert len(alice_accounts) == 2
        assert {a.account_number for a in alice_accounts} == {1, 2}

    def test_transfer_success(self) -> None:
        repo = InMemoryAccountRepository()
        bank = BankService(repo)
        bank.add_account(CurrentAccount("Alice", 1, 100))
        bank.add_account(CurrentAccount("Bob", 2, 50))
        (bank.find_account(1)).deposit(200)
        bank.transfer(1, 2, 50)
        assert (bank.find_account(1)).balance == 150
        assert (bank.find_account(2)).balance == 50


    def test_transfer_source_not_found(self) -> None:
        repo = InMemoryAccountRepository()
        bank = BankService(repo)
        bank.add_account(CurrentAccount("Alice", 1, 100))
        bank.add_account(CurrentAccount("Bob", 2, 50))
        # (bank.find_account(2)).deposit(100)
        with pytest.raises(AccountNotFoundError, match=r"Source account"):
            bank.transfer(999, 2, 10)


    def test_transfer_destination_not_found(self) -> None:
        repo = InMemoryAccountRepository()
        bank = BankService(repo)
        bank.add_account(CurrentAccount("Alice", 1, 100))
        bank.add_account(CurrentAccount("Bob", 2, 50))
        # (bank.find_account(1)).deposit(100)
        with pytest.raises(AccountNotFoundError, match=r"Destination account"):
            bank.transfer(1, 999, 10)


    def test_transfer_insufficient_funds_raises(self) -> None:
        repo = InMemoryAccountRepository()
        bank = BankService(repo)
        bank.add_account(SavingsAccount("Alice", 1, 0.02))
        bank.add_account(SavingsAccount("Bob", 2, 0.02))
        (bank.find_account(1)).deposit(20)
        with pytest.raises(InsufficientFundsError):
            bank.transfer(1, 2, 50)


    def test_transfer_updates_both_accounts(self) -> None:
        repo = InMemoryAccountRepository()
        bank = BankService(repo)
        bank.add_account(CurrentAccount("Alice", 1, 100))
        bank.add_account(CurrentAccount("Bob", 2, 50))
        (bank.find_account(1)).deposit(100)
        (bank.find_account(2)).deposit(25)
        bank.transfer(1, 2, 40)
        assert (bank.find_account(1)).balance == 60
        assert (bank.find_account(2)).balance == 65

