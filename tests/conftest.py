"""Pytest fixtures shared across tests."""

import pytest

from domain.models import CurrentAccount, SavingsAccount
from repositories.in_memory import InMemoryAccountRepository
from services.transfer_service import TransferService
from services.bank import Bank


@pytest.fixture
def bank() -> Bank:
    """Bank with two accounts: savings (1) and current (2)."""
    b = Bank(InMemoryAccountRepository())
    b.add_account(SavingsAccount("Alice", 1, interest_rate=0.02))
    b.add_account(CurrentAccount("Bob", 2, overdraft_limit=100))
    return b


@pytest.fixture
def repo(bank: Bank) -> InMemoryAccountRepository:
    """In-memory repository with the default bank."""
    return bank.accounts


@pytest.fixture
def transfer_service(repo: InMemoryAccountRepository) -> TransferService:
    """Transfer service using the in-memory repo."""
    return TransferService(repo)
