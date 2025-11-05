# 🔐 CipherVault+ - CLI Secured Data Manager

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

**CipherVault+** adalah password manager berbasis CLI dengan enkripsi 2-layer yang aman dan mudah digunakan. Data tersimpan secara lokal dengan enkripsi, tanpa memerlukan koneksi internet.

---

## 📋 Table of Contents

- [Features](#-features)
- [Demo](#-demo)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Technical Details](#-technical-details)
- [Security](#-security)
- [Development](#-development)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## ✨ Features

### Core Features
- 🔒 **2-Layer Encryption** - Caesar Cipher + Base64 encoding untuk keamanan ganda
- 📝 **CRUD Operations** - Create, Read, Update, Delete vault entries
- 🔍 **Search Functionality** - Linear search untuk menemukan entries dengan cepat
- 📊 **Sort Options** - Bubble sort dan built-in sort by title atau date
- 📋 **Audit Logging** - Automatic logging semua aktivitas user
- 👤 **User Authentication** - Register dan login dengan SHA256 password hashing
- 💾 **Local Storage** - Data tersimpan di file .txt lokal (no cloud, full privacy)
- 📈 **Statistics** - View statistics aktivitas dan vault entries

### Security Features
- ✅ Password hashing dengan SHA256
- ✅ 2-layer encryption (Caesar Cipher + Base64)
- ✅ Master password untuk encrypt/decrypt semua entries
- ✅ Input sanitization untuk prevent injection
- ✅ Audit trail untuk security monitoring

### Educational Value
Project ini mengimplementasikan konsep dasar pemrograman:
- **Tipe Data Koleksi**: List, Dictionary, Tuple
- **Fungsi**: Regular functions, recursive functions
- **Searching**: Linear search (manual implementation)
- **Sorting**: Bubble sort (manual) dan built-in sort
- **String Manipulation**: Caesar cipher, parsing, validation

---

## 🎬 Demo

### Welcome Screen
```
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║              🔐  CIPHERVAULT+ v1.0  🔐                  ║
║                                                          ║
║              CLI Secured Data Manager                   ║
║         Password Manager dengan Enkripsi 2-Layer        ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝

Features:
- Enkripsi 2-Layer (Caesar Cipher + Base64)
- CRUD Operations (Create, Read, Update, Delete)
- Search & Sort Algorithms
- Audit Logging System
- Offline & Secure (Data tersimpan lokal)
```

### Main Menu
```
MAIN MENU
──────────────────────────────────────────────────────────
1. Register (Buat akun baru)
2. Login (Masuk ke vault)
3. Exit (Keluar program)

> Pilih menu: _
```

### Vault Dashboard
```
VAULT DASHBOARD - Welcome, dani!
──────────────────────────────────────────────────────────
📊 Total entries: 5

1. Create New Entry
2. View All Entries
3. Search Entry
4. Update Entry
5. Delete Entry
6. Sort Entries
7. View Audit Log
8. Account Statistics
9. Logout

> Pilih menu: _
```

### Example: View Entries
```
YOUR VAULT ENTRIES
──────────────────────────────────────────────────────────
Total: 3 entries

1. [VAULT001] Gmail Account
   Account : dani@gmail.com
   Password: **************
   Notes   : Email utama
   Created : 2025-10-28 10:30:00

2. [VAULT002] Facebook Account
   Account : dani.fb
   Password: *********
   Notes   : Social media
   Created : 2025-10-28 11:00:00

3. [VAULT003] GitHub Account
   Account : dani-dev
   Password: ***********
   Notes   : Developer account
   Created : 2025-10-28 11:30:00
```

---

## 🚀 Installation

### Prerequisites
- Python 3.7 atau lebih tinggi
- No external dependencies (semua built-in modules)

### Steps

1. **Clone repository**
```bash
   git clone https://github.com/yourusername/CipherVault-Plus.git
   cd CipherVault-Plus
```

2. **Buat folder data (otomatis jika belum ada)**
```bash
   mkdir data
```

3. **Run program**
```bash
   python main.py
```

That's it! No pip install required! 🎉

---

## 📖 Usage

### 1. Register User Baru
```bash
> Pilih menu: 1

REGISTER NEW USER
──────────────────────────────────────────────────────────

> Username: dani
> Master Password: MySecurePass123
> Confirm Password: MySecurePass123

✅ User 'dani' berhasil didaftarkan!
```

**Password Requirements:**
- Minimal 8 karakter
- Harus ada huruf BESAR
- Harus ada huruf kecil
- Harus ada angka

### 2. Login
```bash
> Pilih menu: 2

LOGIN
──────────────────────────────────────────────────────────

> Username: dani
> Master Password: MySecurePass123

✅ Login berhasil! Selamat datang, dani!
```

### 3. Create Entry (Tambah Password)
```bash
> Pilih menu: 1

CREATE NEW ENTRY
──────────────────────────────────────────────────────────

Masukkan data entry:
  Title (e.g. Gmail Account): Gmail
  Account/Username: dani@gmail.com
  Password: myGmailPassword123
  Notes (optional): Email utama saya

🔐 Encrypting password...
✅ Entry 'Gmail' berhasil dibuat!
   ID: VAULT001
   Password telah dienkripsi dengan aman.
```

### 4. View Entries (Lihat Password)
```bash
> Pilih menu: 2

YOUR VAULT ENTRIES
──────────────────────────────────────────────────────────

1. [VAULT001] Gmail
   Account : dani@gmail.com
   Password: **************
   ...

> View detail entry? (Enter ID atau 'n'): VAULT001

ENTRY DETAIL
──────────────────────────────────────────────────────────

ID       : VAULT001
Title    : Gmail
Account  : dani@gmail.com
Password : ************** (encrypted)
Notes    : Email utama saya
Created  : 2025-10-28 10:30:00

> Show password? (y/n): y

🔓 Decrypting password...
   Password: myGmailPassword123
```

### 5. Search Entry
```bash
> Pilih menu: 3

SEARCH ENTRIES
──────────────────────────────────────────────────────────

> Enter keyword (title/account): gmail

🔍 Searching for 'gmail'...

Found 1 entries:

1. [VAULT001] Gmail
   Account : dani@gmail.com
   Password: **************
   Notes   : Email utama saya
```

### 6. Sort Entries
```bash
> Pilih menu: 6

SORT ENTRIES
──────────────────────────────────────────────────────────

Sort by:
1. Title (A-Z)
2. Title (Z-A)
3. Date (Newest First)
4. Date (Oldest First)

> Choose sort option: 1

Sorted by: Title (A-Z)

1. [VAULT003] Amazon
2. [VAULT002] Facebook
3. [VAULT001] Gmail
```

### 7. View Audit Log
```bash
> Pilih menu: 7

AUDIT LOG
──────────────────────────────────────────────────────────

View options:
1. My Activities (All)
2. Recent Activities (Last 10)
3. All System Logs

> Choose: 1

Activities for dani
──────────────────────────────────────────────────────────
Total: 8 entries

[2025-10-28 10:30:00] dani - REGISTER
  └─ New user registered

[2025-10-28 10:31:00] dani - LOGIN
  └─ User logged in successfully

[2025-10-28 10:32:00] dani - CREATE
  └─ Created entry: Gmail

[2025-10-28 10:35:00] dani - READ
  └─ Viewed entry: Gmail
```

### 8. Statistics
```bash
> Pilih menu: 8

STATISTICS FOR: DANI
──────────────────────────────────────────────────────────

Total Activities: 12
First Activity  : 2025-10-28 10:30:00
Last Activity   : 2025-10-28 11:45:00

Activity Breakdown:
  • REGISTER    : 1 times
  • LOGIN       : 3 times
  • CREATE      : 4 times
  • READ        : 2 times
  • UPDATE      : 1 times
  • SEARCH      : 1 times

──────────────────────────────────────────────────────────
VAULT STATISTICS
──────────────────────────────────────────────────────────

Total Entries: 5
Latest Entry : Amazon (2025-10-28 11:30:00)
Oldest Entry : Gmail (2025-10-28 10:32:00)
```

---

## 📁 Project Structure
```
CipherVault+/
│
├── main.py              # Entry point & menu utama
├── auth.py              # Authentication system (register/login)
├── crypto.py            # Enkripsi 2-layer (Caesar + Base64)
├── vault.py             # CRUD operations + Search + Sort
├── audit.py             # Audit logging system
├── utils.py             # Helper functions & utilities
│
├── data/
│   ├── users.txt        # User database (username|hash|date)
│   ├── vault.txt        # Vault entries (encrypted passwords)
│   └── audit_log.txt    # Activity logs
│
└── README.md            # Documentation
```

### File Descriptions

| File | Lines | Description |
|------|-------|-------------|
| `main.py` | ~280 | Entry point, menu system, flow control |
| `auth.py` | ~280 | User authentication, SHA256 hashing |
| `crypto.py` | ~200 | Caesar Cipher + Base64 encryption |
| `vault.py` | ~450 | CRUD operations, search, sort algorithms |
| `audit.py` | ~180 | Logging system, statistics |
| `utils.py` | ~250 | Helper functions, ID generator (recursive) |
| **Total** | **~1,640** | **Pure code: ~1,100 lines** |

---

## 🔧 Technical Details

### Encryption Algorithm

**2-Layer Encryption Process:**
```
Plain Password: "MyPassword123"
        ↓
[Layer 1: Caesar Cipher]
- Shift derived from master password
- Character-by-character shift
        ↓
Encrypted (Caesar): "ZjDmeemgjt789"
        ↓
[Layer 2: Base64 Encoding]
- Binary to ASCII conversion
- Obfuscation layer
        ↓
Final Encrypted: "WmpEbWVlbWdqdDc4OQ=="
        ↓
Stored in vault.txt
```

**Decryption Process (Reverse Order):**
```
Encrypted: "WmpEbWVlbWdqdDc4OQ=="
        ↓
[Base64 Decode]
        ↓
[Caesar Decrypt]
        ↓
Plain Password: "MyPassword123"
```

### Data Storage Format

**users.txt** (User database):
```
username|password_hash|created_at
dani|5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8|2025-10-28
```

**vault.txt** (Encrypted passwords):
```
id|username|title|account|encrypted_password|notes|timestamp
VAULT001|dani|Gmail|dani@gmail.com|WmpEbWVl...|Email|2025-10-28 10:30:00
```

**audit_log.txt** (Activity logs):
```
timestamp|username|action|details
2025-10-28 10:30:00|dani|LOGIN|User logged in successfully
2025-10-28 10:32:00|dani|CREATE|Created entry: Gmail
```

### Algorithms Implementation

#### 1. Caesar Cipher (String Manipulation)
```python
def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            shifted = (ord(char) - ascii_offset + shift) % 26
            result += chr(shifted + ascii_offset)
        else:
            result += char
    return result
```

**Complexity:** O(n) - linear time

#### 2. Linear Search (Searching)
```python
def search_entries(username, keyword):
    results = []
    keyword_lower = keyword.lower()
    
    for entry in entries:
        if keyword_lower in entry['title'].lower():
            results.append(entry)
    
    return results
```

**Complexity:** O(n) - must check all entries

#### 3. Bubble Sort (Sorting)
```python
def bubble_sort_entries(entries, by='title'):
    n = len(entries)
    
    for i in range(n):
        for j in range(0, n - i - 1):
            if entries[j][by] > entries[j+1][by]:
                entries[j], entries[j+1] = entries[j+1], entries[j]
    
    return entries
```

**Complexity:** O(n²) - nested loops

#### 4. Recursive ID Generator (Recursion)
```python
def generate_entry_id(existing_ids, current=1):
    new_id = f"VAULT{current:03d}"
    
    if new_id not in existing_ids:
        return new_id
    
    return generate_entry_id(existing_ids, current + 1)
```

**Complexity:** O(n) - worst case

### Data Structures Used

| Type | Usage | Example |
|------|-------|---------|
| **List** | Store collections of entries/logs | `entries = [...]` |
| **Dictionary** | Represent vault entries | `entry = {'id': 'VAULT001', ...}` |
| **Tuple** | Immutable config data | `MENU_OPTIONS = (...)` |
| **String** | Heavy manipulation in crypto | Caesar cipher operations |

---

## 🔒 Security

### Security Features

✅ **Password Hashing (SHA256)**
- Passwords never stored in plain text
- One-way hash function (irreversible)
- Same input always produces same hash

✅ **2-Layer Encryption**
- Caesar Cipher: Character shifting based on master password
- Base64: Additional obfuscation layer
- Master password never stored

✅ **Input Sanitization**
- Remove dangerous characters
- Prevent delimiter conflicts
- Validate all user inputs

✅ **Audit Trail**
- All activities logged with timestamp
- Security monitoring capability
- Track unauthorized access attempts

### Security Considerations

⚠️ **Educational Purpose**
- Caesar Cipher + Base64 is NOT production-grade encryption
- Suitable for local password manager with low threat model
- For production, consider AES-256 or other industry-standard algorithms

⚠️ **Master Password**
- Master password is the key to all encrypted data
- If lost, data cannot be recovered
- Choose a strong, memorable master password

⚠️ **Local Storage**
- Data stored in plain text files (encrypted passwords only)
- Secure your computer with disk encryption (BitLocker, FileVault)
- Regular backups recommended

### Potential Improvements

For production use, consider:
1. **Stronger Encryption**: AES-256-GCM
2. **Key Derivation**: PBKDF2 or Argon2
3. **Database**: SQLite with SQLCipher
4. **2FA**: Two-factor authentication
5. **Password Recovery**: Security questions or backup keys

---

## 🛠️ Development

### System Requirements

- **OS**: Windows, Linux, macOS
- **Python**: 3.7+
- **RAM**: Minimal 256 MB
- **Storage**: Minimal 1 MB
- **Internet**: Not required (fully offline)

### Dependencies

**Built-in Modules Only** (No pip install needed):
```python
import hashlib      # SHA256 password hashing
import base64       # Base64 encoding
import datetime     # Timestamp generation
import os           # File operations
import sys          # System operations
```

### Testing

Run individual modules for unit testing:
```bash
# Test utils
python utils.py

# Test crypto
python crypto.py

# Test auth
python auth.py

# Test audit
python audit.py

# Test vault (requires auth)
python vault.py
```

### Code Style

- **Docstrings**: Every function documented
- **Comments**: Explain complex logic
- **PEP 8**: Follow Python style guide
- **Modular**: Separation of concerns

---

## 🤝 Contributing

Contributions are welcome! Here's how:

### How to Contribute

1. **Fork** the repository
2. **Create** a new branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Contribution Ideas

- 🔐 Implement AES-256 encryption
- 📱 Add password generator with customization
- 🌐 Create web interface (Flask/Django)
- 📊 Add data visualization for statistics
- 🔔 Implement password expiry reminders
- 🌍 Add multi-language support
- 🎨 Improve CLI UI with colors (colorama)
- 📦 Add export/import vault backup
- 🔍 Implement breach detection (HIBP API)
- 📱 Create browser extension for auto-fill

### Bug Reports

Found a bug? Please open an issue with:
- Description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots (if applicable)

---

## 👨‍💻 Author

**Project**: Final Project - Dasar Pemrograman  
**Institution**: Institut Pertanian Bogor
**Date**: October 2025

---

## 🙏 Acknowledgments

- Thanks to Bu Faldiena for guidance
- Inspired by modern password managers (LastPass, 1Password, Bitwarden)
- Caesar Cipher: Classical cryptography algorithm
- Python community for excellent documentation

---

## 📚 References

### Cryptography
- [Caesar Cipher - Wikipedia](https://en.wikipedia.org/wiki/Caesar_cipher)
- [Base64 Encoding - RFC 4648](https://tools.ietf.org/html/rfc4648)
- [SHA-256 Hashing - FIPS 180-4](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf)

### Algorithms
- [Linear Search - GeeksforGeeks](https://www.geeksforgeeks.org/linear-search/)
- [Bubble Sort - GeeksforGeeks](https://www.geeksforgeeks.org/bubble-sort/)

### Python
- [Python Documentation](https://docs.python.org/3/)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)

---

## 🎯 Project Goals Achieved

✅ **Academic Requirements**
- CRUD operations: Complete ✓
- File storage: Implemented ✓
- Tipe data koleksi: List, Dict, Tuple ✓
- Fungsi: Regular, recursive, with params/return ✓
- Searching: Linear search (manual) ✓
- Sorting: Bubble sort (manual) + built-in ✓
- String manipulation: Heavy (Caesar cipher) ✓
- CLI interface: Full implementation ✓

✅ **Additional Features**
- 2-layer encryption
- User authentication
- Audit logging
- Statistics generation
- Input validation
- Error handling

---

## 📞 Support

Need help? Have questions?

- 📖 Read the [Usage Guide](#-usage)
- 🐛 Report bugs via [GitHub Issues](https://github.com/yourusername/CipherVault-Plus/issues)
- 💬 Discussion via [GitHub Discussions](https://github.com/yourusername/CipherVault-Plus/discussions)
- 📧 Email: afarik.rakas@gmail.com

---

## ⭐ Show Your Support

If you found this project helpful, please consider:
- ⭐ Starring the repository
- 🍴 Forking for your own modifications
- 📢 Sharing with others
- 🐛 Reporting bugs
- 💡 Suggesting improvements

---

<div align="center">

**Made with ❤️ and ☕ by Afarik Rakas Berdi**

*CipherVault+ - Your Passwords, Your Control, Your Privacy*

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Security](https://img.shields.io/badge/Security-Focused-green?style=for-the-badge)
![Offline](https://img.shields.io/badge/100%25-Offline-blue?style=for-the-badge)

[⬆ Back to Top](#-ciphervault---cli-secured-data-manager)


</div>
