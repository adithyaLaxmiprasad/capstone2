from __future__ import annotations
from dataclasses import dataclass
import uuid

class InsufficientFundsError(Exception):
    pass

class InvalidAmountError(Exception):
    pass

@dataclass
class BankAccount:
    account_no: str
    holder_name: str
    balance: float = 0.0

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise InvalidAmountError("Deposit amount must be positive")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise InvalidAmountError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise InsufficientFundsError("Insufficient balance")
        self.balance -= amount

    def get_balance(self) -> float:
        return round(self.balance, 2)

@dataclass
class SavingsAccount(BankAccount):
    interest_rate: float = 0.04

    def apply_interest(self, years: float = 1.0) -> float:
        if years < 0:
            raise InvalidAmountError("Years must be non-negative")
        interest = self.balance * self.interest_rate * years
        self.balance += interest
        return round(interest, 2)

@dataclass
class CurrentAccount(BankAccount):
    overdraft_limit: float = 0.0

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise InvalidAmountError("Withdrawal amount must be positive")
        if amount > self.balance + self.overdraft_limit:
            raise InsufficientFundsError("Exceeds overdraft limit")
        self.balance -= amount

def generate_account_no(prefix: str = "AC") -> str:
    return f"{prefix}-{uuid.uuid4().hex[:10].upper()}"
