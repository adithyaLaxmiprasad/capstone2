from pathlib import Path
from banking_project.scripts.accounts import BankAccount
from banking_project.scripts.transactions import TransactionLogger, make_tx

def test_transaction_file_is_created_and_has_rows(tmp_path: Path):
    logger = TransactionLogger(base_dir=tmp_path.as_posix())
    acc = BankAccount(account_no="AC-TEST", holder_name="Test", balance=0)

    # Perform a couple of actions and log them
    acc.deposit(100)
    path1 = logger.log(make_tx(acc.account_no, acc.holder_name, "DEPOSIT", 100, acc.get_balance()))

    acc.withdraw(30)
    path2 = logger.log(make_tx(acc.account_no, acc.holder_name, "WITHDRAW", 30, acc.get_balance()))

    # Same file day-wise
    assert path1 == path2
    assert path1.exists()

    content = path1.read_text(encoding="utf-8").strip().splitlines()
    # header + 2 rows
    assert len(content) == 3
    # quick sanity on columns present
    header = content[0].split(",")
    assert "timestamp" in header and "account_no" in header and "balance_after" in header
