"""Tests for domain models: Account types and Bank."""

import pytest

from domain.exceptions import (
    InsufficientFundsError,
    InvalidAmountError,
    OverdraftError,
)
from domain.models import Bank, CurrentAccount, SavingsAccount


class TestSavingsAccount:
    def test_deposit_increases_balance(self) -> None:
        acc = SavingsAccount("Alice", 1, interest_rate=0.02)
        acc.deposit(100)
        assert acc.balance == 100

    def test_deposit_negative_raises(self) -> None:
        acc = SavingsAccount("Alice", 1, interest_rate=0.02)
        with pytest.raises(InvalidAmountError):
            acc.deposit(-10)
        with pytest.raises(InvalidAmountError):
            acc.deposit(0)

    def test_withdraw_decreases_balance(self) -> None:
        acc = SavingsAccount("Alice", 1, interest_rate=0.02)
        acc.deposit(100)
        acc.withdraw(30)
        assert acc.balance == 70

    def test_withdraw_more_than_balance_raises(self) -> None:
        acc = SavingsAccount("Alice", 1, interest_rate=0.02)
        acc.deposit(50)
        with pytest.raises(InsufficientFundsError):
            acc.withdraw(60)

    def test_withdraw_negative_raises(self) -> None:
        acc = SavingsAccount("Alice", 1, interest_rate=0.02)
        with pytest.raises(InvalidAmountError):
            acc.withdraw(-5)

    def test_apply_interest(self) -> None:
        acc = SavingsAccount("Alice", 1, interest_rate=0.10)
        acc.deposit(100)
        acc.apply_interest()
        assert acc.balance == 110


class TestCurrentAccount:
    def test_withdraw_within_overdraft(self) -> None:
        acc = CurrentAccount("Bob", 2, overdraft_limit=100)
        acc.deposit(20)
        acc.withdraw(50)
        assert acc.balance == -30

    def test_withdraw_exceeds_overdraft_raises(self) -> None:
        acc = CurrentAccount("Bob", 2, overdraft_limit=50)
        acc.deposit(10)
        with pytest.raises(OverdraftError):
            acc.withdraw(70)

    def test_deposit_negative_raises(self) -> None:
        acc = CurrentAccount("Bob", 2, overdraft_limit=100)
        with pytest.raises(InvalidAmountError):
            acc.deposit(0)


class TestBank:
    def test_add_and_find_account(self) -> None:
        bank = Bank()
        acc = SavingsAccount("Alice", 1, interest_rate=0.02)
        bank.add_account(acc)
        assert bank.find_account(1) is acc
        assert bank.find_account(999) is None

    def test_total_deposits(self) -> None:
        bank = Bank()
        bank.add_account(SavingsAccount("A", 1, 0.02))
        bank.add_account(CurrentAccount("B", 2, 100))
        bank.find_account(1).deposit(50)
        bank.find_account(2).deposit(30)
        assert bank.total_deposits() == 80

    def test_get_accounts_by_owner(self) -> None:
        bank = Bank()
        bank.add_account(SavingsAccount("Alice", 1, 0.02))
        bank.add_account(CurrentAccount("Alice", 2, 100))
        bank.add_account(CurrentAccount("Bob", 3, 50))
        alice_accounts = bank.get_accounts_by_owner("Alice")
        assert len(alice_accounts) == 2
        assert {a.account_number for a in alice_accounts} == {1, 2}
