import pytest
from banking_project.scripts.customers import Customer, CustomerRepository, CustomerAccounts

def test_repository_add_and_get():
    repo = CustomerRepository()
    c = Customer(customer_id="C1", name="Alice", email="alice@example.com")
    repo.add(c)
    assert repo.get_by_id("C1") == c
    assert repo.get_by_email("alice@example.com") == c

def test_repository_duplicates():
    repo = CustomerRepository()
    repo.add(Customer(customer_id="C1", name="A", email="a@x.com"))
    with pytest.raises(ValueError):
        repo.add(Customer(customer_id="C1", name="B", email="b@x.com"))
    with pytest.raises(ValueError):
        repo.add(Customer(customer_id="C2", name="B", email="a@x.com"))

def test_customer_accounts_open_and_get():
    from banking_project.scripts.accounts import SavingsAccount, CurrentAccount
    c = Customer(customer_id="C2", name="Bob", email="bob@example.com")
    ca = CustomerAccounts(customer=c)
    s = ca.open_savings(initial_deposit=200)
    cu = ca.open_current(initial_deposit=100, overdraft_limit=50)
    assert isinstance(s, SavingsAccount)
    assert isinstance(cu, CurrentAccount)
    assert ca.get_account(s.account_no) is s
