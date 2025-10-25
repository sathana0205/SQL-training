import json
import os
import mysql.connector
conn=mysql.connector.connect (
    host="localhost",
    port=3306,
    user="root",
    password="sathana",
    database="bank_db"
)
def get_connection():
    try:
        conn=mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="sathana",
            database="bank_db"
        )
        return conn
    except mysql.connector.Error as e:
        print("Couldn't connect ot Mysql.Please")
        print("Error: ", e)
        return None

DATA_FILE = "bank_data.json"

# ---------- Data Handling ----------
def load_data():
    """Load data as a list (convert old dict data if found)."""
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return []

    # Convert dict format (old) → list format (new)
    if isinstance(data, dict):
        new_list = []
        for name, details in data.items():
            if isinstance(details, dict):
                details["account_holder"] = name
                new_list.append(details)
        save_data(new_list)
        return new_list

    if isinstance(data, list):
        return data

    return []


def save_data(data):
    """Save data list to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ---------- BankAccount Class ----------
class BankAccount:
    def __init__(self, account_holder, pin, balance=0):
        self.account_holder = account_holder
        self.__pin = pin
        self.__balance = balance

    def verify_pin(self, pin):
        return self.__pin == pin

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            return f"Deposited ₹{amount}. New balance: ₹{self.__balance}"
        return "Invalid deposit amount."

    def withdraw(self, amount):
        if amount <= 0:
            return "Invalid withdrawal amount."
        elif amount > self.__balance:
            return "Insufficient funds."
        else:
            self.__balance -= amount
            return f"Withdrew ₹{amount}. Remaining balance: ₹{self.__balance}"

    def get_balance(self):
        return self.__balance

    def to_dict(self):
        return {
            "account_holder": self.account_holder,
            "pin": self.__pin,
            "balance": self.__balance
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["account_holder"], data["pin"], data["balance"])


# ---------- CRUD Operations ----------
def create_account(accounts_data):
    print("\n--- Create Account ---")
    name = input("Enter account holder name: ").strip()
    pin = input("Set 4-digit PIN: ").strip()
    try:
        initial_balance = float(input("Initial Deposit (₹): "))
    except ValueError:
        print("Invalid amount.")
        return

    if not name:
        print("Enter a valid name.")
        return
    if not pin.isdigit() or len(pin) != 4:
        print("PIN must be a 4-digit number.")
        return

    # Save to JSON (for local data)
    new_account = BankAccount(name, pin, initial_balance)
    accounts_data.append(new_account.to_dict())
    save_data(accounts_data)

    # Save to MySQL as well
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO account (account_holder, pin, balance)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (name, pin, initial_balance))
            conn.commit()
            print(f"Account created for {name} and saved to MySQL!")
        except Exception as e:
            print("Failed to save to database:", e)
        finally:
            cursor.close()
            conn.close()
    else:
        print("Could not connect to MySQL, saved only in JSON file.")

    # Duplicates allowed — no name check
    new_account = BankAccount(name, pin, initial_balance)
    accounts_data.append(new_account.to_dict())
    save_data(accounts_data)
    print(f" Account created for {name} with ₹{initial_balance}")


def read_accounts(accounts_data):
    print("\n--- All Accounts ---")
    if not accounts_data:
        print("No accounts found.")
        return

    for i, acc in enumerate(accounts_data, start=1):
        print(f"{i}. Name: {acc['account_holder']}, Balance: ₹{acc['balance']}")


def update_account(accounts_data):
    print("\n--- Update Account ---")
    name = input("Enter account holder name to update: ").strip()

    # Find all matching accounts
    matches = [acc for acc in accounts_data if acc["account_holder"] == name]
    if not matches:
        print("Account not found.")
        return

    for acc in matches:
        new_name = input(f"Enter new name for {name} (leave blank to skip): ").strip()
        new_pin = input("Enter new 4-digit PIN (leave blank to skip): ").strip()

        if new_name:
            acc["account_holder"] = new_name
        if new_pin and new_pin.isdigit() and len(new_pin) == 4:
            acc["pin"] = new_pin


    save_data(accounts_data)
    print(" Account(s) updated successfully.")


def delete_account(accounts_data):
    print("\n--- Delete Account ---")
    name = input("Enter account name to delete: ").strip()

    # Delete all matching names
    before = len(accounts_data)
    accounts_data[:] = [acc for acc in accounts_data if acc["account_holder"] != name]
    after = len(accounts_data)

    if before == after:
        print("Account not found.")
    else:
        save_data(accounts_data)
        print(f" Deleted {before - after} account(s) for '{name}'.")


# ---------- Login + ATM ----------
def login(accounts_data):
    print("\n--- Login ---")
    name = input("Enter account holder name: ").strip()
    pin = input("Enter your 4-digit PIN: ").strip()

    # Allow multiple same-name accounts
    for acc_data in accounts_data:
        if acc_data["account_holder"] == name:
            account = BankAccount.from_dict(acc_data)
            if account.verify_pin(pin):
                print(f" Welcome {name}! Login successful.")
                return account, acc_data
    print(" Incorrect name or PIN.")
    return None, None


def atm_operations(account, account_data, accounts_data):
    while True:
        print("\n--- ATM Operations ---")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Logout")
        choice = input("Choose an option (1-4): ")

        if choice == "1":
            try:
                amount = int(input("Enter deposit amount: ₹"))
                print(account.deposit(amount))
                account_data.update(account.to_dict())
                save_data(accounts_data)
            except ValueError:
                print("Invalid amount.")
        elif choice == "2":
            try:
                amount = int(input("Enter withdrawal amount: ₹"))
                print(account.withdraw(amount))
                account_data.update(account.to_dict())
                save_data(accounts_data)
            except ValueError:
                print("Invalid amount.")
        elif choice == "3":
            print(f"Your current balance is ₹{account.get_balance()}")
        elif choice == "4":
            print(" Logged out successfully.")
            break
        else:
            print("Invalid option. Try again.")


# ---------- Main Program ----------
def main():
    accounts_data = load_data()

    while True:
        print("\n===== Welcome to the Bank ATM System =====")
        print("1. Create Account")
        print("2. Login")
        print("3. Read Accounts")
        print("4. Update Account")
        print("5. Delete Account")
        print("6. Exit")
        choice = input("Select an option (1-6): ")

        if choice == "1":
            create_account(accounts_data)
        elif choice == "2":
            account, account_data = login(accounts_data)
            if account:
                atm_operations(account, account_data, accounts_data)
        elif choice == "3":
            read_accounts(accounts_data)
        elif choice == "4":
            update_account(accounts_data)
        elif choice == "5":
            delete_account(accounts_data)
        elif choice == "6":
            print(" Thank you for using the ATM System. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()