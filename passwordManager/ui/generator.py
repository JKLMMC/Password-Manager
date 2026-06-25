import tkinter as tk
from tkinter import messagebox
import pyperclip
from crypto import generate_password, check_password_strength

class PasswordGenerator:
    def __init__(self, master, callback):
        self.callback = callback
        
        self.window = tk.Toplevel(master)
        self.window.title("🔑 Tạo mật khẩu")
        self.window.geometry("500x480")
        self.window.resizable(False, False)
        
        tk.Label(self.window, text="🔑 TẠO MẬT KHẨU MẠNH", 
                 font=("Arial", 16, "bold")).pack(pady=15)
        
        # === ĐỘ DÀI ===
        frame1 = tk.Frame(self.window)
        frame1.pack(pady=5)
        tk.Label(frame1, text="Độ dài:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.length_var = tk.StringVar(value="14")
        tk.Spinbox(frame1, from_=8, to_=32, textvariable=self.length_var, 
                   width=5).pack(side=tk.LEFT, padx=5)
        
        # === TÙY CHỌN KÝ TỰ ===
        frame2 = tk.Frame(self.window)
        frame2.pack(pady=10)
        
        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=True)
        
        tk.Checkbutton(frame2, text="Chữ hoa", variable=self.use_upper).pack(side=tk.LEFT, padx=5)
        tk.Checkbutton(frame2, text="Chữ thường", variable=self.use_lower).pack(side=tk.LEFT, padx=5)
        tk.Checkbutton(frame2, text="Số", variable=self.use_digits).pack(side=tk.LEFT, padx=5)
        tk.Checkbutton(frame2, text="Ký tự đặc biệt", variable=self.use_special).pack(side=tk.LEFT, padx=5)
        
        # === NÚT TẠO ===
        tk.Button(self.window, text="🔄 Tạo mới", 
                  command=self.generate, width=15, bg="#2196F3", fg="white").pack(pady=10)
        
        # === HIỂN THỊ MẬT KHẨU ===
        self.password_label = tk.Label(self.window, text="", 
                                       font=("Arial", 16, "bold"), fg="blue")
        self.password_label.pack(pady=10)
        
        # === ĐỘ MẠNH ===
        self.strength_label = tk.Label(self.window, text="", font=("Arial", 11))
        self.strength_label.pack(pady=5)
        
        # === NÚT CHỌN ===
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text="✅ Chọn", command=self.select_password, 
                  width=12, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="📋 Copy", command=self.copy_password, 
                  width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🔙 Quay lại", command=self.close_window, 
                  width=12, bg="#f44336", fg="white").pack(side=tk.LEFT, padx=5)
        
        # Tạo lần đầu
        self.generate()
    
    def generate(self):
        """Tạo mật khẩu với tùy chọn"""
        try:
            length = int(self.length_var.get())
            
            password = generate_password(
                length=length,
                use_upper=self.use_upper.get(),
                use_lower=self.use_lower.get(),
                use_digits=self.use_digits.get(),
                use_special=self.use_special.get()
            )
            
            self.password_label.config(text=password)
            
            # Kiểm tra độ mạnh
            score, label, color = check_password_strength(password)
            self.strength_label.config(text=f"Độ mạnh: {label} (Điểm: {score}/100)", fg=color)
            
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def select_password(self):
        """Chọn mật khẩu và gọi callback"""
        password = self.password_label.cget("text")
        if password:
            self.callback(password)
            self.window.destroy()
    
    def copy_password(self):
        """Copy vào clipboard"""
        password = self.password_label.cget("text")
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Thành công", "✅ Đã copy mật khẩu vào clipboard!")
    
    def close_window(self):
        """Đóng cửa sổ, quay lại dashboard"""
        self.window.destroy()