import time
import os
import json

# Clear screen function
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Account class
class Account:
    def __init__(self, account_number, pin, initial_balance=0):
        self.account_number = account_number
        self.pin = pin
        self._balance = initial_balance
        self.transaction_history = []

    def __validate_amount(self, amount):
        return isinstance(amount, (int, float)) and amount > 0

    def deposit(self, amount):
        if self.__validate_amount(amount):
            self._balance += amount
            self.transaction_history.append(f"deposit :{amount}")
            print(f"Deposited {amount} successfully.")
        else:
            print("Invalid deposit amount")

    def withdraw(self, amount):
        if self.__validate_amount(amount) and amount <= self._balance:
            self._balance -= amount
            self.transaction_history.append(f"amount : {amount}" )
            print(f"Withdrew {amount} successfully")
        else:
            print("Invalid withdrawal amount or insufficient funds")

    def check_balance(self):
        return self._balance

    def get_transaction_history(self):
        # import datetime
        # current_datetime = datetime.datetime.now()
        # self.transaction_history.append(current_datetime)
        return self.transaction_history

    def display_account(self):
        print(f"Balance: {self._balance}")
        print(f"Account Number: {self.account_number}")
        print(f"PIN: {self.pin}")
        print("-" * 50)

    def to_dict(self):
        return {
            'account_number': self.account_number,
            'pin': self.pin,
            'balance': self._balance
        }

    @staticmethod
    def from_dict(data):
        return Account(data['account_number'], data['pin'], data['balance'])


# Function to load accounts from a JSON file
def load_accounts_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return [Account.from_dict(account_data) for account_data in data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Return an empty list if file doesn't exist or is empty



def store_accounts_to_file(file_path, accounts):
    with open(file_path, 'w') as file:
        json.dump([account.to_dict() for account in accounts], file, indent=4)


# Function to create a new account
def create_account(accounts, file_path):
    clear_screen()
    print("\nCreate New Account\n")

    retry_count = 3 

    while retry_count > 0:
        try:
            account_number = int(input("Enter your account number (numeric): "))
        except(ValueError):
            print("Invalid input! Please enter a numeric account number.")
            continue

        pin = input("Enter your 4-digit PIN: ")


        if len(pin) != 4 or not pin.isdigit():
            print("Invalid PIN! The PIN must be exactly 4 digits and numeric.")
            continue

        pin = int(pin)  # Convert to integer after validation

        try:
            balance = float(input("Enter your initial balance: "))
            if balance < 0:
                print("Balance cannot be negative. Please enter a valid amount.")
                continue
        except(ValueError):
            print("Invalid balance input! Please enter a numeric value for the balance.")
            continue

        
        for account in accounts:
            if account.account_number == account_number:
                print("Account already exists with that account number.")
                retry_count -= 1
                if retry_count == 0:
                    print("Too many failed attempts.")
                    time.sleep(2)
                    return None  
                time.sleep(3)
                break
        else :

            new_account = Account(account_number, pin, balance)
            accounts.append(new_account)

            store_accounts_to_file(file_path, accounts)

            print(f"Account {account_number} created successfully!")
            time.sleep(2)
            return new_account


def delete_account(accounts, file_path):
    clear_screen()
    print("\nDelete By...\n")
    print("1 - Account Number")
    account_number = int(input("Enter your account_number : "))

    account_to_delete = None
    for account in accounts:
        if account.account_number == account_number:
            account_to_delete = account
            break

    if account_to_delete:
        accounts.remove(account_to_delete)
        print(f"Account {account_number} deleted successfully.")

        store_accounts_to_file(file_path, accounts)
    else:
        print("Account not found.")
    time.sleep(2)


# Admin Menu
def Admin_Menu(accounts, file_path):
    clear_screen()
    print("\nAdmin Menu...\n")
    print("1 - View All Accounts")
    print("2 - Delete Account")
    print("3 - Return to Main Menu\n")

    choice = input("Enter your choice: ")
    if choice == '1':
        clear_screen()
        if accounts:
            print("Displaying all accounts...")
            for account in accounts:
                account.display_account()
                time.sleep(2)
        else:
            print("No accounts to display...")
            time.sleep(2)
    elif choice == '2':
        delete_account(accounts, file_path)
    elif choice == '3':
        return



def User_login(accounts):
    clear_screen()
    print("\nLog In\n")

    account_number = int(input("Enter your account number: "))
    pin = int(input("Enter your 4-digit PIN: "))
    
    
    
    found_account = None
    for account in accounts:
        if account.account_number == account_number and account.pin == pin:
            found_account = account
            break

    if found_account:
        while True:
            clear_screen()
            print(f"\nWelcome, Account {found_account.account_number}")
            print("Choose an action:")
            print("1 - Check balance")
            print("2 - Deposit money")
            print("3 - Withdraw money")
            print("4 - View transaction history")
            print("5 - Exit")

            choice = input("Enter your choice: ")
            if choice == '1':
                print(f"Your balance is: {found_account.check_balance()}")
                time.sleep(2)
            elif choice == '2':
                print(f"Balance before deposit = {found_account.check_balance()}")
                amount_deposit = float(input("Enter amount to deposit: "))
                found_account.deposit(amount_deposit)
                found_account.get_transaction_history()
                time.sleep(2)
            elif choice == '3':
                print(f"Balance before withdrawal = {found_account.check_balance()}")
                amount_withdraw = float(input("Enter amount to withdraw: "))
                found_account.withdraw(amount_withdraw)
                found_account.get_transaction_history()
                time.sleep(2)
            elif choice == '4':
                print("Transaction History:")
                print(found_account.get_transaction_history())
                time.sleep(5)
            elif choice == '5':
                print("Exiting user menu...")
                time.sleep(2)
                break
            else:
                print("Invalid choice, try again.")
                time.sleep(2)




if __name__ == "__main__":

    file_path = "bank_data.json"

    accounts = load_accounts_from_file(file_path)

    while True:
        clear_screen()
        print("\nWelcome to the Banking System")
        print("\nChoose an action:")
        print("1. Open New Account")
        print("2. Access Existing Account")
        print("3. Admin Menu")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            new_account = create_account(accounts, file_path)
            if new_account:
                print("Account created successfully!")
                time.sleep(2)
        elif choice == '2':
            User_login(accounts)
        elif choice == '3':
            Admin_Menu(accounts, file_path)
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice, try again.")
            time.sleep(2)
 