"""PostgreSQL implementation of AccountRepository using asyncpg."""

from typing import Optional

import asyncpg

from domain.models import Account, CurrentAccount, SavingsAccount
from repositories.base import AccountRepository


def _row_to_account(row: asyncpg.Record) -> Account:
    """Map a DB row to a domain Account (SavingsAccount or CurrentAccount)."""
    account_number = int(row["account_number"])
    owner = row["owner"]
    balance = float(row["balance"])
    if row["type"] == "savings":
        acc = SavingsAccount(owner, account_number, interest_rate=float(row["interest_rate"]))
    else:
        acc = CurrentAccount(owner, account_number, overdraft_limit=float(row["overdraft_limit"]))
    acc._balance = balance
    return acc


class PostgresAccountRepository(AccountRepository):
    """Persists accounts to PostgreSQL using the accounts table (async)."""

    def __init__(self, dsn: str) -> None:
        """
        Args:
            dsn: Connection string, e.g. "postgresql://user:password@localhost:5432/minibank"
        """
        self._dsn = dsn
        self._pool: Optional[asyncpg.Pool] = None

    async def _get_pool(self) -> asyncpg.Pool:
        if self._pool is None:
            self._pool = await asyncpg.create_pool(self._dsn, min_size=1, max_size=10)
        return self._pool

    async def close(self) -> None:
        """Close the connection pool. Call when shutting down."""
        if self._pool is not None:
            await self._pool.close()
            self._pool = None

    async def add_account(self, account: Account) -> None:
        if isinstance(account, SavingsAccount):
            type_val = "savings"
            interest_rate = account.interest_rate
            overdraft_limit = None
        elif isinstance(account, CurrentAccount):
            type_val = "current"
            interest_rate = None
            overdraft_limit = account.overdraft_limit
        else:
            raise TypeError(f"Unknown account type: {type(account)}")

        pool = await self._get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO accounts (account_number, owner, type, balance, interest_rate, overdraft_limit)
                VALUES ($1, $2, $3, $4, $5, $6)
                """,
                account.account_number,
                account.owner,
                type_val,
                account.balance,
                interest_rate,
                overdraft_limit,
            )

    async def find_by_id(self, account_number: int) -> Optional[Account]:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT account_number, owner, type, balance, interest_rate, overdraft_limit
                FROM accounts WHERE account_number = $1
                """,
                account_number,
            )
        if row is None:
            return None
        return _row_to_account(row)

    async def find_by_owner(self, owner: str) -> list[Account]:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT account_number, owner, type, balance, interest_rate, overdraft_limit
                FROM accounts WHERE owner = $1
                """,
                owner,
            )
        return [_row_to_account(row) for row in rows]

    async def all(self) -> list[Account]:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT account_number, owner, type, balance, interest_rate, overdraft_limit
                FROM accounts
                """
            )
        return [_row_to_account(row) for row in rows]

    async def update_account(self, account: Account) -> None:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE accounts SET balance = $1, updated_at = NOW()
                WHERE account_number = $2
                """,
                account.balance,
                account.account_number,
            )
