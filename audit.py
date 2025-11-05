"""
audit.py
========
Audit logging system untuk CipherVault+
Mencatat semua aktivitas user untuk security monitoring

Features:
- Auto logging semua aktivitas (Login, CRUD, Search, Logout)
- View audit history dengan filter
- Statistics generation

Topik Praktikum yang diimplementasi:
- File I/O operations
- Fungsi dengan parameter
- String manipulation (parsing)
- List untuk menyimpan log entries
"""

from datetime import datetime
from utils import get_file_path, format_timestamp, sanitize_input


# ==================== FILE PATH ====================

AUDIT_LOG_FILE = get_file_path('audit_log.txt')


# ==================== LOGGING FUNCTIONS ====================

def log_activity(username, action, details=""):
    """
    Log aktivitas user ke audit_log.txt
    
    Format: timestamp|username|action|details
    
    Args:
        username (str): Username yang melakukan aktivitas
        action (str): Jenis aktivitas (LOGIN, CREATE, READ, UPDATE, DELETE, SEARCH, LOGOUT)
        details (str): Detail tambahan (optional)
    
    Returns:
        bool: True jika berhasil log
    
    Example:
        >>> log_activity("dani", "LOGIN", "User logged in successfully")
        True
    """
    try:
        # Get timestamp sekarang
        timestamp = format_timestamp()
        
        # Sanitize input untuk hindari konflik dengan delimiter
        username = sanitize_input(username)
        action = sanitize_input(action)
        details = sanitize_input(details)
        
        # Format: timestamp|username|action|details
        log_entry = f"{timestamp}|{username}|{action}|{details}\n"
        
        # Append ke file
        with open(AUDIT_LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        
        return True
    
    except Exception as e:
        print(f"❌ Error logging activity: {e}")
        return False


def log_login(username):
    """Log aktivitas LOGIN"""
    return log_activity(username, "LOGIN", "User logged in successfully")


def log_logout(username):
    """Log aktivitas LOGOUT"""
    return log_activity(username, "LOGOUT", "User logged out")


def log_create_entry(username, entry_title):
    """Log aktivitas CREATE entry"""
    return log_activity(username, "CREATE", f"Created entry: {entry_title}")


def log_read_entry(username, entry_title):
    """Log aktivitas READ entry"""
    return log_activity(username, "READ", f"Viewed entry: {entry_title}")


def log_update_entry(username, entry_title):
    """Log aktivitas UPDATE entry"""
    return log_activity(username, "UPDATE", f"Updated entry: {entry_title}")


def log_delete_entry(username, entry_title):
    """Log aktivitas DELETE entry"""
    return log_activity(username, "DELETE", f"Deleted entry: {entry_title}")


def log_search(username, keyword):
    """Log aktivitas SEARCH"""
    return log_activity(username, "SEARCH", f"Searched for: {keyword}")


def log_register(username):
    """Log aktivitas REGISTER"""
    return log_activity(username, "REGISTER", "New user registered")


# ==================== READ LOGS ====================

def parse_log_line(line):
    """
    Parse satu baris log entry
    
    Args:
        line (str): Satu baris dari audit_log.txt
    
    Returns:
        dict: Dictionary berisi timestamp, username, action, details
              None jika format invalid
    
    Example:
        >>> parse_log_line("2025-10-28 10:30:00|dani|LOGIN|User logged in")
        {'timestamp': '2025-10-28 10:30:00', 'username': 'dani', 'action': 'LOGIN', 'details': 'User logged in'}
    """
    try:
        # Split by delimiter
        parts = line.strip().split('|')
        
        if len(parts) >= 4:
            return {
                'timestamp': parts[0],
                'username': parts[1],
                'action': parts[2],
                'details': parts[3]
            }
        elif len(parts) == 3:
            # Backward compatibility (tanpa details)
            return {
                'timestamp': parts[0],
                'username': parts[1],
                'action': parts[2],
                'details': ''
            }
        else:
            return None
    
    except Exception as e:
        print(f"Error parsing log line: {e}")
        return None


def read_all_logs():
    """
    Baca semua log entries dari file
    
    Returns:
        list: List of dictionaries berisi log entries
    
    Example:
        >>> logs = read_all_logs()
        >>> len(logs)
        10
    """
    logs = []
    
    try:
        # Check apakah file ada
        with open(AUDIT_LOG_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                log_entry = parse_log_line(line)
                if log_entry:
                    logs.append(log_entry)
    
    except FileNotFoundError:
        # File belum ada, return empty list
        pass
    
    except Exception as e:
        print(f"❌ Error reading logs: {e}")
    
    return logs


def get_user_logs(username):
    """
    Get semua log untuk user tertentu
    
    Args:
        username (str): Username yang dicari
    
    Returns:
        list: List of log entries untuk user tersebut
    """
    all_logs = read_all_logs()
    
    # Filter by username (case-insensitive)
    user_logs = [log for log in all_logs if log['username'].lower() == username.lower()]
    
    return user_logs


def get_logs_by_action(action):
    """
    Get semua log dengan action tertentu
    
    Args:
        action (str): Action type (LOGIN, CREATE, READ, UPDATE, DELETE, etc)
    
    Returns:
        list: List of log entries dengan action tersebut
    """
    all_logs = read_all_logs()
    
    # Filter by action (case-insensitive)
    filtered_logs = [log for log in all_logs if log['action'].upper() == action.upper()]
    
    return filtered_logs


def get_recent_logs(count=10):
    """
    Get N log entries terakhir
    
    Args:
        count (int): Jumlah log yang diambil (default 10)
    
    Returns:
        list: List of recent log entries
    """
    all_logs = read_all_logs()
    
    # Return N terakhir (reverse order)
    return all_logs[-count:] if len(all_logs) > count else all_logs


# ==================== DISPLAY LOGS ====================

def display_log_entry(log_entry):
    """
    Display single log entry dengan format rapi
    
    Args:
        log_entry (dict): Dictionary log entry
    """
    print(f"[{log_entry['timestamp']}] {log_entry['username']} - {log_entry['action']}")
    if log_entry['details']:
        print(f"  └─ {log_entry['details']}")


def display_logs(logs, title="Audit Logs"):
    """
    Display multiple log entries
    
    Args:
        logs (list): List of log entries
        title (str): Judul display
    """
    print("\n" + "="*60)
    print(f"  {title.upper()}")
    print("="*60)
    
    if not logs:
        print("  (No logs found)")
        return
    
    print(f"  Total: {len(logs)} entries\n")
    
    for log in logs:
        display_log_entry(log)
        print()  # Empty line between entries


# ==================== STATISTICS ====================

def get_user_statistics(username):
    """
    Generate statistics untuk user tertentu
    
    Args:
        username (str): Username
    
    Returns:
        dict: Dictionary berisi statistics
    
    Example:
        >>> stats = get_user_statistics("dani")
        >>> stats['total_activities']
        25
    """
    user_logs = get_user_logs(username)
    
    # Count by action type
    action_counts = {}
    for log in user_logs:
        action = log['action']
        action_counts[action] = action_counts.get(action, 0) + 1
    
    stats = {
        'username': username,
        'total_activities': len(user_logs),
        'action_breakdown': action_counts,
        'first_activity': user_logs[0]['timestamp'] if user_logs else None,
        'last_activity': user_logs[-1]['timestamp'] if user_logs else None
    }
    
    return stats


def display_statistics(stats):
    """
    Display statistics dengan format rapi
    
    Args:
        stats (dict): Dictionary statistics dari get_user_statistics()
    """
    print("\n" + "="*60)
    print(f"  STATISTICS FOR: {stats['username'].upper()}")
    print("="*60)
    
    print(f"\nTotal Activities: {stats['total_activities']}")
    
    if stats['first_activity']:
        print(f"First Activity  : {stats['first_activity']}")
    
    if stats['last_activity']:
        print(f"Last Activity   : {stats['last_activity']}")
    
    print("\nActivity Breakdown:")
    for action, count in stats['action_breakdown'].items():
        print(f"  • {action:<12} : {count} times")


# ==================== TESTING ====================

if __name__ == "__main__":
    print("Testing audit.py...")
    print("="*60)
    
    # Test logging berbagai aktivitas
    print("\n1. Testing Log Activities:")
    test_user = "test_user"
    
    activities = [
        ("REGISTER", "New user registered"),
        ("LOGIN", "User logged in"),
        ("CREATE", "Created entry: Gmail"),
        ("READ", "Viewed entry: Gmail"),
        ("UPDATE", "Updated entry: Gmail"),
        ("SEARCH", "Searched for: facebook"),
        ("DELETE", "Deleted entry: Old Account"),
        ("LOGOUT", "User logged out")
    ]
    
    for action, details in activities:
        success = log_activity(test_user, action, details)
        print(f"   {'✓' if success else '✗'} Logged: {action} - {details}")
    
    # Test read logs
    print("\n2. Testing Read Logs:")
    all_logs = read_all_logs()
    print(f"   Total logs in file: {len(all_logs)}")
    
    # Test get user logs
    print("\n3. Testing Get User Logs:")
    user_logs = get_user_logs(test_user)
    print(f"   Logs for '{test_user}': {len(user_logs)}")
    
    # Test filter by action
    print("\n4. Testing Filter by Action:")
    login_logs = get_logs_by_action("LOGIN")
    print(f"   Total LOGIN activities: {len(login_logs)}")
    
    # Test recent logs
    print("\n5. Testing Recent Logs (last 5):")
    recent = get_recent_logs(5)
    for log in recent:
        print(f"   - [{log['timestamp']}] {log['username']}: {log['action']}")
    
    # Test statistics
    print("\n6. Testing Statistics:")
    stats = get_user_statistics(test_user)
    display_statistics(stats)
    
    print("\n" + "="*60)
    print("✅ Audit testing complete!")
    print(f"Check the file: {AUDIT_LOG_FILE}")