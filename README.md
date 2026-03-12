# MiniBank Python

A small banking-style app in Python with a layered structure: domain models, repositories, and services.

## Structure

```
src/
├── domain/
│   ├── models.py      # Account (abstract), SavingsAccount, CurrentAccount, Bank
│   └── exceptions.py  # InsufficientFundsError, AccountNotFoundError, etc.
├── repositories/
│   ├── base.py        # BankRepository protocol
│   └── in_memory.py   # InMemoryBankRepository
├── services/
│   └── transfer_service.py  # TransferService (orchestration + locking)
└── main.py            # Entry point
```

- **Domain**: Account types and `Bank` (thin aggregate; no transfer logic).
- **Repositories**: Load/save the `Bank` aggregate (in-memory implementation included).
- **Services**: Transfer orchestration and lock ordering to avoid deadlock.

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
