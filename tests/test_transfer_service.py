"""Tests for TransferService."""

import pytest

from domain.exceptions import AccountNotFoundError, InsufficientFundsError
from domain.models import CurrentAccount, SavingsAccount
from repositories.in_memory import InMemoryBankRepository
from services.transfer_service import TransferService
from services.bank import Bank as BankService


def test_transfer_success(transfer_service: TransferService, bank: BankService) -> None:
    (bank.find_account(1)).deposit(200)
    transfer_service.transfer(1, 2, 50)
    assert (bank.find_account(1)).balance == 150
    assert (bank.find_account(2)).balance == 50


def test_transfer_source_not_found(transfer_service: TransferService, bank: BankService) -> None:
    (bank.find_account(2)).deposit(100)
    with pytest.raises(AccountNotFoundError, match="Source account"):
        transfer_service.transfer(999, 2, 10)


def test_transfer_destination_not_found(
    transfer_service: TransferService, bank: BankService
) -> None:
    (bank.find_account(1)).deposit(100)
    with pytest.raises(AccountNotFoundError, match="Destination account"):
        transfer_service.transfer(1, 999, 10)


def test_transfer_insufficient_funds_raises(
    transfer_service: TransferService, bank: BankService
) -> None:
    (bank.find_account(1)).deposit(20)
    with pytest.raises(InsufficientFundsError):
        transfer_service.transfer(1, 2, 50)


def test_transfer_updates_both_accounts(transfer_service: TransferService, bank: BankService) -> None:
    (bank.find_account(1)).deposit(100)
    (bank.find_account(2)).deposit(25)
    transfer_service.transfer(1, 2, 40)
    assert (bank.find_account(1)).balance == 60
    assert (bank.find_account(2)).balance == 65
