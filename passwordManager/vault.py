import json
import os
import shutil
from datetime import datetime
from crypto import encrypt_data, decrypt_data

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT_DIR = os.path.join(BASE_DIR, "vaults")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")

# Tạo thư mục
os.makedirs(VAULT_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)

def get_vault_path(username):
    return os.path.join(VAULT_DIR, f"{username}.json")

def load_vault(master_password, username="default"):
    vault_file = get_vault_path(username)
    
    if not os.path.exists(vault_file):
        return []
    
    with open(vault_file, "rb") as f:
        encrypted_data = f.read()
    
    if not encrypted_data:
        return []
    
    try:
        decrypted_bytes = decrypt_data(encrypted_data, master_password)
        return json.loads(decrypted_bytes.decode('utf-8'))
    except Exception:
        raise Exception("Sai mật khẩu hoặc file bị hỏng!")

def save_vault(vault_data, master_password, username="default"):
    vault_file = get_vault_path(username)
    json_str = json.dumps(vault_data, ensure_ascii=False, indent=2)
    encrypted_data = encrypt_data(json_str.encode('utf-8'), master_password)
    
    with open(vault_file, "wb") as f:
        f.write(encrypted_data)

def list_vaults():
    vaults = []
    for file in os.listdir(VAULT_DIR):
        if file.endswith(".json"):
            vaults.append(file.replace(".json", ""))
    return vaults

def delete_vault(username):
    vault_file = get_vault_path(username)
    if os.path.exists(vault_file):
        os.remove(vault_file)
        return True
    return False

def backup_vault(username):
    """Tạo backup cho vault"""
    vault_file = get_vault_path(username)
    if not os.path.exists(vault_file):
        return False
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_DIR, f"{username}_backup_{timestamp}.json")
    shutil.copy2(vault_file, backup_file)
    return backup_file

def list_backups(username=None):
    """Liệt kê các file backup"""
    backups = []
    for file in os.listdir(BACKUP_DIR):
        if file.endswith(".json"):
            if username and not file.startswith(username):
                continue
            backups.append(file)
    return sorted(backups, reverse=True)

def restore_backup(username, backup_file):
    """Phục hồi từ backup"""
    backup_path = os.path.join(BACKUP_DIR, backup_file)
    if not os.path.exists(backup_path):
        return False
    
    vault_file = get_vault_path(username)
    shutil.copy2(backup_path, vault_file)
    return True

def user_exists(username):
    """Kiểm tra username đã tồn tại chưa"""
    return os.path.exists(get_vault_path(username))