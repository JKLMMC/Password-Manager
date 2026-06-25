import tkinter as tk
from tkinter import messagebox
import pyperclip
from vault import load_vault, save_vault, user_exists
from crypto import check_password_strength

class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("🔐 Password Manager")
        self.master.geometry("500x500")
        self.master.resizable(False, False)
        
        self.mode = "login"
        
        # === TIÊU ĐỀ ===
        self.title_label = tk.Label(master, text="🔐 ĐĂNG NHẬP", 
                                    font=("Arial", 22, "bold"), fg="#2196F3")
        self.title_label.pack(pady=20)
        
        # === FORM ===
        form_frame = tk.Frame(master)
        form_frame.pack(pady=15)
        
        # Username
        tk.Label(form_frame, text="Username:", font=("Arial", 11)).grid(row=0, column=0, pady=10, padx=5)
        self.username_entry = tk.Entry(form_frame, width=25, font=("Arial", 12))
        self.username_entry.grid(row=0, column=1, pady=10, padx=5)
        self.username_entry.focus()
        
        # Master Password
        tk.Label(form_frame, text="Master Password:", font=("Arial", 11)).grid(row=1, column=0, pady=10, padx=5)
        self.password_entry = tk.Entry(form_frame, width=25, font=("Arial", 12), show="•")
        self.password_entry.grid(row=1, column=1, pady=10, padx=5)
        
        # Độ mạnh password (chỉ hiện khi đăng ký)
        self.strength_label = tk.Label(form_frame, text="", font=("Arial", 9))
        self.password_entry.bind('<KeyRelease>', self.update_strength)
        
        # Xác nhận mật khẩu (chỉ hiện khi đăng ký)
        self.confirm_label = tk.Label(form_frame, text="Xác nhận:", font=("Arial", 11))
        self.confirm_entry = tk.Entry(form_frame, width=25, font=("Arial", 12), show="•")
           
        # === NÚT CHÍNH ===
        self.action_btn = tk.Button(master, text="🔓 Đăng nhập", 
                                    command=self.handle_action,
                                    width=22, height=2, bg="#4CAF50", fg="white",
                                    font=("Arial", 12, "bold"))
        self.action_btn.pack(pady=10)
        
        # === CHUYỂN MODE ===
        self.switch_btn = tk.Button(master, text="Chưa có tài khoản? Đăng ký", 
                                    command=self.switch_mode,
                                    font=("Arial", 10), fg="#2196F3", bd=0, cursor="hand2")
        self.switch_btn.pack()
        
        # === STATUS ===
        self.status_label = tk.Label(master, text="", font=("Arial", 9), fg="gray")
        self.status_label.pack(pady=5)
        
        self.master.bind('<Return>', lambda e: self.handle_action())
    
    def update_strength(self, event=None):
        """Hiển thị độ mạnh password khi đăng ký"""
        if self.mode == "register":
            password = self.password_entry.get()
            if password:
                score, label, color = check_password_strength(password)
                self.strength_label.grid(row=2, column=0, columnspan=2, pady=5)
                self.strength_label.config(text=f"Độ mạnh: {label}", fg=color)
            else:
                self.strength_label.grid_remove()
    
    def switch_mode(self):
        if self.mode == "login":
            self.mode = "register"
            self.title_label.config(text="📝 ĐĂNG KÝ", fg="#FF9800")
            self.action_btn.config(text="📝 Đăng ký", bg="#FF9800")
            self.switch_btn.config(text="Đã có tài khoản? Đăng nhập", fg="#4CAF50")
            self.status_label.config(text="Tạo master password mới", fg="#FF9800")
            
            self.confirm_label.grid(row=3, column=0, pady=10, padx=5)
            self.confirm_entry.grid(row=3, column=1, pady=10, padx=5)
            self.master.geometry("500x560")
        else:
            self.mode = "login"
            self.title_label.config(text="🔐 ĐĂNG NHẬP", fg="#2196F3")
            self.action_btn.config(text="🔓 Đăng nhập", bg="#4CAF50")
            self.switch_btn.config(text="Chưa có tài khoản? Đăng ký", fg="#2196F3")
            self.status_label.config(text="", fg="gray")
            
            self.confirm_label.grid_remove()
            self.confirm_entry.grid_remove()
            self.strength_label.grid_remove()
            self.master.geometry("500x500")
        
        self.password_entry.delete(0, tk.END)
        self.confirm_entry.delete(0, tk.END)
        self.password_entry.focus()
    
    def handle_action(self):
        username = self.username_entry.get().strip()
        master_pwd = self.password_entry.get().strip()
        
        if not username:
            messagebox.showwarning("Lỗi", "Vui lòng nhập username!")
            return
        
        if not master_pwd:
            messagebox.showwarning("Lỗi", "Vui lòng nhập master password!")
            return
        
        try:
            if self.mode == "login":
                # ===== ĐĂNG NHẬP =====
                if not user_exists(username):
                    messagebox.showwarning("Lỗi", f"Username '{username}' không tồn tại!")
                    return
                
                vault_data = load_vault(master_pwd, username)
                self.master.destroy()
                
                import ui.dashboard as dashboard
                root = tk.Tk()
                dashboard.Dashboard(root, vault_data, master_pwd, username)
                root.mainloop()
                
            else:
                # ===== ĐĂNG KÝ =====
                confirm_pwd = self.confirm_entry.get().strip()
                
                if master_pwd != confirm_pwd:
                    messagebox.showwarning("Lỗi", "Mật khẩu xác nhận không khớp!")
                    return
                
                if len(master_pwd) < 6:
                    messagebox.showwarning("Lỗi", "Mật khẩu phải có ít nhất 6 ký tự!")
                    return
                
                if user_exists(username):
                    messagebox.showwarning("Lỗi", f"Username '{username}' đã tồn tại!")
                    return
                
                # Tạo vault mới
                save_vault([], master_pwd, username)
                messagebox.showinfo("Thành công", 
                                   f"✅ Đăng ký thành công!\n\nUsername: {username}\n\n⚠️ Hãy nhớ kỹ master password này!\nNếu quên, dữ liệu sẽ bị mất vĩnh viễn!")
                
                self.switch_mode()
                self.username_entry.delete(0, tk.END)
                self.password_entry.delete(0, tk.END)
                self.confirm_entry.delete(0, tk.END)
                self.username_entry.focus()
                
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
            self.password_entry.delete(0, tk.END)
            if self.mode == "register":
                self.confirm_entry.delete(0, tk.END)