"""In-memory implementation of BankRepository."""

from domain.models import Bank

from repositories.base import BankRepository


class InMemoryBankRepository(BankRepository):
    """Holds a single Bank in memory. save() is a no-op."""

    def __init__(self, bank: Bank | None = None) -> None:
        self._bank = bank if bank is not None else Bank()

    def get(self) -> Bank:
        return self._bank

    def save(self, bank: Bank) -> None:
        # In-memory: same instance, no persist step
        pass
