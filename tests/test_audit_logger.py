"""Tests for AuditLogger."""

import asyncio

import pytest

from domain.logger import AuditLogger, LogRecord
from domain.models import AccountAction


def test_log_appends_record() -> None:
    logger = AuditLogger()

    async def run_log() -> None:
        await logger.log(1, AccountAction.DEPOSIT, 100.0)

    asyncio.run(run_log())

    assert len(logger.history) == 1
    rec = logger.history[0]
    assert rec.account_number == 1
    assert rec.action == AccountAction.DEPOSIT
    assert rec.amount == 100.0
    assert rec.timestamp != ""


def test_get_logs_filters_by_account_number() -> None:
    logger = AuditLogger()

    async def run_logs() -> None:
        await logger.log(1, AccountAction.DEPOSIT, 50.0)
        await logger.log(2, AccountAction.WITHDRAW, 20.0)
        await logger.log(1, AccountAction.WITHDRAW, 10.0)

    asyncio.run(run_logs())

    one_logs = logger.get_logs(1)
    assert len(one_logs) == 2
    assert [r.amount for r in one_logs] == [50.0, 10.0]

    two_logs = logger.get_logs(2)
    assert len(two_logs) == 1
    assert two_logs[0].action == AccountAction.WITHDRAW and two_logs[0].amount == 20.0


def test_get_logs_empty_for_unknown_account() -> None:
    logger = AuditLogger()

    async def run_log() -> None:
        await logger.log(1, AccountAction.INTEREST, 5.0)

    asyncio.run(run_log())

    assert logger.get_logs(999) == []
