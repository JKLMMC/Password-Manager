import tkinter as tk
from tkinter import messagebox, ttk
import os
from vault import backup_vault, list_backups, restore_backup, delete_vault, save_vault
from crypto import change_password, check_password_strength

class SettingsWindow:
    def __init__(self, master, username, master_password, vault_data, refresh_callback):
        self.master = master
        self.username = username
        self.master_password = master_password
        self.vault_data = vault_data
        self.refresh_callback = refresh_callback
        
        self.window = tk.Toplevel(master)
        self.window.title("⚙️ Cài đặt")
        self.window.geometry("550x550")
        self.window.resizable(False, False)
        
        # === TAB CONTROL ===
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Đổi mật khẩu
        tab1 = tk.Frame(notebook)
        notebook.add(tab1, text="🔑 Đổi Master Password")
        self.setup_change_password(tab1)
        
        # Tab 2: Backup
        tab2 = tk.Frame(notebook)
        notebook.add(tab2, text="💾 Backup & Restore")
        self.setup_backup(tab2)
        
        # Tab 3: Thông tin
        tab3 = tk.Frame(notebook)
        notebook.add(tab3, text="ℹ️ Thông tin")
        self.setup_info(tab3)
        
        # ===== NÚT QUAY LẠI (THÊM VÀO ĐÂY) =====
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="🔙 Quay lại", command=self.close_window,
                  width=20, height=2, bg="#f44336", fg="white", 
                  font=("Arial", 11, "bold")).pack()
    
    def setup_change_password(self, parent):
        """Giao diện đổi master password"""
        tk.Label(parent, text="ĐỔI MASTER PASSWORD", 
                 font=("Arial", 14, "bold")).pack(pady=15)
        
        tk.Label(parent, text="⚠️ Cảnh báo: Đổi mật khẩu sẽ mã hóa lại toàn bộ dữ liệu!", 
                 font=("Arial", 10), fg="red").pack(pady=5)
        
        frame = tk.Frame(parent)
        frame.pack(pady=20)
        
        tk.Label(frame, text="Mật khẩu cũ:", font=("Arial", 11)).grid(row=0, column=0, pady=8, padx=5)
        self.old_pass = tk.Entry(frame, width=25, show="•", font=("Arial", 12))
        self.old_pass.grid(row=0, column=1, pady=8, padx=5)
        
        tk.Label(frame, text="Mật khẩu mới:", font=("Arial", 11)).grid(row=1, column=0, pady=8, padx=5)
        self.new_pass = tk.Entry(frame, width=25, show="•", font=("Arial", 12))
        self.new_pass.grid(row=1, column=1, pady=8, padx=5)
        self.new_pass.bind('<KeyRelease>', self.check_new_strength)
        
        # Nút tạo mật khẩu mạnh
        self.gen_btn = tk.Button(frame, text="🔑 Tạo mật khẩu mạnh", 
                                 command=self.generate_new_password,
                                 font=("Arial", 9), bg="#FF9800", fg="white")
        self.gen_btn.grid(row=1, column=2, padx=5)
        
        self.strength_label = tk.Label(frame, text="", font=("Arial", 9))
        self.strength_label.grid(row=2, column=0, columnspan=3, pady=5)
        
        tk.Label(frame, text="Xác nhận mới:", font=("Arial", 11)).grid(row=3, column=0, pady=8, padx=5)
        self.confirm_new = tk.Entry(frame, width=25, show="•", font=("Arial", 12))
        self.confirm_new.grid(row=3, column=1, pady=8, padx=5)
        
        tk.Button(parent, text="🔄 Đổi mật khẩu", command=self.change_password,
                  width=20, height=2, bg="#FF9800", fg="white",
                  font=("Arial", 11, "bold")).pack(pady=20)
    
    def generate_new_password(self):
        """Tạo mật khẩu mới mạnh"""
        from crypto import generate_password
        password = generate_password(length=16, use_upper=True, use_lower=True,
                                     use_digits=True, use_special=True)
        
        self.new_pass.delete(0, tk.END)
        self.new_pass.insert(0, password)
        self.confirm_new.delete(0, tk.END)
        self.confirm_new.insert(0, password)
        
        import pyperclip
        pyperclip.copy(password)
        
        self.check_new_strength()
        messagebox.showinfo("Thành công", 
                           f"✅ Đã tạo mật khẩu mới!\n\n"
                           f"Mật khẩu: {password}\n\n"
                           f"📋 Đã copy vào clipboard!")
    
    def check_new_strength(self, event=None):
        password = self.new_pass.get()
        if password:
            score, label, color = check_password_strength(password)
            self.strength_label.config(text=f"Độ mạnh: {label} (Điểm: {score}/100)", fg=color)
        else:
            self.strength_label.config(text="")
    
    def change_password(self):
        old = self.old_pass.get()
        new = self.new_pass.get()
        confirm = self.confirm_new.get()
        
        if old != self.master_password:
            messagebox.showerror("Lỗi", "Mật khẩu cũ không đúng!")
            return
        
        if not new or len(new) < 6:
            messagebox.showerror("Lỗi", "Mật khẩu mới phải có ít nhất 6 ký tự!")
            return
        
        if new != confirm:
            messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp!")
            return
        
        # Kiểm tra độ mạnh
        score, label, color = check_password_strength(new)
        if score < 50:
            if not messagebox.askyesno("Cảnh báo", 
                                       f"⚠️ Mật khẩu mới {label}\n\n"
                                       "Mật khẩu yếu dễ bị tấn công!\n"
                                       "Bạn có muốn tiếp tục đổi không?"):
                return
        
        if messagebox.askyesno("Xác nhận", "Đổi master password? Dữ liệu sẽ được mã hóa lại."):
            try:
                import json
                json_str = json.dumps(self.vault_data, ensure_ascii=False, indent=2)
                from crypto import encrypt_data
                encrypted = encrypt_data(json_str.encode('utf-8'), new)
                
                from vault import get_vault_path
                with open(get_vault_path(self.username), "wb") as f:
                    f.write(encrypted)
                
                self.master_password = new
                messagebox.showinfo("Thành công", "✅ Đổi master password thành công!")
                self.window.destroy()
                self.refresh_callback(new)
                
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
    
    def setup_backup(self, parent):
        """Giao diện Backup & Restore"""
        tk.Label(parent, text="💾 BACKUP & RESTORE", 
                 font=("Arial", 14, "bold")).pack(pady=15)
        
        btn_frame = tk.Frame(parent)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="📤 Tạo Backup", command=self.create_backup,
                  width=15, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="📥 Restore", command=self.restore_backup,
                  width=15, bg="#FF9800", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🔄 Refresh", command=self.list_backups,
                  width=15).pack(side=tk.LEFT, padx=5)
        
        tk.Label(parent, text="Danh sách backup:", font=("Arial", 11)).pack(anchor=tk.W, padx=20)
        
        self.backup_listbox = tk.Listbox(parent, font=("Arial", 10), height=8)
        self.backup_listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.list_backups()
    
    def list_backups(self):
        self.backup_listbox.delete(0, tk.END)
        backups = list_backups(self.username)
        for backup in backups:
            self.backup_listbox.insert(tk.END, backup)
    
    def create_backup(self):
        result = backup_vault(self.username)
        if result:
            messagebox.showinfo("Thành công", f"✅ Đã tạo backup:\n{os.path.basename(result)}")
            self.list_backups()
        else:
            messagebox.showwarning("Lỗi", "Không có dữ liệu để backup!")
    
    def restore_backup(self):
        selection = self.backup_listbox.curselection()
        if not selection:
            messagebox.showwarning("Lỗi", "Chọn file backup để restore!")
            return
        
        backup_file = self.backup_listbox.get(selection[0])
        if messagebox.askyesno("Xác nhận", f"Restore từ {backup_file}? Dữ liệu hiện tại sẽ bị ghi đè!"):
            from vault import restore_backup
            if restore_backup(self.username, backup_file):
                messagebox.showinfo("Thành công", "✅ Restore thành công! Hãy đăng nhập lại.")
                self.window.destroy()
                from vault import load_vault
                new_data = load_vault(self.master_password, self.username)
                self.refresh_callback(None, new_data)
            else:
                messagebox.showerror("Lỗi", "Không thể restore!")
    
    def setup_info(self, parent):
        """Thông tin hệ thống"""
        tk.Label(parent, text="ℹ️ THÔNG TIN HỆ THỐNG", 
                 font=("Arial", 14, "bold")).pack(pady=15)
        
        info = f"""
        📁 Username: {self.username}
        🔐 Mã hóa: AES-256-GCM
        🔑 PBKDF2: 600,000 vòng
        📂 Số lượng mật khẩu: {len(self.vault_data)}
        📅 Ngày tạo: (Chưa cập nhật)
        """
        
        tk.Label(parent, text=info, font=("Arial", 11), justify=tk.LEFT,
                 bg="#f0f0f0", padx=20, pady=20).pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(parent, text="🔐 Password Manager v2.0 - Đồ án ATTT", 
                 font=("Arial", 9), fg="gray").pack(pady=10)
    
    # ===== THÊM HÀM NÀY VÀO CUỐI CLASS =====
    def close_window(self):
        """Đóng cửa sổ cài đặt, quay lại trang chủ"""
        self.window.destroy()