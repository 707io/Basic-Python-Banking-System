# Console Banking System (Python)

A console-based banking system built in Python. The application allows users to create accounts, securely log in, manage balances, and record transactions using CSV-based persistent storage.

---

## Features

### Customer Banking Portal
- Create a new account with an initial deposit
- Login using username and password
- Check account balance
- Deposit funds (with optional description)
- Withdraw funds (with optional description)
- Transfer funds to another account
- View recent transaction history
- Change account password
- Logout

### Admin Dashboard
- View all accounts
- View all transactions (recent records)
- View system statistics (totals, averages, min/max balances)
- Search accounts by username

### Storage and Logging
- Persistent storage using CSV files
- Automatic initialization of:
  - `bank_data/users.csv`
  - `bank_data/transactions.csv`

---

## Tech Stack

- **Language:** Python 3
- **Storage:** CSV files
- **Libraries:** Python standard library only

---

## Project Structure

```
.
├── BankSystem.py
└── bank_data/
    ├── users.csv
    └── transactions.csv
```

---

## Requirements

- Python 3.8+ recommended
- No third-party packages required

---

## How to Run

### 1) Run the system

```bash
python BankSystem.py
```

### 2) First-time setup

On the first run, the application automatically creates the `bank_data/` folder and initializes the CSV database files if they do not already exist.

---

## Data Files

### `users.csv`
Stores account information:
- `username`
- `password` (Base64-encoded)
- `balance`

### `transactions.csv`
Stores transaction history:
- `username`
- `date`
- `type`
- `amount`
- `balance`
- `details`

---

## Supported Transaction Types

The system records transactions using these types:
- `ACCOUNT_CREATION`
- `DEPOSIT`
- `WITHDRAWAL`
- `TRANSFER_OUT`
- `TRANSFER_IN`

---

## License

This repository is intended for academic and educational use.
