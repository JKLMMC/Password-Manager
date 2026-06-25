import tkinter as tk
from tkinter import messagebox
import pyperclip
from vault import save_vault, list_vaults, delete_vault, backup_vault, load_vault
from ui.generator import PasswordGenerator
from ui.search import SearchWindow
from ui.settings import SettingsWindow
from crypto import check_password_strength


class Dashboard:
    def __init__(self, master, vault_data, master_password, username):
        self.master = master
        self.vault_data = vault_data
        self.master_password = master_password
        self.username = username
        self.selected_index = None
        
        self.master.title(f"🔐 Password Manager - {username}")
        self.master.geometry("850x700")
        self.master.resizable(True, True)
        
        # === TOP BAR ===
        top_frame = tk.Frame(self.master)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(top_frame, text=f"👤 {username} | 📁 {len(self.vault_data)} mật khẩu", 
                 font=("Arial", 10)).pack(side=tk.LEFT)
        
        # === THANH CÔNG CỤ ===
        toolbar = tk.Frame(self.master)
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(toolbar, text="🔍 Tìm kiếm", command=self.open_search,
                  width=12).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="📁 Đổi vault", command=self.switch_vault,
                  width=12).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="📤 Backup", command=self.do_backup,
                  width=12).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="⚙️ Cài đặt", command=self.open_settings,
                  width=12).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="🔒 Khóa & Thoát", command=self.logout,
                  width=14, fg="red").pack(side=tk.RIGHT, padx=2)
        
        # === DANH SÁCH ===
        tk.Label(self.master, text="📋 Danh sách tài khoản:", 
                 font=("Arial", 12, "bold")).pack(anchor=tk.W, padx=10, pady=(10,5))
        
        list_frame = tk.Frame(self.master)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0,10))
        
        self.listbox = tk.Listbox(list_frame, font=("Arial", 11), height=12)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)
        
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        
        # === FORM NHẬP ===
        form_frame = tk.LabelFrame(self.master, text="Thông tin tài khoản", padx=10, pady=10)
        form_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(form_frame, text="Site:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.site_entry = tk.Entry(form_frame, width=35)
        self.site_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Username:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.user_entry = tk.Entry(form_frame, width=35)
        self.user_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.pass_entry = tk.Entry(form_frame, width=35)
        self.pass_entry.grid(row=2, column=1, padx=5, pady=5)
        self.pass_entry.bind('<KeyRelease>', self.check_password_strength)
        
        # Label hiển thị độ mạnh password
        self.strength_label = tk.Label(form_frame, text="", font=("Arial", 9))
        self.strength_label.grid(row=3, column=0, columnspan=2, sticky=tk.W, padx=5, pady=2)
        
        # Nút tạo mật khẩu
        tk.Button(form_frame, text="🔑 Tạo mật khẩu", 
                  command=self.open_generator).grid(row=2, column=2, padx=5)
        
        # === NÚT CHỨC NĂNG ===
        btn_frame = tk.Frame(self.master)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="➕ Thêm", command=self.add_entry, 
                  width=10, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="✏️ Sửa", command=self.edit_entry, 
                  width=10, bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🗑 Xóa", command=self.delete_entry, 
                  width=10, bg="#f44336", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="📋 Copy Pass", command=self.copy_password, 
                  width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🔄 Làm mới", command=self.refresh_list, 
                  width=12).pack(side=tk.LEFT, padx=5)
        
        self.update_listbox()
    
    # ==================== CÁC HÀM CHÍNH ====================
    
    def update_listbox(self):
        """Cập nhật danh sách"""
        self.listbox.delete(0, tk.END)
        for entry in self.vault_data:
            self.listbox.insert(tk.END, f"{entry['site']} - {entry['username']}")
        
        # Cập nhật số lượng
        self.master.title(f"🔐 Password Manager - {self.username} ({len(self.vault_data)})")
    
    def clear_form(self):
        """Xóa form"""
        self.site_entry.delete(0, tk.END)
        self.user_entry.delete(0, tk.END)
        self.pass_entry.delete(0, tk.END)
        self.strength_label.config(text="")
        self.selected_index = None
        self.listbox.selection_clear(0, tk.END)
    
    def save_and_refresh(self):
        """Lưu và refresh"""
        save_vault(self.vault_data, self.master_password, self.username)
        self.update_listbox()
        self.clear_form()
        messagebox.showinfo("Thành công", "✅ Đã lưu thay đổi!")
    
    def refresh_list(self):
        """Refresh danh sách từ file"""
        try:
            self.vault_data = load_vault(self.master_password, self.username)
            self.update_listbox()
            self.clear_form()
            messagebox.showinfo("Thành công", "Đã làm mới danh sách!")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    # ==================== CHỌN VÀ HIỂN THỊ ====================
    
    def on_select(self, event):
        """Chọn entry"""
        selection = self.listbox.curselection()
        if selection:
            self.selected_index = selection[0]
            entry = self.vault_data[self.selected_index]
            self.site_entry.delete(0, tk.END)
            self.site_entry.insert(0, entry['site'])
            self.user_entry.delete(0, tk.END)
            self.user_entry.insert(0, entry['username'])
            self.pass_entry.delete(0, tk.END)
            self.pass_entry.insert(0, entry['password'])
            self.check_password_strength()
    
    def check_password_strength(self, event=None):
        """Kiểm tra độ mạnh password"""
        password = self.pass_entry.get()
        if password:
            score, label, color = check_password_strength(password)
            self.strength_label.config(text=f"Độ mạnh: {label} (Điểm: {score}/100)", fg=color)
        else:
            self.strength_label.config(text="")
    
    # ==================== THÊM / SỬA / XÓA ====================
    
    def add_entry(self):
        """Thêm mới"""
        site = self.site_entry.get().strip()
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        
        if not site or not username or not password:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ!")
            return
        
        # Kiểm tra trùng
        for entry in self.vault_data:
            if entry['site'].lower() == site.lower():
                messagebox.showwarning("Lỗi", f"Site '{site}' đã tồn tại!")
                return
        
        self.vault_data.append({
            'site': site,
            'username': username,
            'password': password
        })
        save_vault(self.vault_data, self.master_password, self.username)
        self.update_listbox()
        self.clear_form()
        messagebox.showinfo("Thành công", f"✅ Đã thêm {site}!")
    
    def edit_entry(self):
        """Sửa"""
        if self.selected_index is None:
            messagebox.showwarning("Lỗi", "Chọn tài khoản cần sửa!")
            return
        
        site = self.site_entry.get().strip()
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        
        if not site or not username or not password:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ!")
            return
        
        self.vault_data[self.selected_index] = {
            'site': site,
            'username': username,
            'password': password
        }
        save_vault(self.vault_data, self.master_password, self.username)
        self.update_listbox()
        self.clear_form()
        messagebox.showinfo("Thành công", f"✅ Đã cập nhật {site}!")
    
    def delete_entry(self):
        """Xóa"""
        if self.selected_index is None:
            messagebox.showwarning("Lỗi", "Chọn tài khoản cần xóa!")
            return
        
        entry = self.vault_data[self.selected_index]
        if messagebox.askyesno("Xác nhận", f"Xóa '{entry['site']}'?"):
            del self.vault_data[self.selected_index]
            save_vault(self.vault_data, self.master_password, self.username)
            self.update_listbox()
            self.clear_form()
            messagebox.showinfo("Thành công", "✅ Đã xóa!")
    
    # ==================== COPY / GENERATOR ====================
    
    def copy_password(self):
        """Copy password"""
        if self.selected_index is None:
            messagebox.showwarning("Lỗi", "Chọn tài khoản!")
            return
        
        password = self.vault_data[self.selected_index]['password']
        pyperclip.copy(password)
        messagebox.showinfo("Thành công", "✅ Đã copy mật khẩu vào clipboard!")
    
    def open_generator(self):
        """Mở cửa sổ tạo mật khẩu"""
        PasswordGenerator(self.master, self.set_password)
    
    def set_password(self, password):
        """Callback từ generator"""
        self.pass_entry.delete(0, tk.END)
        self.pass_entry.insert(0, password)
        self.check_password_strength()
    
    # ==================== TÌM KIẾM ====================
    
    def open_search(self):
        """Mở cửa sổ tìm kiếm"""
        def select_callback(entry):
            for i, e in enumerate(self.vault_data):
                if e['site'] == entry['site'] and e['username'] == entry['username']:
                    self.selected_index = i
                    self.site_entry.delete(0, tk.END)
                    self.site_entry.insert(0, entry['site'])
                    self.user_entry.delete(0, tk.END)
                    self.user_entry.insert(0, entry['username'])
                    self.pass_entry.delete(0, tk.END)
                    self.pass_entry.insert(0, entry['password'])
                    self.check_password_strength()
                    self.listbox.selection_clear(0, tk.END)
                    self.listbox.selection_set(i)
                    self.listbox.see(i)
                    break
        
        SearchWindow(self.master, self.vault_data, select_callback)
    
    # ==================== QUẢN LÝ VAULT ====================
    
    def switch_vault(self):
        """Đổi sang vault khác"""
        vaults = list_vaults()
        if not vaults:
            messagebox.showinfo("Thông báo", "Chưa có vault nào khác!")
            return
        
        # Tạo popup chọn vault
        window = tk.Toplevel(self.master)
        window.title("Chọn vault")
        window.geometry("300x300")
        window.resizable(False, False)
        
        tk.Label(window, text="Chọn vault:", font=("Arial", 12, "bold")).pack(pady=10)
        
        listbox = tk.Listbox(window, font=("Arial", 11), height=10)
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for v in vaults:
            if v != self.username:
                listbox.insert(tk.END, v)
        
        def load_selected():
            selection = listbox.curselection()
            if selection:
                name = listbox.get(selection[0])
                window.destroy()
                
                try:
                    vault_data = load_vault(self.master_password, name)
                    self.username = name
                    self.vault_data = vault_data
                    self.master.title(f"🔐 Password Manager - {name}")
                    self.update_listbox()
                    self.clear_form()
                    messagebox.showinfo("Thành công", f"✅ Đã chuyển sang vault: {name}")
                except Exception as e:
                    messagebox.showerror("Lỗi", str(e))
        
        tk.Button(window, text="Chọn", command=load_selected, 
                  width=15).pack(pady=10)
    
    def do_backup(self):
        """Tạo backup"""
        result = backup_vault(self.username)
        if result:
            import os
            messagebox.showinfo("Thành công", 
                               f"✅ Đã tạo backup!\n\n📁 {os.path.basename(result)}")
        else:
            messagebox.showwarning("Lỗi", "Không có dữ liệu để backup!")
    
    # ==================== CÀI ĐẶT ====================
    
    def open_settings(self):
        """Mở cửa sổ cài đặt"""
        def refresh_callback(new_password=None, new_data=None):
            if new_password:
                self.master_password = new_password
            if new_data is not None:
                self.vault_data = new_data
                self.update_listbox()
        
        SettingsWindow(self.master, self.username, self.master_password, 
                      self.vault_data, refresh_callback)
    
    # ==================== THOÁT ====================
    
    def logout(self):
        """Thoát"""
        if messagebox.askyesno("Xác nhận", "Lưu thay đổi trước khi thoát?"):
            save_vault(self.vault_data, self.master_password, self.username)
        self.master.destroy()