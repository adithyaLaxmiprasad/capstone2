from __future__ import annotations
from scripts.accounts import SavingsAccount, CurrentAccount, InvalidAmountError, InsufficientFundsError
from scripts.customers import Customer, CustomerAccounts
from scripts.transactions import TransactionLogger, make_tx

def prompt(msg: str) -> str:
    return input(msg).strip()

def choose_account(ca: CustomerAccounts):
    if not ca.accounts:
        print("No accounts yet.")
        return None
    print("Your accounts:")
    for i, acc in enumerate(ca.accounts.values(), start=1):
        print(f"{i}. {acc.account_no} ({acc.__class__.__name__}) - Balance: {acc.get_balance()}")
    idx = int(prompt("Choose account number (index): "))
    if idx < 1 or idx > len(ca.accounts):
        print("Invalid choice.")
        return None
    return list(ca.accounts.values())[idx-1]

def main():
    print("=== Welcome to Mini ATM ===")
    name = prompt("Enter your name: ")
    email = prompt("Enter your email: ")
    customer = Customer(customer_id=email, name=name, email=email)
    ca = CustomerAccounts(customer)
    logger = TransactionLogger()

    while True:
        print("\nMenu:")
        print("1. Open Savings")
        print("2. Open Current")
        print("3. Deposit")
        print("4. Withdraw")
        print("5. Check Balance")
        print("6. Apply Interest (Savings only)")
        print("7. Exit")

        choice = prompt("Choose: ")
        try:
            if choice == "1":
                initial = float(prompt("Initial deposit (>=0): "))
                rate = float(prompt("Interest rate (e.g., 0.04): "))
                acc = ca.open_savings(initial, rate)
                logger.log(make_tx(acc.account_no, acc.holder_name, "OPEN", initial, acc.get_balance(), "Savings opened"))
                print(f"Savings opened: {acc.account_no} | Balance: {acc.get_balance()}")

            elif choice == "2":
                initial = float(prompt("Initial deposit (>=0): "))
                od = float(prompt("Overdraft limit (>=0): "))
                acc = ca.open_current(initial, od)
                logger.log(make_tx(acc.account_no, acc.holder_name, "OPEN", initial, acc.get_balance(), f"Current opened, OD={od}"))
                print(f"Current opened: {acc.account_no} | Balance: {acc.get_balance()}")

            elif choice == "3":
                acc = choose_account(ca)
                if not acc: continue
                amount = float(prompt("Deposit amount: "))
                acc.deposit(amount)
                logger.log(make_tx(acc.account_no, acc.holder_name, "DEPOSIT", amount, acc.get_balance()))
                print(f"Deposited. New balance: {acc.get_balance()}")

            elif choice == "4":
                acc = choose_account(ca)
                if not acc: continue
                amount = float(prompt("Withdraw amount: "))
                acc.withdraw(amount)
                logger.log(make_tx(acc.account_no, acc.holder_name, "WITHDRAW", amount, acc.get_balance()))
                print(f"Withdrawn. New balance: {acc.get_balance()}")

            elif choice == "5":
                acc = choose_account(ca)
                if not acc: continue
                print(f"Balance: {acc.get_balance()}")

            elif choice == "6":
                acc = choose_account(ca)
                if not acc: continue
                if isinstance(acc, SavingsAccount):
                    years = float(prompt("Years to apply interest for: "))
                    earned = acc.apply_interest(years)
                    logger.log(make_tx(acc.account_no, acc.holder_name, "INTEREST", earned, acc.get_balance(), f"years={years}"))
                    print(f"Interest applied: {earned}. New balance: {acc.get_balance()}")
                else:
                    print("Selected account is not a SavingsAccount.")

            elif choice == "7":
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
        except (InvalidAmountError, InsufficientFundsError, ValueError) as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
