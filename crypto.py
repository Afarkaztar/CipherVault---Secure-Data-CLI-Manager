"""
crypto.py
=========
Cryptography module untuk CipherVault+
Implementasi enkripsi 2-layer:
1. Caesar Cipher (shift encryption)
2. Base64 Encoding (obfuscation)

Topik Praktikum yang diimplementasi:
- Fungsi dengan parameter & return value
- String manipulation (heavy)
- Character manipulation dengan ord() dan chr()
"""

import base64


# ==================== CAESAR CIPHER ====================

def caesar_encrypt(text, shift):
    """
    Encrypt text menggunakan Caesar Cipher
    
    Cara kerja:
    - Setiap huruf digeser sebanyak 'shift' posisi di alfabet
    - Huruf besar tetap besar, huruf kecil tetap kecil
    - Karakter non-alfabet tidak diubah
    
    Args:
        text (str): Plain text yang akan dienkripsi
        shift (int): Jumlah pergeseran (0-25)
    
    Returns:
        str: Encrypted text
    
    Example:
        >>> caesar_encrypt("Hello", 3)
        "Khoor"
    """
    result = ""
    
    for char in text:
        if char.isalpha():
            # Tentukan base ASCII (65 untuk A, 97 untuk a)
            ascii_offset = 65 if char.isupper() else 97
            
            # Shift character dengan modulo 26 (jumlah huruf)
            shifted = (ord(char) - ascii_offset + shift) % 26
            
            # Convert kembali ke character
            result += chr(shifted + ascii_offset)
        else:
            # Karakter non-alfabet tidak diubah
            result += char
    
    return result


def caesar_decrypt(text, shift):
    """
    Decrypt text yang dienkripsi dengan Caesar Cipher
    
    Args:
        text (str): Encrypted text
        shift (int): Jumlah pergeseran yang sama dengan saat encrypt
    
    Returns:
        str: Decrypted text (plain text)
    
    Example:
        >>> caesar_decrypt("Khoor", 3)
        "Hello"
    """
    # Decrypt = encrypt dengan shift negatif
    return caesar_encrypt(text, -shift)


# ==================== BASE64 ENCODING ====================

def base64_encode(text):
    """
    Encode text ke Base64
    
    Base64 bukan enkripsi, tapi encoding untuk:
    - Convert binary data ke ASCII text
    - Obfuscation tambahan (susah dibaca manusia)
    
    Args:
        text (str): Plain text
    
    Returns:
        str: Base64 encoded string
    
    Example:
        >>> base64_encode("Hello")
        "SGVsbG8="
    """
    # Convert string ke bytes, lalu encode
    text_bytes = text.encode('utf-8')
    base64_bytes = base64.b64encode(text_bytes)
    
    # Convert bytes kembali ke string
    return base64_bytes.decode('utf-8')


def base64_decode(encoded_text):
    """
    Decode Base64 string kembali ke plain text
    
    Args:
        encoded_text (str): Base64 encoded string
    
    Returns:
        str: Decoded plain text
    
    Example:
        >>> base64_decode("SGVsbG8=")
        "Hello"
    """
    try:
        # Convert string ke bytes, lalu decode
        encoded_bytes = encoded_text.encode('utf-8')
        decoded_bytes = base64.b64decode(encoded_bytes)
        
        # Convert bytes kembali ke string
        return decoded_bytes.decode('utf-8')
    except Exception as e:
        # Jika gagal decode, return string kosong
        print(f"Error decoding Base64: {e}")
        return ""


# ==================== KEY DERIVATION ====================

def derive_key_from_password(master_password):
    """
    Generate shift key dari master password
    
    Cara kerja:
    - Jumlahkan nilai ASCII semua karakter di password
    - Modulo 26 untuk dapat shift 0-25
    
    Args:
        master_password (str): Master password user
    
    Returns:
        int: Shift key (0-25)
    
    Example:
        >>> derive_key_from_password("MyPass123")
        15  # (sum of ASCII values) % 26
    """
    # Sum semua nilai ASCII
    ascii_sum = sum(ord(char) for char in master_password)
    
    # Modulo 26 untuk dapat shift 0-25
    shift = ascii_sum % 26
    
    return shift


# ==================== 2-LAYER ENCRYPTION ====================

def encrypt_password(plain_password, master_password):
    """
    Encrypt password dengan 2-layer encryption
    
    Layer 1: Caesar Cipher dengan key dari master_password
    Layer 2: Base64 encoding
    
    Args:
        plain_password (str): Password asli yang akan dienkripsi
        master_password (str): Master password user (sebagai key)
    
    Returns:
        str: Encrypted password (2-layer)
    
    Example:
        >>> encrypt_password("mypass123", "MasterKey")
        "bXlwYXNzMTIz"  # Hasil akan berbeda tergantung shift
    """
    # Derive shift key dari master password
    shift = derive_key_from_password(master_password)
    
    # Layer 1: Caesar Cipher
    caesar_encrypted = caesar_encrypt(plain_password, shift)
    
    # Layer 2: Base64 Encoding
    final_encrypted = base64_encode(caesar_encrypted)
    
    return final_encrypted


def decrypt_password(encrypted_password, master_password):
    """
    Decrypt password yang dienkripsi 2-layer
    
    Proses reverse dari encrypt:
    Layer 1: Base64 decode
    Layer 2: Caesar Cipher decrypt
    
    Args:
        encrypted_password (str): Password terenkripsi
        master_password (str): Master password user (sebagai key)
    
    Returns:
        str: Plain password (decrypted)
    
    Example:
        >>> decrypt_password("bXlwYXNzMTIz", "MasterKey")
        "mypass123"
    """
    # Derive shift key dari master password (harus sama dengan saat encrypt)
    shift = derive_key_from_password(master_password)
    
    # Layer 1: Base64 Decode
    base64_decoded = base64_decode(encrypted_password)
    
    # Jika gagal decode, return string kosong
    if not base64_decoded:
        return ""
    
    # Layer 2: Caesar Cipher Decrypt
    final_decrypted = caesar_decrypt(base64_decoded, shift)
    
    return final_decrypted


# ==================== PASSWORD GENERATOR (BONUS) ====================

def generate_strong_password(length=12):
    """
    Generate random strong password
    
    Rules:
    - Minimal 12 karakter
    - Mix huruf besar, kecil, angka, special char
    
    Args:
        length (int): Panjang password (default 12)
    
    Returns:
        str: Generated password
    """
    import random
    import string
    
    # Pool karakter
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special = "!@#$%^&*"
    
    # Gabung semua pool
    all_chars = lowercase + uppercase + digits + special
    
    # Generate password
    password = ''.join(random.choice(all_chars) for _ in range(length))
    
    # Pastikan ada minimal 1 dari setiap jenis
    if (any(c.islower() for c in password) and
        any(c.isupper() for c in password) and
        any(c.isdigit() for c in password) and
        any(c in special for c in password)):
        return password
    else:
        # Jika tidak memenuhi, generate ulang (rekursif)
        return generate_strong_password(length)


# ==================== TESTING ====================

if __name__ == "__main__":
    print("Testing crypto.py...")
    print("=" * 60)
    
    # Test Caesar Cipher
    print("\n1. Testing Caesar Cipher:")
    plain = "Hello World 123"
    shift = 3
    encrypted = caesar_encrypt(plain, shift)
    decrypted = caesar_decrypt(encrypted, shift)
    
    print(f"   Plain text : {plain}")
    print(f"   Shift      : {shift}")
    print(f"   Encrypted  : {encrypted}")
    print(f"   Decrypted  : {decrypted}")
    print(f"   Match      : {'✓' if plain == decrypted else '✗'}")
    
    # Test Base64
    print("\n2. Testing Base64:")
    plain = "Secret Password"
    encoded = base64_encode(plain)
    decoded = base64_decode(encoded)
    
    print(f"   Plain text : {plain}")
    print(f"   Encoded    : {encoded}")
    print(f"   Decoded    : {decoded}")
    print(f"   Match      : {'✓' if plain == decoded else '✗'}")
    
    # Test Key Derivation
    print("\n3. Testing Key Derivation:")
    passwords = ["MyPassword", "AnotherPass", "Test123"]
    for pwd in passwords:
        shift = derive_key_from_password(pwd)
        print(f"   Master Password: '{pwd}' → Shift: {shift}")
    
    # Test 2-Layer Encryption
    print("\n4. Testing 2-Layer Encryption:")
    plain_pass = "mySecretPass123"
    master_pass = "MasterKey456"
    
    encrypted = encrypt_password(plain_pass, master_pass)
    decrypted = decrypt_password(encrypted, master_pass)
    
    print(f"   Plain Password   : {plain_pass}")
    print(f"   Master Password  : {master_pass}")
    print(f"   Encrypted (2L)   : {encrypted}")
    print(f"   Decrypted        : {decrypted}")
    print(f"   Match            : {'✓' if plain_pass == decrypted else '✗'}")
    
    # Test dengan master password berbeda (harus gagal)
    print("\n5. Testing dengan Wrong Master Password:")
    wrong_master = "WrongKey"
    wrong_decrypt = decrypt_password(encrypted, wrong_master)
    
    print(f"   Encrypted        : {encrypted}")
    print(f"   Wrong Master     : {wrong_master}")
    print(f"   Wrong Decrypt    : {wrong_decrypt}")
    print(f"   Should Fail      : {'✓' if plain_pass != wrong_decrypt else '✗'}")
    
    # Test Password Generator
    print("\n6. Testing Password Generator:")
    for i in range(3):
        generated = generate_strong_password(12)
        print(f"   Generated #{i+1}   : {generated}")
    
    print("\n" + "=" * 60)
    print("✅ Crypto testing complete!")