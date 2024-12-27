import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import random
import string
import time
import os
import threading
from typing import Optional

class KeyGeneratorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("随机密钥生成器")
        
        self.settings_button = ttk.Button(root, text="⚙️ 设置", command=self.show_settings)
        self.settings_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.label = ttk.Label(root, text="密钥长度 (最多1152位):", font=("Helvetica", 14))
        self.label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.length_entry = ttk.Entry(root, font=("Helvetica", 14))
        self.length_entry.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        
        button_frame = ttk.Frame(root)
        button_frame.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        
        self.generate_button = ttk.Button(button_frame, text="生成密钥", command=self.start_key_generation)
        self.generate_button.grid(row=0, column=0, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="停止", command=self.stop_generation)
        self.stop_button.grid(row=0, column=1, padx=5)
        
        self.reset_button = ttk.Button(button_frame, text="初始化", command=self.reset)
        self.reset_button.grid(row=0, column=2, padx=5)
        
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.progress.grid_remove()
        
        self.key_var = tk.StringVar()
        self.key_label = ttk.Label(root, textvariable=self.key_var, font=("Helvetica", 14), wraplength=400)
        self.key_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        
        self.save_button = ttk.Button(root, text="保存密钥", command=self.save_key)
        self.save_button.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        
        self.generated_key = ""
        self.total_time = 10
        self.log_dir = "logs"
        self.stop_event = threading.Event()

    def show_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("设置")
        
        self.time_label = ttk.Label(settings_window, text="生成时间 (秒):", font=("Helvetica", 14))
        self.time_label.pack(pady=10)
        
        self.time_entry = ttk.Entry(settings_window, font=("Helvetica", 14))
        self.time_entry.pack(pady=10)
        self.time_entry.insert(0, str(self.total_time))
        
        self.log_dir_label = ttk.Label(settings_window, text="日志文件夹:", font=("Helvetica", 14))
        self.log_dir_label.pack(pady=10)
        
        self.log_dir_entry = ttk.Entry(settings_window, font=("Helvetica", 14))
        self.log_dir_entry.pack(pady=10)
        self.log_dir_entry.insert(0, self.log_dir)
        
        save_button = ttk.Button(settings_window, text="保存", command=lambda: self.save_settings(settings_window))
        save_button.pack(pady=10)

    def save_settings(self, window):
        try:
            self.total_time = int(self.time_entry.get())
            if self.total_time <= 0:
                raise ValueError("时间必须大于0")
            self.log_dir = self.log_dir_entry.get()
            if not os.path.exists(self.log_dir):
                os.makedirs(self.log_dir)
            window.destroy()
        except ValueError as e:
            self.key_var.set(f"输入无效: {e}")

    def start_key_generation(self):
        self.stop_event.clear()
        threading.Thread(target=self.generate_key).start()

    def generate_key(self):
        try:
            length = int(self.length_entry.get())
            if length <= 0 or length > 1152:
                raise ValueError("长度必须在1到1152之间")
            
            self.generated_key = ''
            self.progress["maximum"] = length
            interval = self.total_time / length
            self.progress.grid()
            
            for i in range(length):
                if self.stop_event.is_set():
                    break
                self.generated_key += random.choice(string.digits)
                self.key_var.set(self.format_key(self.generated_key))
                self.progress["value"] = i + 1
                self.root.update_idletasks()
                time.sleep(interval)
        except ValueError as e:
            self.key_var.set(f"输入无效: {e}")

    def stop_generation(self):
        self.stop_event.set()

    def reset(self):
        self.generated_key = ""
        self.key_var.set("")
        self.progress["value"] = 0
        self.progress.grid_remove()
        self.length_entry.delete(0, tk.END)
        self.stop_event.clear()

    def format_key(self, key: str) -> str:
        return ' '.join(key[i:i+4] for i in range(0, len(key), 4))

    def save_key(self):
        if self.generated_key:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if file_path:
                with open(file_path, "w") as file:
                    file.write(self.generated_key)
                self.key_var.set(f"密钥已保存到 {file_path}")
                self.save_log(file_path)
            else:
                self.key_var.set("保存已取消")
        else:
            self.key_var.set("请先生成一个密钥")

    def save_log(self, file_path: str):
        log_file = os.path.join(self.log_dir, "key_generator_log.txt")
        with open(log_file, "a") as log:
            log.write(f"密钥已保存到: {file_path}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyGeneratorApp(root)
    root.mainloop()