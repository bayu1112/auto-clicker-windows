import tkinter as tk
from tkinter import messagebox, ttk
import keyboard
import threading
import time
from datetime import datetime

class KeyboardClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Keyboard Clicker - Windows PC")
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
        # Variables
        self.is_clicking = False
        self.click_thread = None
        self.total_clicks = 0
        
        # Setup UI
        self.setup_ui()
        self.setup_keyboard_shortcuts()
        
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#2196F3", height=60)
        header_frame.pack(fill="x")
        
        title = tk.Label(
            header_frame,
            text="⌨️ KEYBOARD CLICKER",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#2196F3"
        )
        title.pack(pady=15)
        
        # Main Frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # ===== KEY TO PRESS =====
        key_frame = tk.LabelFrame(
            main_frame,
            text="Tombol yang Akan Ditekan",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        key_frame.pack(fill="x", pady=10)
        
        tk.Label(key_frame, text="Pilih Tombol:", font=("Arial", 10), bg="#f0f0f0").pack(anchor="w")
        
        self.key_var = tk.StringVar(value="space")
        
        keys = [
            ("Space", "space"),
            ("Enter", "enter"),
            ("A", "a"),
            ("B", "b"),
            ("C", "c"),
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("Left Click", "left_click"),
            ("Right Click", "right_click"),
        ]
        
        key_combo = ttk.Combobox(
            key_frame,
            textvariable=self.key_var,
            values=[k[0] for k in keys],
            state="readonly",
            font=("Arial", 10),
            width=30
        )
        key_combo.pack(fill="x", pady=5)
        
        self.key_map = {k[0]: k[1] for k in keys}
        
        # ===== CLICK COUNT =====
        count_frame = tk.LabelFrame(
            main_frame,
            text="Jumlah Klik",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        count_frame.pack(fill="x", pady=10)
        
        tk.Label(count_frame, text="Berapa kali menekan tombol?", font=("Arial", 10), bg="#f0f0f0").pack(anchor="w")
        
        self.entry_count = tk.Entry(count_frame, font=("Arial", 11), width=30)
        self.entry_count.insert(0, "10")
        self.entry_count.pack(fill="x", pady=5)
        
        # ===== DELAY SETTINGS =====
        delay_frame = tk.LabelFrame(
            main_frame,
            text="Pengaturan Jeda",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        delay_frame.pack(fill="x", pady=10)
        
        tk.Label(delay_frame, text="Jeda antar tombol (ms):", font=("Arial", 10), bg="#f0f0f0").pack(anchor="w")
        
        self.entry_delay = tk.Entry(delay_frame, font=("Arial", 11), width=30)
        self.entry_delay.insert(0, "100")
        self.entry_delay.pack(fill="x", pady=5)
        
        # ===== HOLD TIME (untuk tombol yang dihold) =====
        hold_frame = tk.LabelFrame(
            main_frame,
            text="Durasi Tahan Tombol",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        hold_frame.pack(fill="x", pady=10)
        
        tk.Label(hold_frame, text="Berapa lama tombol ditekan? (ms):", font=("Arial", 10), bg="#f0f0f0").pack(anchor="w")
        
        self.entry_hold = tk.Entry(hold_frame, font=("Arial", 11), width=30)
        self.entry_hold.insert(0, "50")
        self.entry_hold.pack(fill="x", pady=5)
        
        # ===== STATUS =====
        status_frame = tk.LabelFrame(
            main_frame,
            text="Status",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        status_frame.pack(fill="x", pady=10)
        
        self.status_label = tk.Label(
            status_frame,
            text="Status: SIAP",
            font=("Arial", 10),
            fg="#4CAF50",
            bg="#f0f0f0"
        )
        self.status_label.pack(anchor="w")
        
        self.counter_label = tk.Label(
            status_frame,
            text="Total Klik: 0",
            font=("Arial", 10),
            fg="#2196F3",
            bg="#f0f0f0"
        )
        self.counter_label.pack(anchor="w")
        
        # ===== BUTTONS =====
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(fill="x", pady=15)
        
        self.btn_start = tk.Button(
            button_frame,
            text="▶ MULAI (F6)",
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.start_clicking,
            height=2,
            cursor="hand2"
        )
        self.btn_start.pack(side="left", padx=5, fill="both", expand=True)
        
        self.btn_stop = tk.Button(
            button_frame,
            text="⏹ STOP (F7)",
            bg="#f44336",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.stop_clicking,
            height=2,
            state="disabled",
            cursor="hand2"
        )
        self.btn_stop.pack(side="left", padx=5, fill="both", expand=True)
        
        # ===== INFO BOX =====
        info_frame = tk.LabelFrame(
            main_frame,
            text="Shortcut Keyboard",
            font=("Arial", 10, "bold"),
            bg="#fff3cd",
            padx=10,
            pady=10
        )
        info_frame.pack(fill="x", pady=10)
        
        info_text = tk.Label(
            info_frame,
            text="F6 = Mulai Klik\nF7 = Stop Klik\nESC = Exit Aplikasi",
            font=("Arial", 9),
            bg="#fff3cd",
            justify="left"
        )
        info_text.pack(anchor="w")
        
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts"""
        keyboard.add_hotkey('f6', self.start_clicking)
        keyboard.add_hotkey('f7', self.stop_clicking)
        keyboard.add_hotkey('esc', self.exit_app)
        
    def get_values(self):
        """Get dan validate input values"""
        try:
            count = int(self.entry_count.get())
            delay = int(self.entry_delay.get())
            hold = int(self.entry_hold.get())
            
            if count <= 0 or delay < 0 or hold < 0:
                raise ValueError("Nilai harus positif!")
                
            return count, delay, hold
        except ValueError as e:
            messagebox.showerror("Error", f"Input tidak valid!\n{str(e)}\nGunakan angka saja.")
            return None
            
    def start_clicking(self):
        """Mulai keyboard clicking"""
        if self.is_clicking:
            messagebox.showwarning("Warning", "Keyboard clicking sudah sedang berjalan!")
            return
            
        values = self.get_values()
        if values is None:
            return
            
        count, delay, hold = values
        key = self.key_map[self.key_var.get()]
        
        self.is_clicking = True
        self.total_clicks = 0
        self.btn_start.config(state="disabled")
        self.btn_stop.config(state="normal")
        self.status_label.config(text="Status: BERJALAN ▶", fg="#f44336")
        
        # Countdown sebelum mulai
        countdown = tk.Toplevel(self.root)
        countdown.title("Countdown")
        countdown.geometry("300x100")
        countdown.resizable(False, False)
        
        countdown_label = tk.Label(
            countdown,
            text="Keyboard clicking akan dimulai dalam 3 detik...",
            font=("Arial", 12),
            wraplength=280
        )
        countdown_label.pack(pady=30)
        
        countdown.update()
        for i in range(3, 0, -1):
            countdown_label.config(text=f"Dimulai dalam {i} detik...")
            countdown.update()
            time.sleep(1)
            
        countdown.destroy()
        
        # Start clicking thread
        self.click_thread = threading.Thread(
            target=self.click_loop,
            args=(key, count, delay, hold),
            daemon=True
        )
        self.click_thread.start()
        
    def click_loop(self, key, count, delay, hold):
        """Loop untuk melakukan klik berulang"""
        for i in range(count):
            if not self.is_clicking:
                break
                
            try:
                if key == "left_click":
                    # Gunakan library pyautogui untuk mouse click
                    try:
                        import pyautogui
                        pyautogui.click()
                    except ImportError:
                        keyboard.press_and_release('space')  # Fallback ke space
                elif key == "right_click":
                    try:
                        import pyautogui
                        pyautogui.rightClick()
                    except ImportError:
                        keyboard.press_and_release('space')
                else:
                    # Tekan dan lepas tombol
                    keyboard.press(key)
                    time.sleep(hold / 1000)  # Convert ms to seconds
                    keyboard.release(key)
                
                self.total_clicks += 1
                self.update_counter()
                
            except Exception as e:
                print(f"Error: {e}")
                
            time.sleep(delay / 1000)  # Convert ms to seconds
            
        self.stop_clicking()
        messagebox.showinfo("Selesai", f"Keyboard clicking selesai!\nTotal klik: {self.total_clicks}")
        
    def update_counter(self):
        """Update counter di UI"""
        self.counter_label.config(text=f"Total Klik: {self.total_clicks}")
        self.root.update_idletasks()
        
    def stop_clicking(self):
        """Hentikan keyboard clicking"""
        self.is_clicking = False
        self.btn_start.config(state="normal")
        self.btn_stop.config(state="disabled")
        self.status_label.config(text="Status: SIAP", fg="#4CAF50")
        
    def exit_app(self):
        """Tutup aplikasi"""
        self.is_clicking = False
        if messagebox.askokcancel("Exit", "Yakin ingin keluar?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyboardClicker(root)
    root.mainloop()
