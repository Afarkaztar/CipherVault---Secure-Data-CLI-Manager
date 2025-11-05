"""
utils.py
========
Helper utilities untuk CipherVault+
Berisi fungsi-fungsi pendukung seperti:
- ID generator (rekursif)
- Input validation
- Display formatting
- File path management
"""

import os
from datetime import datetime


# ==================== FILE PATH MANAGEMENT ====================

def get_data_dir():
    """
    Get path ke folder data/
    Akan create folder jika belum ada
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')
    
    # Create folder data jika belum ada
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    return data_dir


def get_file_path(filename):
    """
    Get full path untuk file di folder data/
    
    Args:
        filename (str): Nama file (users.txt, vault.txt, audit_log.txt)
    
    Returns:
        str: Full path ke file
    """
    return os.path.join(get_data_dir(), filename)


# ==================== ID GENERATOR (RECURSIVE) ====================

def generate_entry_id(existing_ids, current=1):
    """
    Generate unique ID untuk vault entry secara rekursif
    Format: VAULT001, VAULT002, dst
    
    Args:
        existing_ids (list): List ID yang sudah ada
        current (int): Nomor ID saat ini (default 1)
    
    Returns:
        str: Unique ID baru
    
    Example:
        >>> generate_entry_id(['VAULT001', 'VAULT002'])
        'VAULT003'
    """
    new_id = f"VAULT{current:03d}"  # Format: VAULT001, VAULT002, dst
    
    # Base case: ID belum ada, return
    if new_id not in existing_ids:
        return new_id
    
    # Recursive case: ID sudah ada, coba nomor berikutnya
    return generate_entry_id(existing_ids, current + 1)


# ==================== INPUT VALIDATION & SANITIZATION ====================

def sanitize_input(text):
    """
    Bersihkan input dari karakter yang bisa conflict dengan delimiter
    
    Args:
        text (str): Input text dari user
    
    Returns:
        str: Cleaned text
    """
    # Hilangkan pipe character (dipakai sebagai delimiter di file)
    text = text.replace('|', '')
    
    # Hilangkan newline characters
    text = text.replace('\n', ' ').replace('\r', '')
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text


def validate_username(username):
    """
    Validasi username
    Rules:
    - Minimal 3 karakter
    - Hanya boleh huruf, angka, underscore
    
    Args:
        username (str): Username untuk divalidasi
    
    Returns:
        tuple: (bool, str) -> (is_valid, error_message)
    """
    if len(username) < 3:
        return False, "Username minimal 3 karakter"
    
    if not username.replace('_', '').isalnum():
        return False, "Username hanya boleh huruf, angka, dan underscore"
    
    return True, ""


def validate_password(password):
    """
    Validasi password strength
    Rules:
    - Minimal 8 karakter
    - Harus ada huruf besar
    - Harus ada huruf kecil
    - Harus ada angka
    
    Args:
        password (str): Password untuk divalidasi
    
    Returns:
        tuple: (bool, str) -> (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password minimal 8 karakter"
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    
    if not has_upper:
        return False, "Password harus ada huruf besar"
    
    if not has_lower:
        return False, "Password harus ada huruf kecil"
    
    if not has_digit:
        return False, "Password harus ada angka"
    
    return True, "Password kuat"


# ==================== DISPLAY FORMATTING ====================

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title):
    """
    Print header dengan border
    
    Args:
        title (str): Judul header
    """
    print("\n" + "="*50)
    print(f"  {title.upper()}")
    print("="*50)


def print_separator():
    """Print separator line"""
    print("-" * 50)


def format_timestamp(dt=None):
    """
    Format datetime ke string
    
    Args:
        dt (datetime): Datetime object (default: sekarang)
    
    Returns:
        str: Formatted timestamp (YYYY-MM-DD HH:MM:SS)
    """
    if dt is None:
        dt = datetime.now()
    
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def format_date(dt=None):
    """
    Format datetime ke string date only
    
    Args:
        dt (datetime): Datetime object (default: sekarang)
    
    Returns:
        str: Formatted date (YYYY-MM-DD)
    """
    if dt is None:
        dt = datetime.now()
    
    return dt.strftime("%Y-%m-%d")


def mask_password(password):
    """
    Mask password dengan asterisk
    
    Args:
        password (str): Password asli
    
    Returns:
        str: Masked password (*******)
    """
    return "*" * len(password)


def format_entry_display(entry, show_password=False):
    """
    Format entry untuk ditampilkan di terminal
    
    Args:
        entry (dict): Dictionary entry vault
        show_password (bool): Apakah password ditampilkan
    
    Returns:
        str: Formatted string untuk display
    """
    password_display = entry['password'] if show_password else mask_password(entry['password'])
    
    result = f"""
╔══════════════════════════════════════════════╗
║ ID       : {entry['id']:<35}║
║ Title    : {entry['title']:<35}║
║ Account  : {entry['account']:<35}║
║ Password : {password_display:<35}║
║ Notes    : {entry.get('notes', '')[:35]:<35}║
║ Created  : {entry.get('created_at', ''):<35}║
╚══════════════════════════════════════════════╝
"""
    return result


# ==================== MENU HELPERS ====================

def get_menu_choice(max_option):
    """
    Get dan validate pilihan menu dari user
    
    Args:
        max_option (int): Jumlah pilihan menu maksimal
    
    Returns:
        int: Pilihan user (1-max_option) atau 0 jika invalid
    """
    try:
        choice = int(input("\n> Pilih menu: "))
        
        if 1 <= choice <= max_option:
            return choice
        else:
            print(f"❌ Pilihan harus antara 1-{max_option}")
            return 0
    except ValueError:
        print("❌ Input harus berupa angka")
        return 0


def confirm_action(message="Apakah Anda yakin?"):
    """
    Minta konfirmasi dari user
    
    Args:
        message (str): Pesan konfirmasi
    
    Returns:
        bool: True jika user confirm (y/yes)
    """
    response = input(f"\n{message} (y/n): ").lower()
    return response in ['y', 'yes']


# ==================== TESTING ====================

if __name__ == "__main__":
    # Test fungsi-fungsi utils
    print("Testing utils.py...")
    
    # Test ID generator
    print("\n1. Testing ID Generator (Recursive):")
    existing = ['VAULT001', 'VAULT002', 'VAULT005']
    new_id = generate_entry_id(existing)
    print(f"   Existing IDs: {existing}")
    print(f"   Generated ID: {new_id}")
    
    # Test sanitize input
    print("\n2. Testing Input Sanitization:")
    dirty = "Hello|World\nTest"
    clean = sanitize_input(dirty)
    print(f"   Before: {repr(dirty)}")
    print(f"   After: {repr(clean)}")
    
    # Test validation
    print("\n3. Testing Username Validation:")
    usernames = ["ab", "user123", "test_user", "user@123"]
    for username in usernames:
        valid, msg = validate_username(username)
        print(f"   '{username}': {'✓' if valid else '✗'} {msg}")
    
    print("\n4. Testing Password Validation:")
    passwords = ["weak", "StrongPass", "Strong123"]
    for password in passwords:
        valid, msg = validate_password(password)
        print(f"   '{password}': {'✓' if valid else '✗'} {msg}")
    
    print("\n✅ Utils testing complete!")