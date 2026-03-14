# MiniBank Python

A small banking-style app in Python with a layered structure: domain models, async repositories, and services.

## Structure

```
src/
├── domain/
│   ├── __init__.py
│   ├── models.py       # Account (abstract), SavingsAccount, CurrentAccount, AccountAction, __str__
│   └── exceptions.py   # InsufficientFundsError, AccountNotFoundError, InvalidAmountError, OverdraftError
├── repositories/
│   ├── __init__.py
│   ├── base.py         # AccountRepository protocol (async)
│   ├── in_memory.py    # InMemoryAccountRepository
│   └── postgres.py     # PostgresAccountRepository (asyncpg)
├── services/
│   ├── __init__.py
│   ├── bank.py         # Bank (async: add_account, find_account, deposit, withdraw, transfer, total_deposits, get_accounts_by_owner)
│   └── audit_logger.py # AuditLogger, LogRecord
├── __init__.py
└── main.py             # Entry point (async)

sql/
└── db-schema.sql       # PostgreSQL schema (accounts, account_transactions)

tests/
├── __init__.py
├── conftest.py         # Shared fixtures
├── test_domain_models.py  # SavingsAccount, CurrentAccount
├── test_bank.py        # Bank (async tests; transfer, exceptions)
└── test_audit_logger.py   # AuditLogger
```

- **Domain**: Account types and exceptions.
- **Repositories**: Async `AccountRepository`; in-memory and PostgreSQL (asyncpg) implementations. Use `update_account` after balance changes for persistence.
- **Services**: `Bank` (async API) and `AuditLogger`.

## Run

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt
PYTHONPATH=src python3 src/main.py
```

`main.py` uses `PostgresAccountRepository` by default, so PostgreSQL must be running and the schema applied (see Database). To run without a DB, switch to `InMemoryAccountRepository` in `main.py`.

## Database

1. Create a database and run the schema:

   ```bash
   psql -h localhost -U your_user -d minibank -f sql/db-schema.sql
   ```

2. Configure the DSN in code, e.g.:

   ```python
   repo = PostgresAccountRepository("postgresql://user:password@localhost:5432/minibank")
   ```

3. Optionally close the pool on shutdown: `await repo.close()`.

## Tests

```bash
pip install -r requirements-dev.txt
PYTHONPATH=src python3 -m pytest tests/ -v
```

Uses `pytest-asyncio` with `asyncio_mode = auto` (see `pytest.ini`). Bank tests are async and use the in-memory repository.

## Requirements

- Python 3.10+
- **Runtime**: `asyncpg` (see `requirements.txt`)
- **Dev**: `pytest`, `pytest-asyncio` (see `requirements-dev.txt`)
