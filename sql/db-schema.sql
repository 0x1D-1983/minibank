-- Account types for discriminator
CREATE TYPE account_type AS ENUM ('savings', 'current');

-- Single table for both account types (shared columns + type-specific nullable columns)
CREATE TABLE accounts (
    id              BIGSERIAL PRIMARY KEY,
    account_number  BIGINT NOT NULL UNIQUE,
    owner           VARCHAR(255) NOT NULL,
    type            account_type NOT NULL,
    balance         NUMERIC(18, 2) NOT NULL DEFAULT 0,
    -- SavingsAccount
    interest_rate   NUMERIC(5, 4) NULL CHECK (type <> 'savings' OR interest_rate IS NOT NULL),
    -- CurrentAccount
    overdraft_limit NUMERIC(18, 2) NULL CHECK (type <> 'current' OR overdraft_limit IS NOT NULL),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_savings_interest CHECK (type <> 'savings' OR (interest_rate IS NOT NULL AND overdraft_limit IS NULL)),
    CONSTRAINT chk_current_overdraft CHECK (type <> 'current' OR (overdraft_limit IS NOT NULL AND interest_rate IS NULL))
);

CREATE INDEX idx_accounts_owner ON accounts (owner);
CREATE INDEX idx_accounts_type ON accounts (type);

-- Optional: transaction history (maps to Account.history)
CREATE TABLE account_transactions (
    id              BIGSERIAL PRIMARY KEY,
    account_id      BIGINT NOT NULL REFERENCES accounts (id) ON DELETE CASCADE,
    action          VARCHAR(20) NOT NULL,  -- DEPOSIT, WITHDRAW, INTEREST, TRANSFER
    amount          NUMERIC(18, 2) NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_account_transactions_account_id ON account_transactions (account_id);
