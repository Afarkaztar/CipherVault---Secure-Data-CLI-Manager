"""
vault.py
========
CRUD operations module untuk CipherVault+
Mengelola vault entries (password manager)

Features:
- CREATE: Tambah entry baru dengan auto-encryption
- READ: Lihat semua entries
- UPDATE: Edit entry existing
- DELETE: Hapus entry dengan konfirmasi
- SEARCH: Cari entry berdasarkan keyword (Linear Search)
- SORT: Sort entries by title/date (Bubble Sort + Built-in)

Topik Praktikum yang diimplementasi:
- Tipe Data Koleksi (List, Dictionary)
- Fungsi dengan parameter & return value
- Searching (Linear Search manual)
- Sorting (Bubble Sort manual + built-in)
- String manipulation
- File I/O operations
"""

from datetime import datetime
from utils import (
    get_file_path,
    format_timestamp,
    sanitize_input,
    generate_entry_id,
    mask_password,
    format_entry_display,
    print_header,
    print_separator,
    confirm_action
)
from crypto import encrypt_password, decrypt_password
from audit import (
    log_create_entry,
    log_read_entry,
    log_update_entry,
    log_delete_entry,
    log_search
)


# ==================== FILE PATH ====================

VAULT_FILE = get_file_path('vault.txt')


# ==================== PARSE & FORMAT ====================

def parse_vault_line(line):
    """
    Parse satu baris dari vault.txt
    
    Format: id|username|title|account|encrypted_password|notes|timestamp
    
    Args:
        line (str): Satu baris dari file
    
    Returns:
        dict: Dictionary berisi entry data
              None jika format invalid
    
    Example:
        >>> parse_vault_line("VAULT001|dani|Gmail|dani@gmail.com|Q1pS...|Notes|2025-10-28 10:30:00")
        {'id': 'VAULT001', 'username': 'dani', 'title': 'Gmail', ...}
    """
    try:
        parts = line.strip().split('|')
        
        if len(parts) == 7:
            return {
                'id': parts[0],
                'username': parts[1],
                'title': parts[2],
                'account': parts[3],
                'password': parts[4],  # Still encrypted
                'notes': parts[5],
                'created_at': parts[6]
            }
        else:
            return None
    
    except Exception as e:
        print(f"Error parsing vault line: {e}")
        return None


def format_vault_line(entry):
    """
    Format entry dictionary ke string untuk save ke file
    
    Args:
        entry (dict): Entry dictionary
    
    Returns:
        str: Formatted line
    
    Example:
        >>> entry = {'id': 'VAULT001', 'username': 'dani', ...}
        >>> format_vault_line(entry)
        "VAULT001|dani|Gmail|dani@gmail.com|Q1pS...|Notes|2025-10-28 10:30:00"
    """
    return f"{entry['id']}|{entry['username']}|{entry['title']}|{entry['account']}|{entry['password']}|{entry['notes']}|{entry['created_at']}\n"


# ==================== READ OPERATIONS ====================

def read_all_entries():
    """
    Baca semua entries dari vault.txt
    
    Returns:
        list: List of dictionaries berisi vault entries
    
    Example:
        >>> entries = read_all_entries()
        >>> len(entries)
        5
    """
    entries = []
    
    try:
        with open(VAULT_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                entry = parse_vault_line(line)
                if entry:
                    entries.append(entry)
    
    except FileNotFoundError:
        # File belum ada, return empty list
        pass
    
    except Exception as e:
        print(f"❌ Error reading vault: {e}")
    
    return entries


def get_user_entries(username):
    """
    Get semua entries milik user tertentu
    
    Args:
        username (str): Username owner
    
    Returns:
        list: List of entries milik user
    """
    all_entries = read_all_entries()
    
    # Filter by username (case-insensitive)
    user_entries = [entry for entry in all_entries if entry['username'].lower() == username.lower()]
    
    return user_entries


def get_entry_by_id(entry_id):
    """
    Get entry berdasarkan ID
    
    Args:
        entry_id (str): ID entry (VAULT001, VAULT002, etc)
    
    Returns:
        dict: Entry data atau None jika tidak ditemukan
    """
    all_entries = read_all_entries()
    
    for entry in all_entries:
        if entry['id'] == entry_id:
            return entry
    
    return None


def get_existing_ids():
    """
    Get semua ID yang sudah ada (untuk generate ID baru)
    
    Returns:
        list: List of existing IDs
    """
    entries = read_all_entries()
    return [entry['id'] for entry in entries]


# ==================== SAVE OPERATIONS ====================

def save_all_entries(entries):
    """
    Save/overwrite semua entries ke vault.txt
    
    Args:
        entries (list): List of entry dictionaries
    
    Returns:
        bool: True jika berhasil save
    """
    try:
        with open(VAULT_FILE, 'w', encoding='utf-8') as f:
            for entry in entries:
                line = format_vault_line(entry)
                f.write(line)
        
        return True
    
    except Exception as e:
        print(f"❌ Error saving vault: {e}")
        return False


# ==================== CREATE ====================

def create_entry(username, master_password):
    """
    Create entry baru
    
    Flow:
    1. Input title, account, password, notes
    2. Encrypt password dengan master_password
    3. Generate unique ID
    4. Save ke file
    5. Log aktivitas
    
    Args:
        username (str): Username owner
        master_password (str): Master password untuk enkripsi
    
    Returns:
        bool: True jika berhasil create
    """
    print_header("CREATE NEW ENTRY")
    
    # Input data entry
    print("\nMasukkan data entry:")
    title = input("  Title (e.g. Gmail Account): ").strip()
    title = sanitize_input(title)
    
    if not title:
        print("❌ Title tidak boleh kosong!")
        return False
    
    account = input("  Account/Username: ").strip()
    account = sanitize_input(account)
    
    password = input("  Password: ").strip()
    
    if not password:
        print("❌ Password tidak boleh kosong!")
        return False
    
    notes = input("  Notes (optional): ").strip()
    notes = sanitize_input(notes)
    
    # Encrypt password
    print("\n🔐 Encrypting password...")
    encrypted_password = encrypt_password(password, master_password)
    
    # Generate unique ID
    existing_ids = get_existing_ids()
    entry_id = generate_entry_id(existing_ids)
    
    # Create entry dictionary
    new_entry = {
        'id': entry_id,
        'username': username,
        'title': title,
        'account': account,
        'password': encrypted_password,  # Encrypted!
        'notes': notes,
        'created_at': format_timestamp()
    }
    
    # Read existing entries
    all_entries = read_all_entries()
    
    # Append new entry
    all_entries.append(new_entry)
    
    # Save to file
    if save_all_entries(all_entries):
        print(f"\n✅ Entry '{title}' berhasil dibuat!")
        print(f"   ID: {entry_id}")
        print(f"   Password telah dienkripsi dengan aman.")
        
        # Log aktivitas
        log_create_entry(username, title)
        
        return True
    else:
        print("❌ Gagal menyimpan entry!")
        return False


# ==================== READ ====================

def view_all_entries(username, master_password):
    """
    Tampilkan semua entries milik user
    
    Args:
        username (str): Username owner
        master_password (str): Master password untuk dekripsi
    """
    print_header("YOUR VAULT ENTRIES")
    
    # Get user entries
    entries = get_user_entries(username)
    
    if not entries:
        print("\n  (No entries yet. Create your first entry!)")
        return
    
    print(f"\n  Total: {len(entries)} entries\n")
    
    # Display entries
    for i, entry in enumerate(entries, 1):
        print(f"{i}. [{entry['id']}] {entry['title']}")
        print(f"   Account : {entry['account']}")
        print(f"   Password: {mask_password(entry['password'])}")
        print(f"   Notes   : {entry['notes']}")
        print(f"   Created : {entry['created_at']}")
        print()
    
    # Option untuk view detail
    print_separator()
    choice = input("\n> View detail entry? (Enter ID atau 'n' untuk skip): ").strip()
    
    if choice.lower() != 'n' and choice:
        view_entry_detail(choice, username, master_password)


def view_entry_detail(entry_id, username, master_password):
    """
    View detail entry dengan option show/hide password
    
    Args:
        entry_id (str): ID entry
        username (str): Username owner
        master_password (str): Master password untuk dekripsi
    """
    # Get entry
    entry = get_entry_by_id(entry_id)
    
    if not entry:
        print(f"❌ Entry dengan ID '{entry_id}' tidak ditemukan!")
        return
    
    # Check ownership
    if entry['username'].lower() != username.lower():
        print("❌ Anda tidak punya akses ke entry ini!")
        return
    
    # Display entry
    print("\n" + "="*50)
    print("  ENTRY DETAIL")
    print("="*50)
    
    print(f"\nID       : {entry['id']}")
    print(f"Title    : {entry['title']}")
    print(f"Account  : {entry['account']}")
    print(f"Password : {mask_password(entry['password'])} (encrypted)")
    print(f"Notes    : {entry['notes']}")
    print(f"Created  : {entry['created_at']}")
    
    # Option show password
    show = input("\n> Show password? (y/n): ").lower()
    
    if show == 'y':
        print("\n🔓 Decrypting password...")
        decrypted = decrypt_password(entry['password'], master_password)
        
        if decrypted:
            print(f"   Password: {decrypted}")
            
            # Log aktivitas read
            log_read_entry(username, entry['title'])
        else:
            print("❌ Gagal decrypt password!")
            print("   Pastikan master password Anda benar.")


# ==================== UPDATE ====================

def update_entry(username, master_password):
    """
    Update entry existing
    
    Flow:
    1. Tampilkan list entries
    2. Pilih entry by ID
    3. Input data baru (bisa skip dengan Enter)
    4. Re-encrypt password jika diubah
    5. Save changes
    6. Log aktivitas
    
    Args:
        username (str): Username owner
        master_password (str): Master password untuk enkripsi
    
    Returns:
        bool: True jika berhasil update
    """
    print_header("UPDATE ENTRY")
    
    # Get user entries
    entries = get_user_entries(username)
    
    if not entries:
        print("\n  (No entries to update)")
        return False
    
    # Display entries
    print(f"\n  Your entries:\n")
    for entry in entries:
        print(f"  [{entry['id']}] {entry['title']} - {entry['account']}")
    
    # Pilih entry
    entry_id = input("\n> Enter ID entry yang akan diupdate: ").strip()
    
    entry = get_entry_by_id(entry_id)
    
    if not entry:
        print(f"❌ Entry dengan ID '{entry_id}' tidak ditemukan!")
        return False
    
    # Check ownership
    if entry['username'].lower() != username.lower():
        print("❌ Anda tidak punya akses ke entry ini!")
        return False
    
    # Display current data
    print("\n  Current data:")
    print(f"  Title   : {entry['title']}")
    print(f"  Account : {entry['account']}")
    print(f"  Password: {mask_password(entry['password'])}")
    print(f"  Notes   : {entry['notes']}")
    
    print("\n  Enter new data (press Enter to keep current):")
    
    # Input new data
    new_title = input(f"  New Title [{entry['title']}]: ").strip()
    if new_title:
        entry['title'] = sanitize_input(new_title)
    
    new_account = input(f"  New Account [{entry['account']}]: ").strip()
    if new_account:
        entry['account'] = sanitize_input(new_account)
    
    new_password = input("  New Password (leave empty to keep): ").strip()
    if new_password:
        # Encrypt new password
        print("  🔐 Encrypting new password...")
        entry['password'] = encrypt_password(new_password, master_password)
    
    new_notes = input(f"  New Notes [{entry['notes']}]: ").strip()
    if new_notes:
        entry['notes'] = sanitize_input(new_notes)
    
    # Confirm update
    if not confirm_action("Save changes?"):
        print("❌ Update dibatalkan.")
        return False
    
    # Update in list
    all_entries = read_all_entries()
    
    for i, e in enumerate(all_entries):
        if e['id'] == entry_id:
            all_entries[i] = entry
            break
    
    # Save to file
    if save_all_entries(all_entries):
        print(f"\n✅ Entry '{entry['title']}' berhasil diupdate!")
        
        # Log aktivitas
        log_update_entry(username, entry['title'])
        
        return True
    else:
        print("❌ Gagal menyimpan perubahan!")
        return False


# ==================== DELETE ====================

def delete_entry(username):
    """
    Delete entry
    
    Flow:
    1. Tampilkan list entries
    2. Pilih entry by ID
    3. Konfirmasi delete
    4. Remove dari list
    5. Save changes
    6. Log aktivitas
    
    Args:
        username (str): Username owner
    
    Returns:
        bool: True jika berhasil delete
    """
    print_header("DELETE ENTRY")
    
    # Get user entries
    entries = get_user_entries(username)
    
    if not entries:
        print("\n  (No entries to delete)")
        return False
    
    # Display entries
    print(f"\n  Your entries:\n")
    for entry in entries:
        print(f"  [{entry['id']}] {entry['title']} - {entry['account']}")
    
    # Pilih entry
    entry_id = input("\n> Enter ID entry yang akan dihapus: ").strip()
    
    entry = get_entry_by_id(entry_id)
    
    if not entry:
        print(f"❌ Entry dengan ID '{entry_id}' tidak ditemukan!")
        return False
    
    # Check ownership
    if entry['username'].lower() != username.lower():
        print("❌ Anda tidak punya akses ke entry ini!")
        return False
    
    # Display entry to be deleted
    print("\n  Entry yang akan dihapus:")
    print(f"  Title   : {entry['title']}")
    print(f"  Account : {entry['account']}")
    
    # Confirm delete
    if not confirm_action("⚠️  HAPUS entry ini? (Tidak bisa di-undo!)"):
        print("❌ Delete dibatalkan.")
        return False
    
    # Remove from list
    all_entries = read_all_entries()
    all_entries = [e for e in all_entries if e['id'] != entry_id]
    
    # Save to file
    if save_all_entries(all_entries):
        print(f"\n✅ Entry '{entry['title']}' berhasil dihapus!")
        
        # Log aktivitas
        log_delete_entry(username, entry['title'])
        
        return True
    else:
        print("❌ Gagal menghapus entry!")
        return False


# ==================== SEARCH (LINEAR SEARCH) ====================

def search_entries(username, keyword):
    """
    Search entries berdasarkan keyword (Linear Search manual)
    
    Mencari di field: title, account
    
    Args:
        username (str): Username owner
        keyword (str): Keyword pencarian
    
    Returns:
        list: List of matching entries
    
    Example:
        >>> search_entries("dani", "gmail")
        [{'id': 'VAULT001', 'title': 'Gmail Account', ...}]
    """
    # Get user entries
    entries = get_user_entries(username)
    
    # List untuk hasil search
    results = []
    
    # Linear search manual (implementasi topik praktikum)
    keyword_lower = keyword.lower()
    
    for entry in entries:
        # Check di field title dan account
        if (keyword_lower in entry['title'].lower() or 
            keyword_lower in entry['account'].lower()):
            results.append(entry)
    
    return results


def search_menu(username, master_password):
    """
    Menu search entries
    
    Args:
        username (str): Username owner
        master_password (str): Master password untuk dekripsi
    """
    print_header("SEARCH ENTRIES")
    
    keyword = input("\n> Enter keyword (title/account): ").strip()
    
    if not keyword:
        print("❌ Keyword tidak boleh kosong!")
        return
    
    # Search
    print(f"\n🔍 Searching for '{keyword}'...")
    results = search_entries(username, keyword)
    
    # Log aktivitas
    log_search(username, keyword)
    
    # Display results
    if not results:
        print(f"\n  (No entries found matching '{keyword}')")
        return
    
    print(f"\n  Found {len(results)} entries:\n")
    
    for i, entry in enumerate(results, 1):
        print(f"{i}. [{entry['id']}] {entry['title']}")
        print(f"   Account : {entry['account']}")
        print(f"   Password: {mask_password(entry['password'])}")
        print(f"   Notes   : {entry['notes']}")
        print()
    
    # Option view detail
    print_separator()
    choice = input("\n> View detail? (Enter ID atau 'n'): ").strip()
    
    if choice.lower() != 'n' and choice:
        view_entry_detail(choice, username, master_password)


# ==================== SORT (BUBBLE SORT + BUILT-IN) ====================

def bubble_sort_entries(entries, by='title', reverse=False):
    """
    Sort entries menggunakan Bubble Sort (manual implementation)
    
    Implementasi topik praktikum: Sorting
    
    Args:
        entries (list): List of entries
        by (str): Field untuk sort ('title' atau 'created_at')
        reverse (bool): True untuk descending order
    
    Returns:
        list: Sorted entries
    
    Example:
        >>> entries = [{'title': 'Gmail'}, {'title': 'Facebook'}]
        >>> sorted_entries = bubble_sort_entries(entries, by='title')
        [{'title': 'Facebook'}, {'title': 'Gmail'}]
    """
    # Copy list agar tidak modify original
    arr = entries.copy()
    n = len(arr)
    
    # Bubble sort algorithm
    for i in range(n):
        # Flag untuk optimasi (jika sudah sorted, stop early)
        swapped = False
        
        for j in range(0, n - i - 1):
            # Get values to compare
            val1 = arr[j][by].lower() if isinstance(arr[j][by], str) else arr[j][by]
            val2 = arr[j + 1][by].lower() if isinstance(arr[j + 1][by], str) else arr[j + 1][by]
            
            # Compare (ascending by default)
            should_swap = val1 > val2 if not reverse else val1 < val2
            
            if should_swap:
                # Swap
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        
        # Jika tidak ada swap, array sudah sorted
        if not swapped:
            break
    
    return arr


def sort_entries_builtin(entries, by='title', reverse=False):
    """
    Sort entries menggunakan built-in sorted() (untuk production)
    
    Args:
        entries (list): List of entries
        by (str): Field untuk sort
        reverse (bool): True untuk descending
    
    Returns:
        list: Sorted entries
    """
    return sorted(entries, key=lambda x: x[by].lower() if isinstance(x[by], str) else x[by], reverse=reverse)


def sort_menu(username):
    """
    Menu sort entries
    
    Args:
        username (str): Username owner
    """
    print_header("SORT ENTRIES")
    
    # Get user entries
    entries = get_user_entries(username)
    
    if not entries:
        print("\n  (No entries to sort)")
        return
    
    # Sort options
    print("\n  Sort by:")
    print("  1. Title (A-Z)")
    print("  2. Title (Z-A)")
    print("  3. Date (Newest First)")
    print("  4. Date (Oldest First)")
    
    choice = input("\n> Choose sort option: ").strip()
    
    # Determine sort parameters
    if choice == '1':
        sorted_entries = bubble_sort_entries(entries, by='title', reverse=False)
        sort_desc = "Title (A-Z)"
    elif choice == '2':
        sorted_entries = bubble_sort_entries(entries, by='title', reverse=True)
        sort_desc = "Title (Z-A)"
    elif choice == '3':
        sorted_entries = sort_entries_builtin(entries, by='created_at', reverse=True)
        sort_desc = "Date (Newest First)"
    elif choice == '4':
        sorted_entries = sort_entries_builtin(entries, by='created_at', reverse=False)
        sort_desc = "Date (Oldest First)"
    else:
        print("❌ Invalid choice!")
        return
    
    # Display sorted entries
    print(f"\n  Sorted by: {sort_desc}\n")
    
    for i, entry in enumerate(sorted_entries, 1):
        print(f"{i}. [{entry['id']}] {entry['title']}")
        print(f"   Account : {entry['account']}")
        print(f"   Created : {entry['created_at']}")
        print()


# ==================== TESTING ====================

if __name__ == "__main__":
    print("Testing vault.py...")
    print("="*60)
    print("\n⚠️  This module requires auth.py for full testing")
    print("Run from main.py for complete functionality test")
    
    # Test parse line
    print("\n1. Testing Parse Vault Line:")
    test_line = "VAULT001|dani|Gmail|dani@gmail.com|Q1pSVllQMTIz|Email utama|2025-10-28 10:30:00"
    entry = parse_vault_line(test_line)
    if entry:
        print(f"   ✓ Parsed: {entry['title']} - {entry['account']}")
    
    # Test format line
    print("\n2. Testing Format Vault Line:")
    formatted = format_vault_line(entry)
    print(f"   ✓ Formatted: {formatted.strip()}")
    
    # Test bubble sort
    print("\n3. Testing Bubble Sort:")
    test_entries = [
        {'id': 'V001', 'title': 'Gmail', 'created_at': '2025-10-28'},
        {'id': 'V002', 'title': 'Facebook', 'created_at': '2025-10-27'},
        {'id': 'V003', 'title': 'Amazon', 'created_at': '2025-10-29'}
    ]
    
    sorted_entries = bubble_sort_entries(test_entries, by='title')
    print("   Sorted by title:")
    for e in sorted_entries:
        print(f"   - {e['title']}")
    
    # Test search
    print("\n4. Testing Linear Search:")
    keyword = "mail"
    results = []
    for entry in test_entries:
        if keyword.lower() in entry['title'].lower():
            results.append(entry)
    print(f"   Search '{keyword}': Found {len(results)} results")
    
    print("\n" + "="*60)
    print("✅ Vault testing complete!")