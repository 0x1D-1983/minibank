# MiniBank Python

A small banking-style app in Python with a layered structure: domain models, repositories, and services.

## Structure

```
src/
├── domain/
│   ├── __init__.py
│   ├── models.py       # Account (abstract), SavingsAccount, CurrentAccount, AccountAction
│   └── exceptions.py   # InsufficientFundsError, AccountNotFoundError, InvalidAmountError, OverdraftError
├── repositories/
│   ├── __init__.py
│   ├── base.py         # AccountRepository protocol
│   └── in_memory.py    # InMemoryAccountRepository
├── services/
│   ├── __init__.py
│   ├── bank.py         # Bank (add_account, find_account, transfer, total_deposits, get_accounts_by_owner)
│   └── audit_logger.py # AuditLogger, LogRecord
├── __init__.py
└── main.py             # Entry point

tests/
├── __init__.py
├── conftest.py         # Shared fixtures
├── test_domain_models.py  # SavingsAccount, CurrentAccount
├── test_bank.py        # Bank (including transfer)
└── test_audit_logger.py  # AuditLogger
```

- **Domain**: Account types and exceptions.
- **Repositories**: `AccountRepository` protocol and `InMemoryAccountRepository`.
- **Services**: `Bank` (accounts + transfer with lock ordering) and `AuditLogger`.

## Run

From the project root:

```bash
# Optional: use a virtual environment
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Run (PYTHONPATH so imports resolve)
PYTHONPATH=src python3 src/main.py
```

## Tests

```bash
pip install -r requirements-dev.txt
PYTHONPATH=src python3 -m pytest tests/ -v
```

## Requirements

- Python 3.10+ (uses `|` for union types in type hints).
