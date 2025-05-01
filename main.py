import mysql.connector

# Establishing connection to the database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='7704Mahonia!',
    database='banking_system'
)
cursor = conn.cursor()

def login():
    """
    Prompts the user to enter their account number and PIN,
    then verifies if the credentials are valid in the database.
    """
    account_number = input("Enter your Account Number: ")
    pin = input("Enter your PIN: ")
    
    cursor.execute("SELECT * FROM accounts WHERE account_number = %s AND pin = %s", (account_number, pin))
    user_data = cursor.fetchone()

    if user_data:
        print("\nLogin successful! Welcome back!\n")
        user_menu(user_data[0])
    else:
        print("\nInvalid account number or PIN! Please try again.\n")

def user_menu(account_number):
    """
    Displays a menu with options for the user after login.
    Allows the user to check balance, deposit, withdraw, or log out.
    """
    while True:
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Logout")
        
        try:
            choice = int(input("Choose an option: "))
            if choice == 1:
                check_balance(account_number)
            elif choice == 2:
                deposit(account_number)
            elif choice == 3:
                withdraw(account_number)
            elif choice == 4:
                print("\nLogging out...\n")
                break
            else:
                print("Invalid option! Please choose a valid number from 1 to 4.")
        except ValueError:
            print("Please enter a valid number.")

def check_balance(account_number):
    """
    Checks and displays the balance of the given account number.
    """
    cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (account_number,))
    balance = cursor.fetchone()[0]
    print(f"\nYour current balance is: ${balance:.2f}\n")

def deposit(account_number):
    """
    Prompts the user for an amount to deposit, updates the balance in the database.
    """
    while True:
        try:
            amount = float(input("Enter amount to deposit: $"))
            if amount <= 0:
                print("Deposit amount must be greater than zero.")
            else:
                cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_number = %s", (amount, account_number))
                conn.commit()
                print("\nDeposit successful!\n")
                break
        except ValueError:
            print("Invalid amount entered. Please enter a numeric value.")

def withdraw(account_number):
    """
    Prompts the user for an amount to withdraw and updates the balance if sufficient funds are available.
    """
    while True:
        try:
            amount = float(input("Enter amount to withdraw: $"))
            if amount <= 0:
                print("Withdrawal amount must be greater than zero.")
                continue

            cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (account_number,))
            balance = cursor.fetchone()[0]

            if amount > balance:
                print("\nInsufficient funds! Please try a smaller amount.\n")
            else:
                cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_number = %s", (amount, account_number))
                conn.commit()
                print("\nWithdrawal successful!\n")
                break
        except ValueError:
            print("Invalid amount entered. Please enter a numeric value.")

def create_account():
    """
    Prompts the user to create a new account with an account number, PIN, and name.
    """
    while True:
        account_number = input("Enter a new account number: ")
        cursor.execute("SELECT * FROM accounts WHERE account_number = %s", (account_number,))
        if cursor.fetchone():
            print("Account number already exists. Please choose a different one.")
        else:
            break

    pin = input("Set a 4-digit PIN: ")
    name = input("Enter your full name: ")

    cursor.execute("INSERT INTO accounts (account_number, pin, name) VALUES (%s, %s, %s)", (account_number, pin, name))
    conn.commit()
    print("\nAccount created successfully! You can now log in.\n")

def close_account():
    """
    Allows the user to close an account by entering the account number.
    """
    account_number = input("Enter the account number to close: ")
    cursor.execute("DELETE FROM accounts WHERE account_number = %s", (account_number,))
    conn.commit()
    print("\nAccount closed successfully!\n")

def modify_account():
    """
    Allows the user to modify their account information (name or PIN).
    """
    account_number = input("Enter the account number to modify: ")
    print("1. Change Name")
    print("2. Change PIN")
    
    try:
        choice = int(input("Choose an option: "))
        if choice == 1:
            new_name = input("Enter new name: ")
            cursor.execute("UPDATE accounts SET name = %s WHERE account_number = %s", (new_name, account_number))
        elif choice == 2:
            new_pin = input("Enter new 4-digit PIN: ")
            cursor.execute("UPDATE accounts SET pin = %s WHERE account_number = %s", (new_pin, account_number))
        else:
            print("Invalid choice! Please choose 1 or 2.")
            return
        
        conn.commit()
        print("\nAccount updated successfully!\n")
    except ValueError:
        print("Invalid input. Please enter a valid number for the option.")

# Main loop to present options to the user
while True:
    print("\nWelcome to the Bank!")
    print("1. Login")
    print("2. Create Account")
    print("3. Close Account")
    print("4. Modify Account")
    print("5. Exit")
    
    try:
        choice = int(input("Choose an option: "))
        if choice == 1:
            login()
        elif choice == 2:
            create_account()
        elif choice == 3:
            close_account()
        elif choice == 4:
            modify_account()
        elif choice == 5:
            print("\nThank you for using the banking system. Goodbye!")
            break
        else:
            print("Invalid option! Please choose a valid option.")
    except ValueError:
        print("Please enter a valid number.")
