# MiniBank Python

A small banking-style app in Python with a layered structure: domain models, repositories, and services.

## Structure

```
src/
├── domain/
│   ├── models.py      # Account (abstract), SavingsAccount, CurrentAccount, AccountAction
│   ├── exceptions.py  # InsufficientFundsError, AccountNotFoundError, InvalidAmountError, OverdraftError
│   └── logger.py      # AuditLogger, LogRecord
├── repositories/
│   ├── base.py        # AccountRepository protocol
│   └── in_memory.py   # InMemoryBankRepository
├── services/
│   ├── bank.py        # Bank (add_account, find_account, total_deposits, get_accounts_by_owner)
│   └── transfer_service.py  # TransferService (orchestration + locking)
└── main.py            # Entry point

tests/
├── conftest.py           # Shared fixtures (bank, repo, transfer_service)
├── test_domain_models.py # Account types (SavingsAccount, CurrentAccount)
├── test_bank.py         # Bank service
├── test_transfer_service.py  # TransferService
└── test_audit_logger.py # AuditLogger
```

- **Domain**: Account types, exceptions, and audit logging.
- **Repositories**: `AccountRepository` protocol and in-memory implementation.
- **Services**: `Bank` (account lookup/aggregation) and `TransferService` (transfers with lock ordering).

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
