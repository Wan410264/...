import tkinter as tk
from tkinter import ttk
import winsound

class CountdownTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("倒计时")
        
        self.time_var = tk.StringVar()
        self.time_var.set("00:00:00.00")
        
        self.label = ttk.Label(root, textvariable=self.time_var, font=("Helvetica", 48))
        self.label.pack(pady=20)
        
        self.entry = ttk.Entry(root, font=("Helvetica", 24))
        self.entry.pack(pady=20)
        
        button_frame = ttk.Frame(root)
        button_frame.pack(pady=20)
        
        self.start_button = ttk.Button(button_frame, text="开始", command=self.start_countdown)
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.pause_button = ttk.Button(button_frame, text="暂停", command=self.pause_countdown)
        self.pause_button.grid(row=0, column=1, padx=5)
        
        self.resume_button = ttk.Button(button_frame, text="继续", command=self.resume_countdown)
        self.resume_button.grid(row=0, column=2, padx=5)
        
        self.reset_button = ttk.Button(button_frame, text="还原", command=self.reset_countdown)
        self.reset_button.grid(row=0, column=3, padx=5)
        
        self.time_left = 0
        self.paused = False

        # 添加血条
        self.canvas = tk.Canvas(root, width=300, height=30, bg='white', highlightthickness=1, highlightbackground="black")
        self.canvas.pack(pady=20)
        self.health_bar = self.canvas.create_rectangle(0, 0, 300, 30, fill='green')
        self.health_text = self.canvas.create_text(150, 15, text="100%", fill="black", font=("Helvetica", 12))
        self.max_health = 100
        self.current_health = self.max_health

    def start_countdown(self):
        try:
            self.time_left = int(float(self.entry.get()) * 1000)  # 将输入的秒数转换为毫秒
            self.max_health = self.time_left  # 将最大健康值设置为倒计时时间
            self.current_health = self.max_health
            self.paused = False
            self.update_timer()
        except ValueError:
            self.time_var.set("输入无效")

    def pause_countdown(self):
        self.paused = True

    def resume_countdown(self):
        if self.paused:
            self.paused = False
            self.update_timer()

    def reset_countdown(self):
        self.time_left = 0
        self.paused = False
        self.time_var.set("00:00:00.00")
        self.canvas.coords(self.health_bar, 0, 0, 300, 30)
        self.canvas.itemconfig(self.health_bar, fill='green')
        self.canvas.itemconfig(self.health_text, text="100%")

    def update_timer(self):
        if self.time_left > 0 and not self.paused:
            millis = (self.time_left % 1000) // 10
            seconds = (self.time_left // 1000) % 60
            minutes = (self.time_left // (1000 * 60)) % 60
            hours = (self.time_left // (1000 * 60 * 60)) % 24
            self.time_var.set(f"{hours:02d}:{minutes:02d}:{seconds:02d}.{millis:02d}")
            self.time_left -= 10
            self.update_health_bar()
            self.root.after(10, self.update_timer)
        elif self.time_left <= 0:
            self.time_var.set("时间到！")
            winsound.Beep(1000, 1000)  # 播放声音

    def update_health_bar(self):
        health_ratio = self.time_left / self.max_health
        self.canvas.coords(self.health_bar, 0, 0, 300 * health_ratio, 30)
        self.canvas.itemconfig(self.health_text, text=f"{int(health_ratio * 100)}%")
        color = self.get_gradient_color(health_ratio)
        self.canvas.itemconfig(self.health_bar, fill=color)

    def get_gradient_color(self, ratio):
        # 渐变色从红色到绿色
        red = int(255 * (1 - ratio))
        green = int(255 * ratio)
        return f'#{red:02x}{green:02x}00'

if __name__ == "__main__":
    root = tk.Tk()
    timer = CountdownTimer(root)
    root.mainloop()