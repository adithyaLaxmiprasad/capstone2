from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple
from .accounts import BankAccount, SavingsAccount, CurrentAccount, generate_account_no

@dataclass(frozen=True)
class Customer:
    customer_id: str
    name: str
    email: str

class CustomerRepository:
    def __init__(self):
        self._by_id: Dict[str, Customer] = {}
        self._by_email: Dict[str, str] = {}
        self._order: List[str] = []

    def add(self, customer: Customer) -> None:
        if customer.customer_id in self._by_id:
            raise ValueError("Duplicate customer_id")
        if customer.email in self._by_email:
            raise ValueError("Duplicate email")
        self._by_id[customer.customer_id] = customer
        self._by_email[customer.email] = customer.customer_id
        self._order.append(customer.customer_id)

    def get_by_id(self, customer_id: str) -> Optional[Customer]:
        return self._by_id.get(customer_id)

    def get_by_email(self, email: str) -> Optional[Customer]:
        cid = self._by_email.get(email)
        return self._by_id.get(cid) if cid else None

    def list_all(self) -> List[Customer]:
        return [self._by_id[cid] for cid in self._order]

    def emails_set(self) -> Set[str]:
        return set(self._by_email.keys())

    def snapshot_ids(self) -> Tuple[str, ...]:
        return tuple(self._order)

@dataclass
class CustomerAccounts:
    customer: Customer
    accounts: Dict[str, BankAccount] = field(default_factory=dict)

    def open_savings(self, initial_deposit: float = 0.0, rate: float = 0.04) -> SavingsAccount:
        acc_no = generate_account_no("SAV")
        acc = SavingsAccount(account_no=acc_no, holder_name=self.customer.name,
                             balance=initial_deposit, interest_rate=rate)
        self.accounts[acc_no] = acc
        return acc

    def open_current(self, initial_deposit: float = 0.0, overdraft_limit: float = 0.0) -> CurrentAccount:
        acc_no = generate_account_no("CUR")
        acc = CurrentAccount(account_no=acc_no, holder_name=self.customer.name,
                             balance=initial_deposit, overdraft_limit=overdraft_limit)
        self.accounts[acc_no] = acc
        return acc

    def get_account(self, account_no: str) -> BankAccount:
        if account_no not in self.accounts:
            raise KeyError("Account not found")
        return self.accounts[account_no]
