"""Tests for Bank service."""

import pytest

from domain.exceptions import AccountNotFoundError, InsufficientFundsError
from domain.models import CurrentAccount, SavingsAccount
from repositories.in_memory import InMemoryAccountRepository
from services.audit_logger import AuditLogger
from services.bank import Bank


@pytest.fixture
def bank() -> Bank:
    """Fresh bank with repo and audit logger for each test."""
    repo = InMemoryAccountRepository()
    audit_logger = AuditLogger()
    return Bank(repo, audit_logger)


class TestBank:
    async def test_add_and_find_account(self, bank: Bank) -> None:
        acc = SavingsAccount("Alice", 1, interest_rate=0.02)
        await bank.add_account(acc)
        assert (await bank.find_account(1)) is acc
        assert (await bank.find_account(999)) is None

    async def test_total_deposits(self, bank: Bank) -> None:
        await bank.add_account(SavingsAccount("A", 1, 0.02))
        await bank.add_account(CurrentAccount("B", 2, 100))
        (await bank.find_account(1)).deposit(50)
        (await bank.find_account(2)).deposit(30)
        assert (await bank.total_deposits()) == 80

    async def test_get_accounts_by_owner(self, bank: Bank) -> None:
        await bank.add_account(SavingsAccount("Alice", 1, 0.02))
        await bank.add_account(CurrentAccount("Alice", 2, 100))
        await bank.add_account(CurrentAccount("Bob", 3, 50))
        alice_accounts = await bank.get_accounts_by_owner("Alice")
        assert len(alice_accounts) == 2
        assert {a.account_number for a in alice_accounts} == {1, 2}

    async def test_transfer_success(self, bank: Bank) -> None:
        await bank.add_account(CurrentAccount("Alice", 1, 100))
        await bank.add_account(CurrentAccount("Bob", 2, 50))
        (await bank.find_account(1)).deposit(200)
        await bank.transfer(1, 2, 50)
        assert (await bank.find_account(1)).balance == 150
        assert (await bank.find_account(2)).balance == 50

    async def test_transfer_source_not_found(self, bank: Bank) -> None:
        await bank.add_account(CurrentAccount("Alice", 1, 100))
        await bank.add_account(CurrentAccount("Bob", 2, 50))
        with pytest.raises(AccountNotFoundError, match=r"Source account"):
            await bank.transfer(999, 2, 10)

    async def test_transfer_destination_not_found(self, bank: Bank) -> None:
        await bank.add_account(CurrentAccount("Alice", 1, 100))
        await bank.add_account(CurrentAccount("Bob", 2, 50))
        with pytest.raises(AccountNotFoundError, match=r"Destination account"):
            await bank.transfer(1, 999, 10)

    async def test_transfer_insufficient_funds_raises(self, bank: Bank) -> None:
        await bank.add_account(SavingsAccount("Alice", 1, 0.02))
        await bank.add_account(SavingsAccount("Bob", 2, 0.02))
        (await bank.find_account(1)).deposit(20)
        with pytest.raises(InsufficientFundsError):
            await bank.transfer(1, 2, 50)

    async def test_transfer_updates_both_accounts(self, bank: Bank) -> None:
        await bank.add_account(CurrentAccount("Alice", 1, 100))
        await bank.add_account(CurrentAccount("Bob", 2, 50))
        (await bank.find_account(1)).deposit(100)
        (await bank.find_account(2)).deposit(25)
        await bank.transfer(1, 2, 40)
        assert (await bank.find_account(1)).balance == 60
        assert (await bank.find_account(2)).balance == 65

