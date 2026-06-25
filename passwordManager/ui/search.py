import tkinter as tk

class SearchWindow:
    def __init__(self, master, vault_data, callback):
        self.master = master
        self.vault_data = vault_data
        self.callback = callback
        
        self.window = tk.Toplevel(master)
        self.window.title("🔍 Tìm kiếm mật khẩu")
        self.window.geometry("500x450")
        self.window.resizable(False, False)
        
        # === TIÊU ĐỀ ===
        tk.Label(self.window, text="🔍 TÌM KIẾM MẬT KHẨU", 
                 font=("Arial", 16, "bold")).pack(pady=10)
        
        # === Ô TÌM KIẾM ===
        search_frame = tk.Frame(self.window)
        search_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.search_entry = tk.Entry(search_frame, font=("Arial", 12), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.search_entry.bind('<KeyRelease>', self.search)
        self.search_entry.focus()
        
        tk.Button(search_frame, text="🔍 Tìm", command=self.search, 
                  width=10, bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=5)
        
        # === DANH SÁCH KẾT QUẢ ===
        self.result_listbox = tk.Listbox(self.window, font=("Arial", 11), height=12)
        self.result_listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.result_listbox.bind('<Double-Button-1>', self.select_result)
        
        # === SỐ LƯỢNG KẾT QUẢ ===
        self.count_label = tk.Label(self.window, text="0 kết quả", font=("Arial", 9))
        self.count_label.pack()
        
        # === NÚT QUAY LẠI ===
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text="🔙 Quay lại", command=self.close_window,
                  width=15, bg="#f44336", fg="white", font=("Arial", 10, "bold")).pack()
        
        self.results = []
    
    def close_window(self):
        """Đóng cửa sổ tìm kiếm, quay lại trang chủ"""
        self.window.destroy()
    
    def search(self, event=None):
        """Tìm kiếm theo site hoặc username"""
        keyword = self.search_entry.get().strip().lower()
        self.result_listbox.delete(0, tk.END)
        
        if not keyword:
            self.count_label.config(text="0 kết quả")
            return
        
        results = []
        for entry in self.vault_data:
            if keyword in entry['site'].lower() or keyword in entry['username'].lower():
                results.append(entry)
        
        for entry in results:
            self.result_listbox.insert(tk.END, f"{entry['site']} - {entry['username']}")
        
        self.count_label.config(text=f"{len(results)} kết quả")
        self.results = results
    
    def select_result(self, event):
        """Chọn kết quả và trả về callback"""
        selection = self.result_listbox.curselection()
        if selection and hasattr(self, 'results'):
            entry = self.results[selection[0]]
            self.callback(entry)
            self.window.destroy()