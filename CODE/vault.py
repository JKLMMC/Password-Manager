import json
import os
import sys

# Đảm bảo thư mục gốc của project luôn trong sys.path
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if _BASE_DIR not in sys.path:
    sys.path.insert(0, _BASE_DIR)

from crypto import encrypt_data, decrypt_data

# Dùng absolute path để tránh lỗi khi chạy từ thư mục khác
VAULT_FILE = os.path.join(_BASE_DIR, "vault.json")

def load_vault(master_password):
    """Tải và giải mã vault. Trả về list[] nếu chưa có file."""
    if not os.path.exists(VAULT_FILE):
        return []

    with open(VAULT_FILE, "rb") as f:
        encrypted_data = f.read()

    if len(encrypted_data) == 0:
        return []

    try:
        decrypted_bytes = decrypt_data(encrypted_data, master_password)
        return json.loads(decrypted_bytes.decode('utf-8'))
    except Exception:
        raise Exception("Sai mật khẩu hoặc file bị hỏng!")

def save_vault(vault_data, master_password):
    """Mã hóa và lưu vault xuống file."""
    json_str = json.dumps(vault_data, ensure_ascii=False, indent=2)
    encrypted_data = encrypt_data(json_str.encode('utf-8'), master_password)

    with open(VAULT_FILE, "wb") as f:
        f.write(encrypted_data)