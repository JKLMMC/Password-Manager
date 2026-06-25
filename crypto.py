import hashlib
import os
import secrets
import string
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

SALT_LENGTH = 16
KEY_LENGTH = 32
NONCE_LENGTH = 12
ITERATIONS = 600000

def generate_salt():
    return os.urandom(SALT_LENGTH)

def derive_key(master_password, salt):
    return hashlib.pbkdf2_hmac(
        'sha256',
        master_password.encode('utf-8'),
        salt,
        ITERATIONS,
        dklen=KEY_LENGTH
    )

def encrypt_data(plaintext, master_password):
    salt = generate_salt()
    key = derive_key(master_password, salt)
    aesgcm = AESGCM(key)
    nonce = os.urandom(NONCE_LENGTH)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    return salt + nonce + ciphertext

def decrypt_data(encrypted_data, master_password):
    salt = encrypted_data[:SALT_LENGTH]
    nonce = encrypted_data[SALT_LENGTH:SALT_LENGTH + NONCE_LENGTH]
    ciphertext = encrypted_data[SALT_LENGTH + NONCE_LENGTH:]
    key = derive_key(master_password, salt)
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, None)

def generate_password(length=14, use_upper=True, use_lower=True,
                      use_digits=True, use_special=True):
    chars = ''
    required = []

    if use_upper:
        chars += string.ascii_uppercase
        required.append(secrets.choice(string.ascii_uppercase))
    if use_lower:
        chars += string.ascii_lowercase
        required.append(secrets.choice(string.ascii_lowercase))
    if use_digits:
        chars += string.digits
        required.append(secrets.choice(string.digits))
    if use_special:
        chars += "!@#$%^&*"
        required.append(secrets.choice("!@#$%^&*"))

    if not chars:
        chars = string.ascii_letters + string.digits
        required = []

    remaining = length - len(required)
    pool = required + [secrets.choice(chars) for _ in range(max(remaining, 0))]
    secrets.SystemRandom().shuffle(pool)
    return ''.join(pool[:length])

def check_password_strength(password):
    if not password:
        return 0, "", "#cccccc"

    score = 0
    if len(password) >= 8:
        score += 10
    if len(password) >= 12:
        score += 10
    if len(password) >= 16:
        score += 10
    if any(c.isupper() for c in password):
        score += 20
    if any(c.islower() for c in password):
        score += 20
    if any(c.isdigit() for c in password):
        score += 15
    if any(c in "!@#$%^&*()_+-=[]{}|;':\",./<>?" for c in password):
        score += 15

    if score <= 25:
        return score, "Rất yếu 🔴", "#e74c3c"
    elif score <= 50:
        return score, "Yếu 🟠", "#e67e22"
    elif score <= 70:
        return score, "Trung bình 🟡", "#f1c40f"
    elif score <= 85:
        return score, "Mạnh 🟢", "#2ecc71"
    else:
        return score, "Rất mạnh 💪", "#27ae60"

def change_password(old_password, new_password, vault_data):
    """Đổi master password: giải mã cũ → mã hóa mới"""
    import json
    json_str = json.dumps(vault_data, ensure_ascii=False, indent=2)
    return encrypt_data(json_str.encode('utf-8'), new_password)