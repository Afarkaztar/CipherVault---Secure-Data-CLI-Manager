"""
auth.py
=======
Authentication module untuk CipherVault+
Mengelola register dan login user

Features:
- Register user baru dengan validation
- Login dengan password hashing (SHA256)
- Session management sederhana
- Check username availability

Topik Praktikum yang diimplementasi:
- Fungsi dengan parameter & return value
- File I/O operations
- Dictionary untuk user data
- String manipulation (hashing)
"""

import hashlib
from datetime import datetime
from utils import (
    get_file_path, 
    sanitize_input,
    validate_username,
    validate_password
)
from audit import log_register, log_login


# ==================== FILE PATH ====================

USERS_FILE = get_file_path('users.txt')


# ==================== PASSWORD HASHING ====================

def hash_password(password):
    """
    Hash password menggunakan SHA256
    
    SHA256 adalah one-way hash function:
    - Input yang sama selalu menghasilkan hash yang sama
    - Tidak bisa di-reverse (hash → password)
    - Secure untuk menyimpan password
    
    Args:
        password (str): Plain password
    
    Returns:
        str: Hashed password (64 karakter hex)
    
    Example:
        >>> hash_password("MyPassword123")
        "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
    """
    # Convert string ke bytes
    password_bytes = password.encode('utf-8')
    
    # Hash dengan SHA256
    hash_object = hashlib.sha256(password_bytes)
    
    # Get hex digest (string representasi)
    hashed = hash_object.hexdigest()
    
    return hashed


def verify_password(plain_password, hashed_password):
    """
    Verify apakah plain password match dengan hash
    
    Args:
        plain_password (str): Password yang diinput user
        hashed_password (str): Hash password yang tersimpan
    
    Returns:
        bool: True jika match
    
    Example:
        >>> stored_hash = hash_password("MyPassword123")
        >>> verify_password("MyPassword123", stored_hash)
        True
        >>> verify_password("WrongPassword", stored_hash)
        False
    """
    # Hash input password
    input_hash = hash_password(plain_password)
    
    # Compare dengan stored hash
    return input_hash == hashed_password


# ==================== USER FILE OPERATIONS ====================

def parse_user_line(line):
    """
    Parse satu baris dari users.txt
    
    Format saat ini: username|password_hash
    Backward compatible: username|password_hash|created_at
    
    Args:
        line (str): Satu baris dari file
    
    Returns:
        dict: Dictionary berisi user data
              None jika format invalid
    
    Example:
        >>> parse_user_line("dani|5e88489...|2025-10-28")
        {'username': 'dani', 'password_hash': '5e88489...', 'created_at': '2025-10-28'}
    """
    try:
        parts = line.strip().split('|')
        
        if len(parts) == 2:
            return {
                'username': parts[0],
                'password_hash': parts[1],
                'created_at': None
            }
        elif len(parts) == 3:
            return {
                'username': parts[0],
                'password_hash': parts[1],
                'created_at': parts[2]
            }
        else:
            return None
    
    except Exception as e:
        print(f"Error parsing user line: {e}")
        return None


def read_all_users():
    """
    Baca semua user dari users.txt
    
    Returns:
        list: List of dictionaries berisi user data
    
    Example:
        >>> users = read_all_users()
        >>> len(users)
        3
    """
    users = []
    
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                user = parse_user_line(line)
                if user:
                    users.append(user)
    
    except FileNotFoundError:
        # File belum ada, return empty list
        pass
    
    except Exception as e:
        print(f"❌ Error reading users: {e}")
    
    return users


def username_exists(username):
    """
    Check apakah username sudah terdaftar
    
    Args:
        username (str): Username yang dicek
    
    Returns:
        bool: True jika username sudah ada
    
    Example:
        >>> username_exists("dani")
        True
        >>> username_exists("newuser")
        False
    """
    users = read_all_users()
    
    # Check apakah username ada (case-insensitive)
    for user in users:
        if user['username'].lower() == username.lower():
            return True
    
    return False


def get_user_by_username(username):
    """
    Get user data berdasarkan username
    
    Args:
        username (str): Username yang dicari
    
    Returns:
        dict: User data atau None jika tidak ditemukan
    """
    users = read_all_users()
    
    for user in users:
        if user['username'].lower() == username.lower():
            return user
    
    return None


def save_user(username, password_hash):
    """
    Simpan user baru ke users.txt
    
    Format baru: username|password_hash
    
    Args:
        username (str): Username
        password_hash (str): Hashed password
    
    Returns:
        bool: True jika berhasil save
    """
    try:
        # Format: username|password_hash (tanpa created_at)
        user_line = f"{username}|{password_hash}\n"
        
        # Append ke file
        with open(USERS_FILE, 'a', encoding='utf-8') as f:
            f.write(user_line)
        
        return True
    
    except Exception as e:
        print(f"❌ Error saving user: {e}")
        return False


# ==================== REGISTER ====================

def register():
    """
    Register user baru
    
    Flow:
    1. Input username
    2. Validasi username (format & availability)
    3. Input password
    4. Validasi password strength
    5. Confirm password
    6. Hash password
    7. Save ke file
    8. Log aktivitas
    
    Returns:
        bool: True jika berhasil register
    """
    print("\n" + "="*50)
    print("  REGISTER NEW USER")
    print("="*50)
    
    # Input username
    username = input("\n> Username: ").strip()
    username = sanitize_input(username)
    
    # Validasi username format
    valid, error_msg = validate_username(username)
    if not valid:
        print(f"❌ {error_msg}")
        return False
    
    # Check availability
    if username_exists(username):
        print(f"❌ Username '{username}' sudah terdaftar!")
        print("   Silakan gunakan username lain.")
        return False
    
    # Input password
    password = input("> Master Password: ").strip()
    
    # Validasi password strength
    valid, error_msg = validate_password(password)
    if not valid:
        print(f"❌ {error_msg}")
        print("\nPassword Requirements:")
        print("  • Minimal 8 karakter")
        print("  • Harus ada huruf BESAR")
        print("  • Harus ada huruf kecil")
        print("  • Harus ada angka")
        return False
    
    # Confirm password
    confirm = input("> Confirm Password: ").strip()
    
    if password != confirm:
        print("❌ Password tidak cocok!")
        return False
    
    # Hash password
    password_hash = hash_password(password)
    
    # Save to file
    if save_user(username, password_hash):
        print(f"\n✅ User '{username}' berhasil didaftarkan!")
        print(f"   Password Anda telah di-hash untuk keamanan.")
        
        # Log aktivitas register
        log_register(username)
        
        return True
    else:
        print("❌ Gagal menyimpan user!")
        return False


# ==================== LOGIN ====================

def login():
    """
    Login user
    
    Flow:
    1. Input username
    2. Check apakah user exist
    3. Input password
    4. Hash password input
    5. Compare dengan stored hash
    6. Return username jika berhasil
    7. Log aktivitas login
    
    Returns:
        str: Username jika berhasil login, None jika gagal
    """
    print("\n" + "="*50)
    print("  LOGIN")
    print("="*50)
    
    # Input username
    username = input("\n> Username: ").strip()
    username = sanitize_input(username)
    
    # Get user data
    user = get_user_by_username(username)
    
    if not user:
        print(f"❌ Username '{username}' tidak ditemukan!")
        print("   Silakan register terlebih dahulu.")
        return None
    
    # Input password
    password = input("> Master Password: ").strip()
    
    # Verify password
    if verify_password(password, user['password_hash']):
        print(f"\n✅ Login berhasil! Selamat datang, {username}!")
        
        # Log aktivitas login
        log_login(username)
        
        # Return username sebagai session token (simple session)
        return username
    else:
        print("❌ Password salah!")
        return None


# ==================== SESSION MANAGEMENT ====================

class Session:
    """
    Simple session management
    
    Menyimpan username user yang sedang login
    """
    def __init__(self):
        self.current_user = None
    
    def login(self, username):
        """Set current user"""
        self.current_user = username
    
    def logout(self):
        """Clear current user"""
        self.current_user = None
    
    def is_logged_in(self):
        """Check apakah ada user yang login"""
        return self.current_user is not None
    
    def get_current_user(self):
        """Get username user yang sedang login"""
        return self.current_user


# Global session object
current_session = Session()


# ==================== TESTING ====================

if __name__ == "__main__":
    print("Testing auth.py...")
    print("="*60)
    
    # Test password hashing
    print("\n1. Testing Password Hashing:")
    passwords = ["Password123", "AnotherPass456", "TestPass789"]
    
    for pwd in passwords:
        hashed = hash_password(pwd)
        print(f"   Password: {pwd}")
        print(f"   Hashed  : {hashed[:32]}... (truncated)")
        
        # Verify
        is_correct = verify_password(pwd, hashed)
        is_wrong = verify_password("WrongPass", hashed)
        print(f"   Verify correct: {'✓' if is_correct else '✗'}")
        print(f"   Verify wrong  : {'✓' if not is_wrong else '✗'}")
        print()
    
    # Test username validation
    print("\n2. Testing Username Validation:")
    test_usernames = ["ab", "validuser", "user_123", "user@name"]
    for username in test_usernames:
        valid, msg = validate_username(username)
        status = '✓' if valid else '✗'
        print(f"   {status} '{username}': {msg if msg else 'Valid'}")
    
    # Test password validation
    print("\n3. Testing Password Validation:")
    test_passwords = ["weak", "NoDigits", "no_upper123", "ValidPass123"]
    for password in test_passwords:
        valid, msg = validate_password(password)
        status = '✓' if valid else '✗'
        print(f"   {status} '{password}': {msg}")
    
    # Test read users
    print("\n4. Testing Read Users:")
    users = read_all_users()
    print(f"   Total users in database: {len(users)}")
    for user in users:
        print(f"   - {user['username']} (created: {user['created_at']})")
    
    # Test username exists
    print("\n5. Testing Username Exists:")
    test_check = ["admin", "user1", "nonexistent"]
    for username in test_check:
        exists = username_exists(username)
        print(f"   '{username}': {'EXISTS' if exists else 'NOT FOUND'}")
    
    # Test session
    print("\n6. Testing Session:")
    session = Session()
    print(f"   Is logged in: {session.is_logged_in()}")
    
    session.login("testuser")
    print(f"   After login: {session.is_logged_in()}")
    print(f"   Current user: {session.get_current_user()}")
    
    session.logout()
    print(f"   After logout: {session.is_logged_in()}")
    
    print("\n" + "="*60)
    print("✅ Auth testing complete!")
    print("\nTo test register & login interactively, run:")
    print("  1. Call register() function")
    print("  2. Call login() function")