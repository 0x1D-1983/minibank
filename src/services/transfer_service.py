"""Transfer orchestration: uses repository and applies locking to avoid deadlock."""

from domain.exceptions import AccountNotFoundError
from repositories.base import AccountRepository


class TransferService:
    """Orchestrates transfers between accounts using the bank repository."""

    def __init__(self, repository: AccountRepository) -> None:
        self._repository = repository

    def transfer(
        self,
        from_account_number: int,
        to_account_number: int,
        amount: float,
    ) -> None:
        """
        Transfer amount from one account to another.
        Locks accounts in a consistent order to prevent deadlock.
        """

        from_account = self._repository.find_by_id(from_account_number)
        if from_account is None:
            raise AccountNotFoundError("Source account doesn't exist")

        to_account = self._repository.find_by_id(to_account_number)
        if to_account is None:
            raise AccountNotFoundError("Destination account doesn't exist")

        # Always acquire locks in account_number order — prevents deadlock
        first, second = sorted(
            [from_account, to_account],
            key=lambda a: a.account_number,
        )

        with first._lock:
            with second._lock:
                from_account.withdraw(amount)
                to_account.deposit(amount)