import os

import random

import tkinter as tk
from tkinter import messagebox



class Account:
    def __init__(self, name, address, ssn, card_num, pin, balance):
        self.name = name
        self.address = address
        self.ssn = ssn
        self.card_num = card_num
        self.pin = pin
        self.balance = balance
        
class Transaction:
    TYPE_WITHDRAW = "Withdraw"
    TYPE_DEPOSIT = "Deposit"
    TYPE_TRANSFER = "Transfer"

    def __init__(self, type_of_transaction, src_card_num, dst_card_num, amount):
        self.type_of_transaction = type_of_transaction
        self.src_card_num = src_card_num
        self.dst_card_num = dst_card_num
        self.amount = amount

class Data:
    FILENAME = "data.txt"

    def __init__(self):
        self.accounts = []
        self.transactions = []

    def save_to_text_file(self):
        try:
            with open(self.FILENAME, 'w') as outFile:
                outFile.write(f"{len(self.accounts)}\n")
                for account in self.accounts:
                    outFile.write(f"{account.name}\n")
                    outFile.write(f"{account.address}\n")
                    outFile.write(f"{account.ssn}\n")
                    outFile.write(f"{account.card_num}\n")
                    outFile.write(f"{account.pin}\n")
                    outFile.write(f"{account.balance}\n")

                outFile.write(f"{len(self.transactions)}\n")
                for transaction in self.transactions:
                    outFile.write(f"{transaction.type_of_transaction}\n")
                    outFile.write(f"{transaction.src_card_num}\n")
                    outFile.write(f"{transaction.dst_card_num}\n")
                    outFile.write(f"{transaction.amount}\n")
            print("Written to", os.getcwd(), self.FILENAME)
        except IOError as e:
            print(f"An error occurred while writing to file {self.FILENAME}: {e}")

    def read_from_text_file(self):
        try:
            with open(self.FILENAME, 'r') as inFile:
                lines = inFile.readlines()
                self.accounts.clear()
                self.transactions.clear()

                num_accounts = int(lines[0])
                current_line = 1
                for _ in range(num_accounts):
                    name = lines[current_line].strip()
                    address = lines[current_line + 1].strip()
                    ssn = lines[current_line + 2].strip()
                    card_num = lines[current_line + 3].strip()
                    pin = lines[current_line + 4].strip()
                    balance = float(lines[current_line + 5].strip())

                    account = Account(name, address, ssn, card_num, pin, balance)
                    self.accounts.append(account)

                    current_line += 6

                num_transactions = int(lines[current_line])
                current_line += 1
                for _ in range(num_transactions):
                    transaction_type = lines[current_line].strip()
                    src_card_num = lines[current_line + 1].strip()
                    dst_card_num = lines[current_line + 2].strip()
                    amount = float(lines[current_line + 3].strip())

                    transaction = Transaction(transaction_type, src_card_num, dst_card_num, amount)
                    self.transactions.append(transaction)

                    current_line += 4

        except FileNotFoundError:
            print(f"There is no file with name {self.FILENAME}, so, no data is restored.")
        except IOError as e:
            print(f"An error occurred while reading from file {self.FILENAME}: {e}")

    def create_new_account_for(self, name, address, ssn, balance):
        used_card_numbers = set(account.card_num for account in self.accounts)
        random.seed()
        while True:
            new_card_num = str(random.randint(10**15, 10**16 - 1))
            if new_card_num in used_card_numbers:
                continue

            # generate new pin
            pin = str(random.randint(0, 9999)).zfill(4)

            account = Account(name, address, ssn, new_card_num, pin, balance)
            self.accounts.append(account)
            return account

    def get_account_by_card_number_and_pin(self, card_num, pin):
        for account in self.accounts:
            if account.card_num == card_num and account.pin == pin:
                return account
        return None

    def get_account_by_card_number(self, card_num):
        for account in self.accounts:
            if account.card_num == card_num:
                return account
        return None

    def get_transactions_by_card_number(self, card_num):
        single_card_transactions = []
        for transaction in self.transactions:
            if transaction.src_card_num == card_num or transaction.dst_card_num == card_num:
                single_card_transactions.append(transaction)
        return single_card_transactions

class Deposit(tk.Frame):
    def __init__(self, data, account):
        super().__init__()

        self.data = data
        self.account = account

        self.configure(bg="#D8D8D8")
        self.grid()

        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self, text="Deposit:", font=("Tahoma", 20))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.balance_label = tk.Label(self, text="Your balance is:")
        self.balance_label.grid(row=1, column=0)
        
        self.balance_value_label = tk.Label(self, text=str(self.account.balance))
        self.balance_value_label.grid(row=1, column=1, columnspan=2)

        self.deposit_label = tk.Label(self, text="Deposit amount:")
        self.deposit_label.grid(row=2, column=0)

        self.deposit_entry = tk.Entry(self)
        self.deposit_entry.grid(row=2, column=1, columnspan=2)

        self.proceed_button = tk.Button(self, text="Deposit", command=self.handle_deposit)
        self.proceed_button.configure(bg="#19A7CE")
        self.proceed_button.grid(row=3, column=1)

        self.cancel_button = tk.Button(self, text="Cancel", command=self.handle_cancel)
        self.cancel_button.configure(bg="#19A7CE")
        self.cancel_button.grid(row=3, column=2)

        self.error_messages_text = tk.Label(self, text="", fg="firebrick")
        self.error_messages_text.grid(row=4, column=0, columnspan=2, pady=10)

    def set_error_message(self, error_message):
        self.error_messages_text.config(text=error_message)

    def handle_deposit(self):
        deposit_amount_str = self.deposit_entry.get().strip()

        try:
            deposit_amount = float(deposit_amount_str)
        except ValueError:
            self.set_error_message("Please enter a valid number greater than 0 for deposit amount")
            return

        if deposit_amount < 0:
            self.set_error_message("Deposit amount can't be negative")
            return

        self.account.balance += deposit_amount
        self.data.transactions.append(Transaction(Transaction.TYPE_DEPOSIT, self.account.card_num, self.account.card_num, deposit_amount))

        messagebox.showinfo("Success", f"Deposit of {deposit_amount} success!\nYour new balance is {self.account.balance}")

        # Take to user home screen
        self.master.destroy()
        UserHome(self.data, self.account).mainloop()

    def handle_cancel(self):
        # Take to user home screen
        self.master.destroy()
        UserHome(self.data, self.account).mainloop()

class Login(tk.Frame):
    def __init__(self, data):
        super().__init__()

        self.data = data

        self.configure(bg="#D8D8D8")
        self.grid()

        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self, text="WELCOME TO ATM", font=("Tahoma", 20), fg="#245953")
        self.title_label.grid(row=0, column=0, columnspan=3)

        self.card_label = tk.Label(self, text="Card No.:")
        self.card_label.grid(row=1, column=0)

        self.card_entry = tk.Entry(self)
        self.card_entry.grid(row=1, column=1, columnspan=2)

        self.pin_label = tk.Label(self, text="PIN:")
        self.pin_label.grid(row=2, column=0)

        self.pin_entry = tk.Entry(self, show="*")
        self.pin_entry.grid(row=2, column=1, columnspan=2)

        self.login_button = tk.Button(self, text="Sign in", command=self.handle_login)
        self.login_button.configure(bg="#19A7CE")
        self.login_button.grid(row=3, column=1)

        self.clear_button = tk.Button(self, text="Clear", command=self.handle_clear)
        self.clear_button.configure(bg="#19A7CE")
        self.clear_button.grid(row=3, column=2)

        self.signup_button = tk.Button(self, text="Sign up", command=self.handle_signup)
        self.signup_button.configure(bg="#19A7CE")
        self.signup_button.grid(row=4, column=0, columnspan=3)

        self.error_messages_text = tk.Label(self, text="", fg="firebrick")
        self.error_messages_text.grid(row=5, column=0, columnspan=3, pady=10)

    def set_error_message(self, error_message):
        self.error_messages_text.config(text=error_message)

    def handle_signup(self):
        # Take to Signup screen
        self.master.destroy()
        Signup(self.data).mainloop()

    def handle_clear(self):
        self.card_entry.delete(0, tk.END)
        self.pin_entry.delete(0, tk.END)

    def handle_login(self):
        card_num = self.card_entry.get().strip()
        pin = self.pin_entry.get().strip()

        account = self.data.get_account_by_card_number_and_pin(card_num, pin)
        if account is None:
            self.set_error_message("Credentials don't match. Please try again.")
        else:
            self.set_error_message("")

            # Change the scene to user home
            self.master.destroy()
            UserHome(self.data, account).mainloop()

class Signup(tk.Frame):
    def __init__(self, data):
        super().__init__()

        self.data = data

        self.configure(bg="#D8D8D8")
        self.grid()

        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self, text="Create an Account", font=("Tahoma", 20))
        self.title_label.grid(row=0, column=0, columnspan=3)

        self.name_label = tk.Label(self, text="Name:")
        self.name_label.grid(row=1, column=0)

        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=1, column=1, columnspan=2)

        self.address_label = tk.Label(self, text="Address:")
        self.address_label.grid(row=2, column=0)

        self.address_entry = tk.Entry(self)
        self.address_entry.grid(row=2, column=1, columnspan=2)

        self.ssn_label = tk.Label(self, text="SSN:")
        self.ssn_label.grid(row=3, column=0)

        self.ssn_entry = tk.Entry(self)
        self.ssn_entry.grid(row=3, column=1, columnspan=2)

        self.deposit_label = tk.Label(self, text="Deposit Amount:")
        self.deposit_label.grid(row=4, column=0)

        self.deposit_entry = tk.Entry(self)
        self.deposit_entry.grid(row=4, column=1, columnspan=2)

        self.create_button = tk.Button(self, text="Create Account", command=self.handle_create)
        self.create_button.configure(bg="#19A7CE")
        self.create_button.grid(row=5, column=1)

        self.login_button = tk.Button(self, text="Go to Login page", command=self.handle_login)
        self.login_button.configure(bg="#19A7CE")
        self.login_button.grid(row=5, column=2)

        self.error_messages_text = tk.Label(self, text="", fg="firebrick")
        self.error_messages_text.grid(row=6, column=0, columnspan=3, pady=10)

    def set_error_message(self, error_message):
        self.error_messages_text.config(text=error_message)

    def handle_create(self):
        name = self.name_entry.get().strip()
        address = self.address_entry.get().strip()
        ssn = self.ssn_entry.get().strip()
        deposit_amt_str = self.deposit_entry.get().strip()

        # Validate inputs
        if len(name) == 0:
            self.set_error_message("Name can't be empty")
            return

        if len(address) == 0:
            self.set_error_message("Address can't be empty")
            return

        if len(ssn) != 9 or not ssn.isdigit():
            self.set_error_message("SSN should have exactly 9 digits and contain digits only")
            return

        try:
            deposit_amt = float(deposit_amt_str)
            if deposit_amt < 200:
                self.set_error_message("Deposit amount must be at least 200")
                return
        except ValueError:
            self.set_error_message("Deposit amount should be a number, and at least 200")
            return

        self.set_error_message("")

        # Create a new account
        new_account = self.data.create_new_account_for(name, address, ssn, deposit_amt)

        messagebox.showinfo("Account creation successful",
                            f"Please note down the following details for further use:\n"
                            f"Your 12 digit card number is: {new_account.card_num}\n"
                            f"Your 4 digit pin is: {new_account.pin}")

        # Take to user home screen
        self.master.destroy()
        UserHome(self.data, new_account).mainloop()

    def handle_login(self):
        # Take to login screen
        self.master.destroy()
        Login(self.data).mainloop()



class TransactionHistory(tk.Frame):
    def __init__(self, data, account):
        super().__init__()

        self.data = data
        self.account = account

        self.configure(bg="#D8D8D8")
        self.grid()

        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self, text="Transfer History:", font=("Tahoma", 20))
        title_label.grid(row=0, column=0, columnspan=2)

        account_name_label = tk.Label(self, text="Account name: " + self.account.name)
        account_name_label.grid(row=1, column=0)

        card_number_label = tk.Label(self, text="Card number: " + self.account.card_num)
        card_number_label.grid(row=2, column=0)

        transaction_history = tk.Text(self, wrap=tk.WORD, height=10, width=40)
        transaction_history.grid(row=3, column=0, columnspan=2)

        btn_home = tk.Button(self, text="Go to home", command=self.handle_home)
        btn_home.configure(bg="#19A7CE")
        btn_home.grid(row=4, column=0)

        # Fill transactions
        my_transactions = self.data.get_transactions_by_card_number(self.account.card_num)
        if not my_transactions:
            transaction_history.insert(tk.END, "No transactions yet for this account")
        else:
            transaction_history.insert(tk.END, "Transactions from recent to oldest:\n")
            for i, transaction in enumerate(my_transactions, 1):
                transaction_history.insert(tk.END, f"{i}) {transaction.type_of_transaction}")

                if transaction.type_of_transaction == "Transfer":
                    if self.account.card_num == transaction.src_card_num:
                        transaction_history.insert(tk.END, f" To {transaction.dst_card_num}")
                    else:
                        transaction_history.insert(tk.END, f" From {transaction.src_card_num}")

                transaction_history.insert(tk.END, f" Amount: {transaction.amount}\n")

        transaction_history.config(state=tk.DISABLED)

    def handle_home(self):
        # Take to user home screen
        self.master.destroy()
        UserHome(self.data, self.account).mainloop()

class Transfer(tk.Frame):
    def __init__(self, data, account):
        super().__init__()

        self.data = data
        self.account = account

        self.configure(bg="#D8D8D8")
        self.grid()

        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self, text="Transfer:", font=("Tahoma", 20))
        title_label.grid(row=0, column=0, columnspan=2)

        balance_label = tk.Label(self, text="Your balance is:")
        balance_label.grid(row=1, column=0)

        balance_value_label = tk.Label(self, text=str(self.account.balance))
        balance_value_label.grid(row=1, column=1, columnspan=2)

        recipient_label = tk.Label(self, text="Card number of recipient:")
        recipient_label.grid(row=2, column=0)

        self.recipient_card_number_entry = tk.Entry(self)
        self.recipient_card_number_entry.grid(row=2, column=1, columnspan=2)

        amount_label = tk.Label(self, text="Amount:")
        amount_label.grid(row=3, column=0)

        self.amount_entry = tk.Entry(self)
        self.amount_entry.grid(row=3, column=1, columnspan=2)

        btn_proceed = tk.Button(self, text="Transfer", command=self.handle_transfer)
        btn_proceed.configure(bg="#19A7CE")
        btn_proceed.grid(row=4, column=1)

        btn_cancel = tk.Button(self, text="Cancel", command=self.handle_cancel)
        btn_cancel.configure(bg="#19A7CE")
        btn_cancel.grid(row=4, column=2)

        self.error_messages_text = tk.Label(self, text="", fg="firebrick")
        self.error_messages_text.grid(row=5, column=0, columnspan=3, pady=10)

    def set_error_message(self, error_message):
        self.error_messages_text.config(text=error_message)

    def handle_transfer(self):
        recipient_card_number = self.recipient_card_number_entry.get().strip()
        recipient_account = self.data.get_account_by_card_number(recipient_card_number)

        if not recipient_account:
            self.set_error_message("Recipient card number doesn't exist")
            return

        if recipient_account.card_num == self.account.card_num:
            self.set_error_message("Transferring to own account is not useful")
            return

        try:
            transfer_amount = float(self.amount_entry.get().strip())
        except ValueError:
            self.set_error_message("Please enter a valid number greater than 0 for transfer amount")
            return

        if transfer_amount < 0:
            self.set_error_message("Transfer amount can't be negative")
            return

        if transfer_amount > self.account.balance:
            self.set_error_message("Transfer amount can't be more than account balance")
            return

        self.account.balance -= transfer_amount
        recipient_account.balance += transfer_amount

        self.data.transactions.append(
            Transaction(Transaction.TYPE_TRANSFER, self.account.card_num, recipient_account.card_num, transfer_amount)
        )

        messagebox.showinfo("Success",
                            f"Transfer of {transfer_amount} success!\nYour new balance is {self.account.balance}\n"
                            f"Amount credited to {recipient_account.card_num}")

        # Take to user home screen
        self.master.destroy()
        UserHome(self.data, self.account).mainloop()

    def handle_cancel(self):
        # Take to user home screen
        self.master.destroy()
        UserHome(self.data, self.account).mainloop()

class Withdraw(tk.Frame):
    def __init__(self, data, account):
        super().__init__()

        self.data = data
        self.account = account

        self.configure(bg="#D8D8D8")
        self.grid()

        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self, text="Withdraw:", font=("Tahoma", 20))
        title_label.grid(row=0, column=0, columnspan=2)

        balance_label = tk.Label(self, text="Your balance is:")
        balance_label.grid(row=1, column=0)

        balance_value_label = tk.Label(self, text=str(self.account.balance))
        balance_value_label.grid(row=1, column=1, columnspan=2)

        withdraw_label = tk.Label(self, text="Withdraw amount:")
        withdraw_label.grid(row=2, column=0)

        self.withdraw_amount_entry = tk.Entry(self)
        self.withdraw_amount_entry.grid(row=2, column=1, columnspan=2)

        btn_proceed = tk.Button(self, text="Withdraw", command=self.handle_withdraw)
        btn_proceed.configure(bg="#19A7CE")
        btn_proceed.grid(row=3, column=1)

        btn_cancel = tk.Button(self, text="Cancel", command=self.handle_cancel)
        btn_cancel.configure(bg="#19A7CE")
        btn_cancel.grid(row=3, column=2)

        self.error_messages_text = tk.Label(self, text="", fg="firebrick")
        self.error_messages_text.grid(row=4, column=0, columnspan=2, pady=10)

    def set_error_message(self, error_message):
        self.error_messages_text.config(text=error_message)

    def handle_withdraw(self):
        try:
            withdraw_amount = float(self.withdraw_amount_entry.get().strip())
        except ValueError:
            self.set_error_message("Please enter a valid number greater than 0 for withdraw amount")
            return

        if withdraw_amount < 0:
            self.set_error_message("Withdraw amount can't be negative")
            return

        if withdraw_amount > self.account.balance:
            self.set_error_message("Can't withdraw more than account balance.")
            return

        self.account.balance -= withdraw_amount

        self.data.transactions.append(
            Transaction(Transaction.TYPE_WITHDRAW, self.account.card_num, self.account.card_num, withdraw_amount)
        )

        messagebox.showinfo("Success", f"Withdraw of {withdraw_amount} success!\nYour new balance is {self.account.balance}")

        # Take to user home screen
        self.master.destroy()
        UserHome(self.data, self.account).mainloop()

    def handle_cancel(self):
        # Take to user home screen
        self.master.destroy()
        UserHome(self.data, self.account).mainloop()

class UserHome(tk.Frame):
    def __init__(self, data, account):
        super().__init__()

        self.data = data
        self.account = account

        self.configure(bg="#D8D8D8")
        self.grid()

        self.create_widgets()

    def create_widgets(self):
        scenetitle = tk.Label(self, text="Hi " + self.account.name + "!", font=("Tahoma", 20))
        scenetitle.grid(row=0, column=0, pady=(0, 10))

        btn_transaction_history = tk.Button(self, text="Transaction History", command=self.handle_transaction_history)
        btn_transaction_history.configure(bg="#19A7CE")
        btn_transaction_history.grid(row=1, column=0, sticky="nsew")

        btn_check_balance = tk.Button(self, text="Check Balance", command=self.handle_check_balance)
        btn_check_balance.configure(bg="#19A7CE")
        btn_check_balance.grid(row=2, column=0, sticky="nsew")

        btn_withdraw = tk.Button(self, text="Withdraw", command=self.handle_withdraw)
        btn_withdraw.configure(bg="#19A7CE")
        btn_withdraw.grid(row=3, column=0, sticky="nsew")

        btn_deposit = tk.Button(self, text="Deposit", command=self.handle_deposit)
        btn_deposit.configure(bg="#19A7CE")
        btn_deposit.grid(row=4, column=0, sticky="nsew")

        btn_transfer = tk.Button(self, text="Transfer", command=self.handle_transfer)
        btn_transfer.configure(bg="#19A7CE")
        btn_transfer.grid(row=5, column=0, sticky="nsew")

        btn_quit = tk.Button(self, text="Quit", command=self.handle_quit)
        btn_quit.configure(bg="#19A7CE")
        btn_quit.grid(row=6, column=0, sticky="nsew")

        for i in range(1, 7):
            self.grid_rowconfigure(i, weight=1)

    def handle_transaction_history(self):
        # take to transaction history screen
        self.destroy()
        TransactionHistory(self.data, self.account).mainloop()

    def handle_check_balance(self):
        messagebox.showinfo("Balance", "Hi " + self.account.name + "\nYour balance is " + str(self.account.balance))

    def handle_withdraw(self):
        # take to withdraw screen
        self.destroy()
        Withdraw(self.data, self.account).mainloop()

    def handle_deposit(self):
        # take to deposit screen
        self.destroy()
        Deposit(self.data, self.account).mainloop()

    def handle_transfer(self):
        # take to transfer screen
        self.destroy()
        Transfer(self.data, self.account).mainloop()

    def handle_quit(self):
        result = messagebox.askyesno("Quit", "Are you sure to quit?")
        if result:
            # take to login screen
            self.destroy()
            Login(self.data).mainloop()

class AutomatedTellerMachineApp:
    def __init__(self):
        self.data = Data()
        self.data.read_from_text_file()

        self.root = tk.Tk()
        self.root.title("Automated Teller Machine")

        self.login_screen = Login(self.data)
        self.login_screen.grid(row=0, column=0)

        self.root.mainloop()

    def on_closing(self):
        try:
            self.data.save_to_text_file()
        except Exception as e:
            print("Some error occurred while saving data at the end of the application.")
            print(f"Error message: {e}")

if __name__ == "__main__":
    app = AutomatedTellerMachineApp()
    app.on_closing()

