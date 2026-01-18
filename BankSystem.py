import csv
import os
import base64
from datetime import datetime
import getpass
import time

class BankingSystem:
    def __init__(self):
        self.bank_folder = 'bank_data'
        self.users_file_path = os.path.join(self.bank_folder, 'users.csv')
        self.transactions_file_path = os.path.join(self.bank_folder, 'transactions.csv')
        self.current_active_user = None
        self.setupFiles()

    def logo(self):
        print(r"""
╔════════════════════════════════════════════════════════════════════════╗
    /$$$$$$  /$$$$$$$   /$$$$$$        /$$$$$$$   /$$$$$$  /$$   /$$ /$$   /$$
  /$$__  $$| $$__  $$ /$$__  $$      | $$__  $$ /$$__  $$| $$$ | $$| $$  /$$/
 | $$  \ $$| $$  \ $$| $$  \__/      | $$  \ $$| $$  \ $$| $$$$| $$| $$ /$$/ 
 | $$$$$$$$| $$$$$$$ | $$            | $$$$$$$ | $$$$$$$$| $$ $$ $$| $$$$$/  
 | $$__  $$| $$__  $$| $$            | $$__  $$| $$__  $$| $$  $$$$| $$  $$  
 | $$  | $$| $$  \ $$| $$    $$      | $$  \ $$| $$  | $$| $$\  $$$| $$\  $$ 
 | $$  | $$| $$$$$$$/|  $$$$$$/      | $$$$$$$/| $$  | $$| $$ \  $$| $$ \  $$
 |__/  |__/|_______/  \______/       |_______/ |__/  |__/|__/  \__/|__/  \__/
                             Made by 707                                                                            
╚════════════════════════════════════════════════════════════════════════╝
        """)

    def sectionHeader(self, title_text):
        print(f"\n┌{'─' * 58}┐")
        print(f"│ {title_text:^56} │")
        print(f"└{'─' * 58}┘")

    def successMsg(self, message_text):
        print(f"\n┌{'─' * 58}┐")
        print(f"│ {'✅ SUCCESS':^56}│")
        print(f"│ {message_text:^56} │")
        print(f"└{'─' * 58}┘")

    def errorMsg(self, error_text):
        print(f"\n┌{'─' * 58}┐")
        print(f"│ {'❌ ERROR':^56}│")
        print(f"│ {error_text:^56} │")
        print(f"└{'─' * 58}┘")

    def infoMsg(self, info_text):
        print(f"\n┌{'─' * 58}┐")
        print(f"│ {'ℹ️  INFORMATION':^56}  │")
        print(f"│ {info_text:^56} │")
        print(f"└{'─' * 58}┘")

    def receipt(self, transaction_type, transaction_amount, account_balance, transaction_details=""):
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
        print(f"""
┌──────────────────────────────────────────────────────────┐
│                    TRANSACTION RECEIPT                   │
├──────────────────────────────────────────────────────────┤
  Type:       {transaction_type:<40} 
  Amount:     ${transaction_amount:>38.2f} 
  Balance:    ${account_balance:>38.2f} 
  Date:       {formatted_time:<40} 
  Details:    {transaction_details:<40} 
└──────────────────────────────────────────────────────────┘
        """)

    def balanceShow(self, username_display, balance_amount):
        current_time_display = datetime.now().strftime("%Y-%m-%d %H:%M")
        print(f"""
┌──────────────────────────────────────────────────────────┐
│                       ACCOUNT BALANCE                    │
├──────────────────────────────────────────────────────────┤
  Account:    {username_display:<40} 
  Balance:    ${balance_amount:>38.2f} 
  As of:      {current_time_display:<40} 
└──────────────────────────────────────────────────────────┘
        """)

    def processing(self, process_message="Processing"):
        print(f"\n⏳ {process_message}", end="", flush=True)
        for _ in range(3):
            time.sleep(0.3)
            print("▪", end="", flush=True)
        print(" ✅")

    def checkUser(self, username_to_check):
        account_list = self.getAccounts()
        for account_record in account_list:
            if account_record['username'] == username_to_check:
                return True
        return False

    def getBal(self, username_for_balance):
        user_record = self.getUser(username_for_balance)
        if user_record:
            return user_record['balance']
        else:
            return 0.0

    def setBalance(self, user_to_update, new_balance_value):
        self.updateBalance(user_to_update, new_balance_value)

    def addTrans(self, trans_username, trans_type, trans_amount, trans_balance, trans_description=""):
        self.saveTrans(trans_username, trans_type, trans_amount, trans_balance, trans_description)

    def hidePass(self, plain_password):
        encoded_bytes = base64.b64encode(plain_password.encode())
        encoded_string = encoded_bytes.decode()
        return encoded_string

    def revealPass(self, encoded_password):
        try:
            decoded_bytes = base64.b64decode(encoded_password.encode())
            decoded_string = decoded_bytes.decode()
            return decoded_string
        except Exception as e:
            return None

    def setupFiles(self):
        if not os.path.isdir(self.bank_folder):
            os.mkdir(self.bank_folder)

        if not os.path.isfile(self.users_file_path):
            with open(self.users_file_path, 'w', newline='') as file_handle:
                csv_writer = csv.writer(file_handle)
                csv_writer.writerow(['username', 'password', 'balance'])

        if not os.path.isfile(self.transactions_file_path):
            with open(self.transactions_file_path, 'w', newline='') as file_handle:
                csv_writer = csv.writer(file_handle)
                csv_writer.writerow(['username', 'date', 'type', 'amount', 'balance', 'details'])

    def getAccounts(self):
        accounts_collection = []
        try:
            if os.path.isfile(self.users_file_path):
                with open(self.users_file_path, 'r') as file_handle:
                    csv_reader = csv.DictReader(file_handle)
                    for row_data in csv_reader:
                        if 'username' in row_data and 'password' in row_data and 'balance' in row_data:
                            try:
                                row_data['balance'] = float(row_data['balance'])
                                accounts_collection.append(row_data)
                            except ValueError:
                                continue
        except Exception as err:
            print("Problem reading account data: " + str(err))
        return accounts_collection

    def getTrans(self):
        transactions_list = []
        try:
            if os.path.isfile(self.transactions_file_path):
                with open(self.transactions_file_path, 'r') as file_handle:
                    csv_reader = csv.DictReader(file_handle)
                    for row_data in csv_reader:
                        required_fields = ['username', 'date', 'type', 'amount', 'balance', 'details']
                        if all(field in row_data for field in required_fields):
                            try:
                                row_data['amount'] = float(row_data['amount'])
                                row_data['balance'] = float(row_data['balance'])
                                transactions_list.append(row_data)
                            except ValueError:
                                continue
        except Exception as err:
            print("Problem reading transaction data: " + str(err))
        return transactions_list

    def storeAccounts(self, accounts_to_save):
        try:
            with open(self.users_file_path, 'w', newline='') as file_handle:
                csv_writer = csv.writer(file_handle)
                csv_writer.writerow(['username', 'password', 'balance'])
                for account_item in accounts_to_save:
                    csv_writer.writerow([account_item['username'], account_item['password'], account_item['balance']])
        except Exception as err:
            print("Problem saving account data: " + str(err))

    def storeTrans(self, transactions_to_save):
        try:
            with open(self.transactions_file_path, 'w', newline='') as file_handle:
                csv_writer = csv.writer(file_handle)
                csv_writer.writerow(['username', 'date', 'type', 'amount', 'balance', 'details'])
                for transaction_item in transactions_to_save:
                    csv_writer.writerow([
                        transaction_item['username'],
                        transaction_item['date'],
                        transaction_item['type'],
                        transaction_item['amount'],
                        transaction_item['balance'],
                        transaction_item['details']
                    ])
        except Exception as err:
            print("Problem saving transaction data: " + str(err))

    def getUser(self, username_to_find):
        account_records = self.getAccounts()
        for account_data in account_records:
            if account_data['username'] == username_to_find:
                return account_data
        return None

    def updateBalance(self, username_for_update, updated_balance):
        account_records = self.getAccounts()
        for account_data in account_records:
            if account_data['username'] == username_for_update:
                account_data['balance'] = updated_balance
        self.storeAccounts(account_records)
        if self.current_active_user and self.current_active_user['username'] == username_for_update:
            self.current_active_user['balance'] = updated_balance

    def saveTrans(self, trans_user, trans_kind, trans_value, trans_bal, trans_desc=""):
        transaction_records = self.getTrans()
        
        new_transaction_record = {
            'username': trans_user,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'type': trans_kind,
            'amount': trans_value,
            'balance': trans_bal,
            'details': trans_desc
        }
        
        transaction_records.append(new_transaction_record)
        self.storeTrans(transaction_records)

    def userTrans(self, target_username):
        all_transactions = self.getTrans()
        user_transactions = []
        for transaction_item in all_transactions:
            if transaction_item['username'] == target_username:
                user_transactions.append(transaction_item)
        return user_transactions

    def newAccount(self):
        self.sectionHeader("CREATE NEW ACCOUNT")
        
        full_name_input = input(" Enter full name: ").strip()
        if len(full_name_input) == 0:
            self.errorMsg("Name cannot be empty!")
            return
        
        chosen_username = input(" Choose username: ").strip()
        if not chosen_username:
            self.errorMsg("Username cannot be empty!")
            return
        
        if self.checkUser(chosen_username):
            self.errorMsg("Username already exists!")
            return
        
        password_input = getpass.getpass(" Set password: ")
        if not password_input:
            self.errorMsg("Password cannot be empty!")
            return
        
        confirm_password = getpass.getpass(" Confirm password: ")
        if password_input != confirm_password:
            self.errorMsg("Passwords do not match!")
            return
        
        account_type_selection = input(" Account type (Savings/Current): ").strip().capitalize()
        if account_type_selection not in ['Savings', 'Current']:
            account_type_selection = 'Savings'
        
        try:
            initial_deposit_amount = float(input(" Initial deposit amount: $"))
            if initial_deposit_amount < 0:
                self.errorMsg("Initial deposit cannot be negative!")
                return
        except ValueError:
            self.errorMsg("Invalid amount!")
            return
        
        encrypted_password = self.hidePass(password_input)
        
        new_account_data = {
            'username': chosen_username,
            'password': encrypted_password,
            'balance': initial_deposit_amount
        }
        
        existing_accounts = self.getAccounts()
        existing_accounts.append(new_account_data)
        self.storeAccounts(existing_accounts)
        
        self.addTrans(chosen_username, 'ACCOUNT_CREATION', initial_deposit_amount, initial_deposit_amount, 'Initial deposit')
        
        self.successMsg("Account created successfully!")
        print(f"┌{'─' * 58}┐")
        print(f"│ {'Account Details':^56} │")
        print(f"├{'─' * 58}┤")
        print(f" Username: {chosen_username:<45} ")
        print(f" Full Name: {full_name_input:<44} ")
        print(f" Account Type: {account_type_selection:<41} ")
        print(f" Initial Balance: ${initial_deposit_amount:>36.2f} ")
        print(f"└{'─' * 58}┘")

    def doLogin(self):
        self.sectionHeader("ACCOUNT LOGIN")
        
        input_username = input(" Username: ").strip()
        input_password = getpass.getpass(" Password: ")
        
        user_data = self.getUser(input_username)
        if user_data:
            stored_password_decoded = self.revealPass(user_data['password'])
            if stored_password_decoded and stored_password_decoded == input_password:
                self.current_active_user = user_data
                self.processing("Authenticating")
                self.successMsg("Welcome back, " + input_username + "!")
                return True
        
        self.errorMsg("Invalid username or password!")
        return False

    def doLogout(self):
        if self.current_active_user:
            self.infoMsg("Goodbye, " + self.current_active_user['username'] + "!")
            self.current_active_user = None

    def viewBalance(self):
        if not self.current_active_user:
            self.errorMsg("Please login first!")
            return
        
        self.balanceShow(self.current_active_user['username'], self.current_active_user['balance'])

    def doDeposit(self):
        if not self.current_active_user:
            self.errorMsg("Please login first!")
            return
        
        self.sectionHeader("DEPOSIT FUNDS")
        
        try:
            deposit_value = float(input(" Enter deposit amount: $"))
            if deposit_value <= 0:
                self.errorMsg("Deposit amount must be positive!")
                return
            
            deposit_description = input(" Enter description (optional): ").strip()
            
            self.processing("Processing deposit")
            updated_balance_value = self.current_active_user['balance'] + deposit_value
            self.setBalance(self.current_active_user['username'], updated_balance_value)
            
            self.addTrans(
                self.current_active_user['username'],
                'DEPOSIT',
                deposit_value,
                updated_balance_value,
                deposit_description or 'Cash deposit'
            )
            
            self.receipt('DEPOSIT', deposit_value, updated_balance_value, deposit_description or 'Cash deposit')
            
        except ValueError:
            self.errorMsg("Invalid amount!")

    def doWithdraw(self):
        if not self.current_active_user:
            self.errorMsg("Please login first!")
            return
        
        self.sectionHeader("WITHDRAW FUNDS")
        
        try:
            withdrawal_value = float(input(" Enter withdrawal amount: $"))
            if withdrawal_value <= 0:
                self.errorMsg("Withdrawal amount must be positive!")
                return
            
            if withdrawal_value > self.current_active_user['balance']:
                self.errorMsg("Insufficient funds!")
                return
            
            withdrawal_description = input(" Enter description (optional): ").strip()
            
            self.processing("Processing withdrawal")
            new_balance_after_withdrawal = self.current_active_user['balance'] - withdrawal_value
            self.setBalance(self.current_active_user['username'], new_balance_after_withdrawal)
            
            self.addTrans(
                self.current_active_user['username'],
                'WITHDRAWAL',
                withdrawal_value,
                new_balance_after_withdrawal,
                withdrawal_description or 'Cash withdrawal'
            )
            
            self.receipt('WITHDRAWAL', withdrawal_value, new_balance_after_withdrawal, withdrawal_description or 'Cash withdrawal')
            
        except ValueError:
            self.errorMsg("Invalid amount!")

    def doTransfer(self):
        if not self.current_active_user:
            self.errorMsg("Please login first!")
            return
        
        self.sectionHeader("FUNDS TRANSFER")
        
        try:
            recipient_username = input(" Enter recipient username: ").strip()
            transfer_amount = float(input(" Enter transfer amount: $"))
            
            if transfer_amount <= 0:
                self.errorMsg("Transfer amount must be positive!")
                return
            
            if transfer_amount > self.current_active_user['balance']:
                self.errorMsg("Insufficient funds!")
                return
            
            if recipient_username == self.current_active_user['username']:
                self.errorMsg("Cannot transfer to your own account!")
                return
            
            recipient_user_data = self.getUser(recipient_username)
            if not recipient_user_data:
                self.errorMsg("Recipient account not found!")
                return
            
            transfer_description = input(" Enter transfer description: ").strip()
            
            self.processing("Processing transfer")
            sender_new_balance = self.current_active_user['balance'] - transfer_amount
            self.setBalance(self.current_active_user['username'], sender_new_balance)
            
            recipient_new_balance = recipient_user_data['balance'] + transfer_amount
            self.setBalance(recipient_username, recipient_new_balance)
            
            self.addTrans(
                self.current_active_user['username'],
                'TRANSFER_OUT',
                transfer_amount,
                sender_new_balance,
                "Transfer to " + recipient_username + ": " + transfer_description
            )
            
            self.addTrans(
                recipient_username,
                'TRANSFER_IN',
                transfer_amount,
                recipient_new_balance,
                "Transfer from " + self.current_active_user['username'] + ": " + transfer_description
            )
            
            self.receipt('TRANSFER_OUT', transfer_amount, sender_new_balance, "To: " + recipient_username)
            self.successMsg("Transfer completed to " + recipient_username)
            
        except ValueError:
            self.errorMsg("Invalid amount!")

    def viewHistory(self):
        if not self.current_active_user:
            self.errorMsg("Please login first!")
            return
        
        user_transaction_history = self.userTrans(self.current_active_user['username'])
        
        self.sectionHeader("TRANSACTION HISTORY")
        print(f"  Account: {self.current_active_user['username']:49} ")
        print(f"├{'─' * 58}┤")
        
        if len(user_transaction_history) == 0:
            print(f"│ {'No transactions found.':^56} │")
            print(f"└{'─' * 58}┘")
            return
        
        recent_transactions = user_transaction_history[-15:]
        
        for transaction_item in reversed(recent_transactions):
            transaction_date = transaction_item['date']
            transaction_type = transaction_item['type']
            transaction_amount = transaction_item['amount']
            transaction_balance = transaction_item['balance']
            transaction_details = transaction_item['details']
            
            arrow_symbol = "↗ " if transaction_type in ['DEPOSIT', 'TRANSFER_IN', 'ACCOUNT_CREATION'] else "↘ "
            color_indicator = "🟢" if transaction_type in ['DEPOSIT', 'TRANSFER_IN', 'ACCOUNT_CREATION'] else "🔴"
            
            print(f" {color_indicator} {transaction_date:16} {transaction_type:12} {arrow_symbol}${transaction_amount:8.2f} ")
            print(f"   Balance: ${transaction_balance:8.2f} {transaction_details[:30]:30} ")
            print(f"├{'─' * 58}┤")
        
        print(f"└{'─' * 58}┘")

    def changePass(self):
        if not self.current_active_user:
            self.errorMsg("Please login first!")
            return
        
        self.sectionHeader("CHANGE PASSWORD")
        
        current_password_input = getpass.getpass(" Enter current password: ")
        if current_password_input != self.revealPass(self.current_active_user['password']):
            self.errorMsg("Incorrect current password!")
            return
        
        new_password_input = getpass.getpass(" Enter new password: ")
        if not new_password_input:
            self.errorMsg("Password cannot be empty!")
            return
        
        confirm_new_password = getpass.getpass(" Confirm new password: ")
        if new_password_input != confirm_new_password:
            self.errorMsg("Passwords do not match!")
            return
        
        existing_accounts = self.getAccounts()
        for account_record in existing_accounts:
            if account_record['username'] == self.current_active_user['username']:
                account_record['password'] = self.hidePass(new_password_input)
                self.current_active_user['password'] = account_record['password']
                break
        
        self.storeAccounts(existing_accounts)
        self.successMsg("Password changed successfully!")

    def userMenu(self):
        while True:
            print(f"""
┌──────────────────────────────────────────────────────────┐
│                 CUSTOMER BANKING PORTAL                  │
├──────────────────────────────────────────────────────────┤
  Account: {self.current_active_user['username']:<43} 
  Balance: ${self.current_active_user['balance']:>38.2f} 
├──────────────────────────────────────────────────────────┤
  1. 💰  Check Balance                                    
  2. 💵  Deposit Money                                    
  3. 💸  Withdraw Money                                   
  4. 🔄  Transfer Money                                   
  5. 📜  Transaction History                              
  6. 🔒  Change Password                                  
  7. 🚪  Logout                                           
└──────────────────────────────────────────────────────────┘
            """)
            
            user_choice = input(" Select option (1-7): ").strip()
            
            if user_choice == '1':
                self.viewBalance()
            elif user_choice == '2':
                self.doDeposit()
            elif user_choice == '3':
                self.doWithdraw()
            elif user_choice == '4':
                self.doTransfer()
            elif user_choice == '5':
                self.viewHistory()
            elif user_choice == '6':
                self.changePass()
            elif user_choice == '7':
                self.doLogout()
                break
            else:
                self.errorMsg("Invalid selection!")

    def adminScreen(self):
        while True:
            print(f"""
┌──────────────────────────────────────────────────────────┐
│                      ADMIN DASHBOARD                     │
├──────────────────────────────────────────────────────────┤
  1. 👥  View All Accounts                                
  2. 📋  View All Transactions                            
  3. 📊  System Statistics                                
  4. 🔍  Search Account                                   
  5. ↩️   Back to Main Menu                                
└──────────────────────────────────────────────────────────┘
            """)
            
            admin_choice = input("│ Select option (1-5): ").strip()
            
            if admin_choice == '1':
                self.showAllAccounts()
            elif admin_choice == '2':
                self.showAllTrans()
            elif admin_choice == '3':
                self.showStats()
            elif admin_choice == '4':
                self.findAccount()
            elif admin_choice == '5':
                break
            else:
                self.errorMsg("Invalid selection!")

    def showAllAccounts(self):
        account_collection = self.getAccounts()
        
        self.sectionHeader("ALL ACCOUNTS")
        
        if not account_collection:
            print(f"│ {'No accounts found.':^56} │")
            print(f"├{'─' * 58}├")
            return
        
        print(f"│ {'Username':15} {'Balance':>12} {'':27} │")
        print(f"├{'─' * 58}┤")
        
        total_balance_sum = 0
        for account_item in account_collection:
            print(f"  {account_item['username']:15} ${account_item['balance']:>10.2f} {'':27} ")
            total_balance_sum += account_item['balance']
        
        print(f"├{'─' * 58}┤")
        print(f"  Total Accounts: {len(account_collection):<38} ")
        print(f"  Total Balance: ${total_balance_sum:>37.2f} ")
        print(f"└{'─' * 58}┘")

    def showAllTrans(self):
        transaction_collection = self.getTrans()
        
        self.sectionHeader("ALL TRANSACTIONS")
        
        if not transaction_collection:
            print(f"│ {'No transactions found.':^56} │")
            print(f"├{'─' * 58}├")
            return
        
        recent_transactions = transaction_collection[-20:]
        
        for transaction_item in reversed(recent_transactions):
            transaction_time = transaction_item['date'][11:16]
            transaction_user = transaction_item['username']
            transaction_type = transaction_item['type']
            transaction_amount = transaction_item['amount']
            transaction_balance = transaction_item['balance']
            transaction_details = transaction_item['details'][:20]
            
            direction_symbol = "↗ " if transaction_type in ['DEPOSIT', 'TRANSFER_IN', 'ACCOUNT_CREATION'] else "↘ "
            
            print(f" {transaction_time:5} {transaction_user:12} {transaction_type:12} {direction_symbol}${transaction_amount:7.2f} ")
            print(f" {transaction_details:20} Balance: ${transaction_balance:7.2f} {'':15} ")
            print(f"├{'─' * 58}┤")
        
        print(f"└{'─' * 58}┘")

    def showStats(self):
        account_collection = self.getAccounts()
        transaction_collection = self.getTrans()
        
        if not account_collection:
            self.errorMsg("No accounts in the system.")
            return
        
        total_balance_calc = sum(account_record['balance'] for account_record in account_collection)
        average_balance_calc = total_balance_calc / len(account_collection)
        
        self.sectionHeader("SYSTEM STATISTICS")
        print(f" Total Accounts: {len(account_collection):<41} ")
        print(f" Total Balance: ${total_balance_calc:>38.2f} ")
        print(f" Average Balance: ${average_balance_calc:>36.2f} ")
        
        balance_values = [account_record['balance'] for account_record in account_collection]
        print(f" Highest Balance: ${max(balance_values):>36.2f} ")
        print(f" Lowest Balance: ${min(balance_values):>37.2f} ")
        
        print(f" Total Transactions: {len(transaction_collection):<36} ")
        print(f"└{'─' * 58}┘")

    def findAccount(self):
        self.sectionHeader("SEARCH ACCOUNT")
        
        search_term = input(" Enter username to search: ").strip().lower()
        
        account_collection = self.getAccounts()
        if not account_collection:
            self.errorMsg("No accounts found.")
            return
        
        search_results = []
        for account_record in account_collection:
            if search_term in account_record['username'].lower():
                search_results.append(account_record)
        
        if len(search_results) == 0:
            self.errorMsg("No accounts found matching your search.")
            return
        
        self.successMsg("Found " + str(len(search_results)) + " account(s)")
        for account_result in search_results:
            print(f"┌{'─' * 58}┐")
            print(f" Username: {account_result['username']:<46} ")
            print(f" Balance: ${account_result['balance']:>46.2f} ")
            print(f"└{'─' * 58}┘")

    def mainScreen(self):
        while True:
            self.logo()
            print("""
┌──────────────────────────────────────────────────────────┐
│                         MAIN MENU                        │
├──────────────────────────────────────────────────────────┤
  1. 🆕  Create New Account                               
  2. 🔐  Login to Account                                 
  3. 👨‍💼  Admin Dashboard                                
  4. 🚪  Exit System                                      
└──────────────────────────────────────────────────────────┘
            """)
            
            main_choice = input(" Select option (1-4): ").strip()
            
            if main_choice == '1':
                self.newAccount()
            elif main_choice == '2':
                if self.doLogin():
                    self.userMenu()
            elif main_choice == '3':
                self.adminScreen()
            elif main_choice == '4':
                self.successMsg("Thank you for using our Bank System!")
                break
            else:
                self.errorMsg("Invalid selection!")

def initialize():
    system_instance = BankingSystem()
    system_instance.mainScreen()

if __name__ == "__main__":
    initialize()