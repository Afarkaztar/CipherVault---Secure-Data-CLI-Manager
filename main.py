"""
main.py
=======
Entry point untuk CipherVault+
CLI Secured Data Manager

Main menu dan flow control untuk:
- Authentication (Register/Login)
- Vault Dashboard (CRUD + Search + Sort + Audit)
- Session management
- Exit program

Author: [Your Name]
Date: 2025-10-28
"""

import os
import sys
from utils import (
    clear_screen,
    print_header,
    print_separator,
    get_menu_choice,
    confirm_action
)
from auth import register, login, current_session
from vault import (
    create_entry,
    view_all_entries,
    update_entry,
    delete_entry,
    search_menu,
    sort_menu,
    get_user_entries
)
from audit import (
    display_logs,
    get_user_logs,
    get_recent_logs,
    display_statistics,
    get_user_statistics,
    log_logout
)


# ==================== WELCOME SCREEN ====================

def show_welcome():
    """
    Tampilkan welcome screen
    """
    clear_screen()
    print("\n" + "="*60)
    print("╔══════════════════════════════════════════════════════════╗")
    print("║                                                          ║")
    print("║              🔐  CIPHERVAULT+ v1.0  🔐                  ║")
    print("║                                                          ║")
    print("║              CLI Secured Data Manager                   ║")
    print("║         Password Manager dengan Enkripsi 2-Layer        ║")
    print("║                                                          ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print("="*60)
    print("\n  Features:")
    print("  • Enkripsi 2-Layer (Caesar Cipher + Base64)")
    print("  • CRUD Operations (Create, Read, Update, Delete)")
    print("  • Search & Sort Algorithms")
    print("  • Audit Logging System")
    print("  • Offline & Secure (Data tersimpan lokal)")
    print("\n" + "="*60)


# ==================== MAIN MENU (BEFORE LOGIN) ====================

def main_menu():
    """
    Main menu sebelum login
    
    Returns:
        str: Choice ('register', 'login', 'exit')
    """
    print("\n" + "="*60)
    print("  MAIN MENU")
    print("="*60)
    print("\n  1. Register (Buat akun baru)")
    print("  2. Login (Masuk ke vault)")
    print("  3. Exit (Keluar program)")
    
    choice = get_menu_choice(3)
    
    if choice == 1:
        return 'register'
    elif choice == 2:
        return 'login'
    elif choice == 3:
        return 'exit'
    else:
        return None


# ==================== VAULT DASHBOARD (AFTER LOGIN) ====================

def vault_dashboard(username, master_password):
    """
    Vault dashboard - menu utama setelah login
    
    Args:
        username (str): Username yang sedang login
        master_password (str): Master password (untuk encrypt/decrypt)
    
    Returns:
        str: 'logout' jika user pilih logout
    """
    while True:
        clear_screen()
        print("\n" + "="*60)
        print(f"  VAULT DASHBOARD - Welcome, {username}!")
        print("="*60)
        
        # Show statistics
        user_entries = get_user_entries(username)
        entry_count = len(user_entries)
        print(f"\n  📊 Total entries: {entry_count}")
        
        # Menu options
        print("\n  1. Create New Entry")
        print("  2. View All Entries")
        print("  3. Search Entry")
        print("  4. Update Entry")
        print("  5. Delete Entry")
        print("  6. Sort Entries")
        print("  7. View Audit Log")
        print("  8. Account Statistics")
        print("  9. Logout")
        
        choice = get_menu_choice(9)
        
        if choice == 1:
            # CREATE
            create_entry(username, master_password)
            input("\nPress Enter to continue...")
        
        elif choice == 2:
            # READ
            view_all_entries(username, master_password)
            input("\nPress Enter to continue...")
        
        elif choice == 3:
            # SEARCH
            search_menu(username, master_password)
            input("\nPress Enter to continue...")
        
        elif choice == 4:
            # UPDATE
            update_entry(username, master_password)
            input("\nPress Enter to continue...")
        
        elif choice == 5:
            # DELETE
            delete_entry(username)
            input("\nPress Enter to continue...")
        
        elif choice == 6:
            # SORT
            sort_menu(username)
            input("\nPress Enter to continue...")
        
        elif choice == 7:
            # AUDIT LOG
            show_audit_log_menu(username)
            input("\nPress Enter to continue...")
        
        elif choice == 8:
            # STATISTICS
            show_statistics(username)
            input("\nPress Enter to continue...")
        
        elif choice == 9:
            # LOGOUT
            if confirm_action("Logout dari vault?"):
                log_logout(username)
                current_session.logout()
                print(f"\n✅ Logout berhasil. Sampai jumpa, {username}!")
                return 'logout'
        
        else:
            print("❌ Pilihan tidak valid!")
            input("\nPress Enter to continue...")


# ==================== AUDIT LOG MENU ====================

def show_audit_log_menu(username):
    """
    Menu untuk view audit logs
    
    Args:
        username (str): Username yang sedang login
    """
    print_header("AUDIT LOG")
    
    print("\n  View options:")
    print("  1. My Activities (All)")
    print("  2. Recent Activities (Last 10)")
    print("  3. All System Logs")
    
    choice = get_menu_choice(3)
    
    if choice == 1:
        # User logs
        logs = get_user_logs(username)
        display_logs(logs, f"Activities for {username}")
    
    elif choice == 2:
        # Recent logs
        logs = get_recent_logs(10)
        # Filter by current user
        user_logs = [log for log in logs if log['username'] == username]
        display_logs(user_logs, f"Recent Activities for {username}")
    
    elif choice == 3:
        # All logs (admin view)
        from audit import read_all_logs
        all_logs = read_all_logs()
        display_logs(all_logs, "All System Logs")
    
    else:
        print("❌ Pilihan tidak valid!")


# ==================== STATISTICS ====================

def show_statistics(username):
    """
    Tampilkan statistics untuk user
    
    Args:
        username (str): Username yang sedang login
    """
    print_header("ACCOUNT STATISTICS")
    
    # Get statistics
    stats = get_user_statistics(username)
    
    # Display
    display_statistics(stats)
    
    # Additional vault statistics
    entries = get_user_entries(username)
    
    if entries:
        print("\n" + "="*60)
        print("  VAULT STATISTICS")
        print("="*60)
        
        print(f"\nTotal Entries: {len(entries)}")
        
        # Most recent entry
        latest = max(entries, key=lambda x: x['created_at'])
        print(f"Latest Entry : {latest['title']} ({latest['created_at']})")
        
        # Oldest entry
        oldest = min(entries, key=lambda x: x['created_at'])
        print(f"Oldest Entry : {oldest['title']} ({oldest['created_at']})")


# ==================== MAIN PROGRAM FLOW ====================

def main():
    """
    Main program flow
    
    Flow:
    1. Show welcome screen
    2. Main menu (Register/Login/Exit)
    3. If login success → Vault Dashboard
    4. Loop until user logout or exit
    """
    # Show welcome
    show_welcome()
    input("\nPress Enter to continue...")
    
    # Main loop
    while True:
        clear_screen()
        
        # Check if user already logged in
        if current_session.is_logged_in():
            # Go to vault dashboard
            username = current_session.get_current_user()
            
            # Need to get master password again (for encryption/decryption)
            # NOTE: In production, you might want to store encrypted in session
            print(f"\n  Welcome back, {username}!")
            master_password = input("  Enter your master password: ").strip()
            
            # Verify password by trying to decrypt a test entry
            # For simplicity, we'll trust the user entered correct password
            # (Password was verified during login)
            
            vault_dashboard(username, master_password)
        
        else:
            # Show main menu
            action = main_menu()
            
            if action == 'register':
                # Register
                clear_screen()
                success = register()
                
                if success:
                    print("\n✅ Registrasi berhasil!")
                    print("   Silakan login dengan akun baru Anda.")
                
                input("\nPress Enter to continue...")
            
            elif action == 'login':
                # Login
                clear_screen()
                username = login()
                
                if username:
                    # Login success
                    current_session.login(username)
                    
                    # Store master password for encryption
                    # (Already entered during login, we'll ask again in dashboard)
                    
                    input("\nPress Enter to continue...")
                else:
                    # Login failed
                    input("\nPress Enter to continue...")
            
            elif action == 'exit':
                # Exit program
                if confirm_action("Keluar dari CipherVault+?"):
                    clear_screen()
                    print("\n" + "="*60)
                    print("  Thank you for using CipherVault+!")
                    print("  Your data is safely encrypted and stored locally.")
                    print("="*60)
                    print("\n  Goodbye! 👋\n")
                    sys.exit(0)


# ==================== PROGRAM ENTRY POINT ====================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\n\n  Program terminated by user (Ctrl+C)")
        print("  Goodbye! 👋\n")
        sys.exit(0)
    except Exception as e:
        # Handle unexpected errors
        print(f"\n❌ Unexpected error: {e}")
        print("  Please report this bug to the developer.")
        sys.exit(1)