import pytest
from banking_project.scripts.accounts import ( BankAccount, SavingsAccount, CurrentAccount,InsufficientFundsError, InvalidAmountError )

def test_deposit_and_withdraw():
    acc = BankAccount(account_no="AC-1", holder_name="Alice", balance=100)
    acc.deposit(50)
    assert acc.get_balance() == 150.00
    acc.withdraw(20)
    assert acc.get_balance() == 130.00

def test_withdraw_insufficient():
    acc = BankAccount(account_no="AC-2", holder_name="Bob", balance=50)
    with pytest.raises(InsufficientFundsError):
        acc.withdraw(60)

def test_invalid_amounts():
    acc = BankAccount(account_no="AC-3", holder_name="Eve", balance=0)
    with pytest.raises(InvalidAmountError):
        acc.deposit(0)
    with pytest.raises(InvalidAmountError):
        acc.withdraw(-5)

def test_savings_interest():
    sav = SavingsAccount(account_no="SAV-1", holder_name="Alice", balance=1000, interest_rate=0.05)
    interest = sav.apply_interest(1)
    assert interest == 50.00
    assert sav.get_balance() == 1050.00

def test_current_overdraft():
    cur = CurrentAccount(account_no="CUR-1", holder_name="Bob", balance=100, overdraft_limit=50)
    cur.withdraw(140)
    assert cur.get_balance() == -40.00
    with pytest.raises(InsufficientFundsError):
        cur.withdraw(20)
