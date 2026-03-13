import asyncio
from dataclasses import dataclass
from datetime import datetime

from domain.models import AccountAction

@dataclass
class LogRecord:
    account_number: int
    action: AccountAction
    amount: float
    timestamp: str


class AuditLogger:
    def __init__(self) -> None:
        self.history: list[LogRecord] = []

    async def log(self, account_number: int, action: AccountAction, amount: float) -> None:
        await asyncio.sleep(0.1)

        self.history.append(LogRecord(
            account_number = account_number,
            action = action,
            amount = amount,
            timestamp = datetime.now().isoformat()
        ))

    def get_logs(self, account_number: int) -> list[LogRecord]:
        return [l for l in self.history if l.account_number == account_number]