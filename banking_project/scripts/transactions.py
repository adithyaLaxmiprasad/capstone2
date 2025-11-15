from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime
import csv
import os
from pathlib import Path

@dataclass
class Transaction:
    timestamp: str
    account_no: str
    holder_name: str
    action: str         # "DEPOSIT" | "WITHDRAW" | "INTEREST" | "OPEN"
    amount: float
    balance_after: float
    note: Optional[str] = None

class TransactionLogger:
    """
    Simple CSV logger. By default writes to ./data/transactions_YYYYMMDD.csv
    """
    def __init__(self, base_dir: Optional[str] = None):
        base = Path(base_dir) if base_dir else Path.cwd() / "data"
        base.mkdir(parents=True, exist_ok=True)
        self.base = base

    def _today_file(self) -> Path:
        fname = f"transactions_{datetime.now().strftime('%Y%m%d')}.csv"
        return self.base / fname

    def log(self, tx: Transaction) -> Path:
        fpath = self._today_file()
        is_new = not fpath.exists()
        with fpath.open("a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "timestamp","account_no","holder_name","action",
                    "amount","balance_after","note"
                ]
            )
            if is_new:
                writer.writeheader()
            writer.writerow(asdict(tx))
        return fpath

def make_tx(account_no: str, holder_name: str, action: str, amount: float, balance_after: float, note: str | None = None) -> Transaction:
    return Transaction(
        timestamp=datetime.now().isoformat(timespec="seconds"),
        account_no=account_no,
        holder_name=holder_name,
        action=action,
        amount=round(amount, 2),
        balance_after=round(balance_after, 2),
        note=note
    )
