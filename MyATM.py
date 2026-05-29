import json
import os

#os function for clear screen
def clear_screen():
    if os.name=="nt":
        os.system("cls")
    else:
        os.system("clear")

def save_account():
    with open("Accounts.json","w") as file:
        json.dump(Accounts,file,indent=4)

def load_accounts(): 
    if os.path.exists("Accounts.json"):
        with open("Accounts.json","r") as file:
            return json.load(file)
    else:
        return []  
Accounts = load_accounts()
#___________________________________________________________________
#SIGN UP FUNCTION
#___________________________________________________________________

def signup(Accounts):
    print("\n=======CREATE ACCOUNTS =============")
    account_number = input("Enter account number: ")
#kuhakikisha account haipo tyar
    existing_account = find_account(Accounts, account_number)
    if existing_account:
        print("Account number already exists")
        return
    name=input("Enter account name: ")
    pin=input("Create 4-digit pin: ")
    if len(pin) !=4 or not pin.isdigit():
        print("Pin must be exactly four digits")
        return
    
    try:
        balance=float(input("Enter initial balance: "))
        if balance < 0:
            print("Balance could not be negative")
            return
    except:
        print("invalid balance")
        return
    
#kutengeneza account mpya
    new_account ={
        "account_number":account_number,
        "pin":pin,
        "name":name,
        "balance":balance,
        "transaction":[]
    }
#kuhifadhi kwenye list
    Accounts.append(new_account)
    save_account()
    print("Accoun created sucsesifull🎉🎉🎉🎉")

# -----------------------------
# VIEW ACCOUNTS WITH PIN
# -----------------------------

def view_accounts(Accounts):

    admin_pin = input(
        "Enter Admin PIN to view accounts: "
    )

    if admin_pin != "9999":
        print("Wrong PIN.")
        return

    if len(Accounts) == 0:
        print("No accounts found.")
        return

    print("\n===== ALL ACCOUNTS =====")

    for account in Accounts:

        print(f"""
Account Number : {account['account_number']}
Name           : {account['name']}
Balance        : {account['balance']}
PIN            : {account['pin']}
-------------------------------
""")

#____________________________________________________________________
# FIND ACCOUNT
#____________________________________________________________________


def find_account(Accounts, account_number):

    for account in Accounts:
        if account["account_number"] == account_number:
            return account

    return None


# __________________________________________________________________
# LOGIN FUNCTION
# __________________________________________________________________

def login(accounts):

    attempts = 3

    while attempts > 0:

        account_number = input("Enter Account Number: ")
        pin = input("Enter PIN: ")

        account = find_account(accounts, account_number)

        if account and account["pin"] == pin:
            print(f"\nLogin successful, welcome {account['name']}!\n")
            return account

        else:
            attempts -= 1
            print(f"Invalid account number or PIN. Attempts left: {attempts}")

    print("Too many failed attempts.")
    return None


# --------------------------------------------------------------
# CHECK BALANCE
# ---------------------------------------------------------------

def check_balance(account):

    print(f"Current Balance: {account['balance']}")


# --------------------------------------------------------------
# DEPOSIT FUNCTION
# --------------------------------------------------------------

def deposit(account, amount):

    if amount <= 0:
        print("Invalid deposit amount.")
        return

    account["balance"] += amount

    transaction = f"Deposit: +{amount}, Balance: {account['balance']}"
    Accounts.append(transaction)
    save_account()

    print(f"Deposit successful. New balance: {account['balance']}")


# ----------------------------------------------------------------
# WITHDRAW FUNCTION
# ----------------------------------------------------------------
def withdraw(account, amount):

    if amount <= 0:
        print("Invalid withdraw amount.")
        return

    if amount > account["balance"]:
        print("Insufficient balance.")
        return

    account["balance"] -= amount

    transaction = f"Withdraw: -{amount}, Balance: {account['balance']}"
    Accounts.append(transaction)

    print(f"Withdraw successful. New balance: {account['balance']}")


# -----------------------------------------------------------
# TRANSFER FUNCTION
# -----------------------------------------------------------

def transfer(accounts, from_account, to_account_number, amount):

    if amount <= 0:
        print("Invalid transfer amount.")
        return

    if amount > from_account["balance"]:
        print("Insufficient balance.")
        return

    if from_account["account_number"] == to_account_number:
        print("Cannot transfer to same account.")
        return

    receiver = find_account(accounts, to_account_number)

    if receiver is None:
        print("Receiver account does not exist.")
        return

    # Transfer process
    from_account["balance"] -= amount
    receiver["balance"] += amount

    sender_transaction = (
        f"Transfer to {to_account_number}: -{amount}, "
        f"Balance: {from_account['balance']}"
    )

    receiver_transaction = (
        f"Received from {from_account['account_number']}: +{amount}, "
        f"Balance: {receiver['balance']}"
    )

    from_account["transactions"].append(sender_transaction)
    receiver["transactions"].append(receiver_transaction)

    print(f"Transfer successful to Account {to_account_number}")


# -----------------------------------------------------------
# MINI STATEMENT
# -----------------------------------------------------------

def mini_statement(account, n=5):

    print("\n===== MINI STATEMENT =====")

    transactions = account["transactions"]

    if len(transactions) == 0:
        print("No transactions available.")
        return

    last_transactions = transactions[-n:]

    for transaction in last_transactions:
        print(transaction)


# -----------------------------------------------------------
# CHANGE PIN
# -----------------------------------------------------------

def change_pin(account):

    old_pin = input("Enter old PIN: ")

    if old_pin != account["pin"]:
        print("Old PIN does not match.")
        return

    new_pin = input("Enter new 4-digit PIN: ")

    if len(new_pin) != 4 or not new_pin.isdigit():
        print("PIN must be exactly 4 digits.")
        return

    confirm_pin = input("Confirm new PIN: ")

    if new_pin != confirm_pin:
        print("PIN confirmation does not match.")
        return

    account["pin"] = new_pin

    print("PIN changed successfully.")


# --------------------------------------------------------------
# ATM MENU
# --------------------------------------------------------------

def atm_menu(accounts, account):

    while True:

        print("\n===== ATM MENU =====")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Mini Statement")
        print("6. Change PIN")
        print("7. Logout")

        choice = input("Enter choice: ")

        # CHECK BALANCE
        if choice == "1":
            clear_screen()
            check_balance(account)


        # DEPOSIT
        elif choice == "2":
            clear_screen()
            amount = float(input("Enter deposit amount: "))
            deposit(account, amount)

        # WITHDRAW
        elif choice == "3":
            clear_screen()
            amount = float(input("Enter withdraw amount: "))
            withdraw(account, amount)

        # TRANSFER
        elif choice == "4":
            clear_screen()
            receiver_account = input("Enter receiver account number: ")
            amount = float(input("Enter amount to transfer: "))

            transfer(accounts, account, receiver_account, amount)

        # MINI STATEMENT
        elif choice == "5":
            clear_screen()

            try:
                n = int(input("How many transactions to show? "))
                mini_statement(account, n)

            except:
                print("Invalid number.")

        # CHANGE PIN
        elif choice == "6":
            clear_screen()
            change_pin(account)

        # LOGOUT
        elif choice == "7":
            clear_screen()
            print("Logged out.")
            break

        else:
            clear_screen()
            print("Invalid choice.")


# ---------------------------------------------------------------
# MAIN PROGRAM LOOP
# ---------------------------------------------------------------

while True:

    print("\n===== MAIN MENU =====")
    print("1.signup")
    print("2.Login")
    print("3.View accounts")
    print("4.Exit")

    option = input("Choose option: ")

    #SIGN UP
    if option== "1":
        clear_screen()
        signup(Accounts)
    # LOGIN
    elif option == "2":
        clear_screen()

        logged_in_account = login(Accounts)

        if logged_in_account:
            atm_menu(Accounts, logged_in_account)

    #VIEW ACCOUNTS
    elif option == "3":
        clear_screen()
        view_accounts(Accounts)

    # EXIT
    elif option == "4":
        clear_screen()
        print("Thank you for using ATM System.")
        break

    else:
        clear_screen()
        print("Invalid option.")