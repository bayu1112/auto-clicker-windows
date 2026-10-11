import tkinter as tk
from tkinter import messagebox, ttk
import keyboard
import threading
import time

class KeyboardClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Keyboard Clicker - Windows PC")
        self.root.geometry("600x900")
        self.root.resizable(True, True)
        self.root.configure(bg="#f0f0f0")
        
        self.is_clicking = False
        self.click_thread = None
        self.total_clicks = 0
        
        # List untuk menyimpan sequence tombol
        self.key_sequence = []
        
        self.setup_ui()
        self.setup_keyboard_shortcuts()
        
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#2196F3", height=60)
        header_frame.pack(fill="x")
        
        title = tk.Label(
            header_frame,
            text="⌨️ KEYBOARD CLICKER - SEQUENCE MODE",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#2196F3"
        )
        title.pack(pady=15)
        
        # Main Frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # ===== MODE SELECTION =====
        mode_frame = tk.LabelFrame(
            main_frame,
            text="Pilih Mode",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        mode_frame.pack(fill="x", pady=10)
        
        self.mode_var = tk.StringVar(value="single")
        
        single_radio = tk.Radiobutton(
            mode_frame,
            text="Single Click (1 Tombol)",
            variable=self.mode_var,
            value="single",
            font=("Arial", 10),
            bg="#f0f0f0",
            command=self.update_ui_mode
        )
        single_radio.pack(anchor="w")
        
        sequence_radio = tk.Radiobutton(
            mode_frame,
            text="Sequence Mode (2-5 Tombol Berurutan)",
            variable=self.mode_var,
            value="sequence",
            font=("Arial", 10),
            bg="#f0f0f0",
            command=self.update_ui_mode
        )
        sequence_radio.pack(anchor="w")
        
        # ===== SINGLE MODE FRAME =====
        self.single_mode_frame = tk.LabelFrame(
            main_frame,
            text="Mode: Single Click",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        self.single_mode_frame.pack(fill="x", pady=10)
        
        tk.Label(self.single_mode_frame, text="Pilih Tombol:", font=("Arial", 10), bg="#f0f0f0").pack(anchor="w")
        
        self.key_var = tk.StringVar(value="Space")
        
        keys = ["Space", "Enter", "A", "B", "C", "D", "1", "2", "3", "Tab", "Backspace"]
        
        key_combo = ttk.Combobox(
            self.single_mode_frame,
            textvariable=self.key_var,
            values=keys,
            state="readonly",
            font=("Arial", 10),
            width=30
        )
        key_combo.pack(fill="x", pady=5)
        
        # ===== SEQUENCE MODE FRAME =====
        self.sequence_mode_frame = tk.LabelFrame(
            main_frame,
            text="Mode: Sequence (2-5 Tombol)",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        self.sequence_mode_frame.pack(fill="x", pady=10)
        
        # Tombol 1
        tk.Label(self.sequence_mode_frame, text="Tombol 1:", font=("Arial", 10), bg="#f0f0f0").pack(anchor="w")
        self.seq_key1 = ttk.Combobox(
            self.sequence_mode_frame,
            values=keys,
            state="readonly",
            font=("Arial", 10),
            width=30
        )
        self.seq_key1.set("A")
        self.seq_key1.pack(fill="x", pady=5)
        
        # Tombol 2
        tk.Label(self.sequence_mode_frame, text="Tombol 2:", font=("Arial", 10), bg="#f0f0f0").pack(anchor="w")
        self.seq_key2 = ttk.Combobox(
            self.sequence_mode_frame,
            values=keys,
            state="readonly",
            font=("Arial", 10),
            width=30
        )
        self.seq_key2.set("B")
        self.seq_key2.pack(fill="x", pady=5)
        
        # Tombol 3
        tk.Label(self.sequence_mode_frame, text="Tombol 3 (Opsional):", font=("Arial", 10), bg="#f0f0f0").pack(anchor="w")
        self.seq_key3 = ttk.Combobox(
            self.sequence_mode_frame,
            values=["Tidak"] + keys,
            state="readonly",
            font=("Arial", 10),
            width=30
        )
        self.seq_key3.set("Tidak")
        self.seq_key3.pack(fill="x", pady=5)
        
        # Tombol 4
        tk.Label(self.sequence_mode_frame, text="Tombol 4 (Opsional):", font=("Arial", 10), bg="#f0f0f0").pack(anchor="w")
        self.seq_key4 = ttk.Combobox(
            self.sequence_mode_frame,
            values=["Tidak"] + keys,
            state="readonly",
            font=("Arial", 10),
            width=30
        )
        self.seq_key4.set("Tidak")
        self.seq_key4.pack(fill="x", pady=5)
        
        # Tombol 5
        tk.Label(self.sequence_mode_frame, text="Tombol 5 (Opsional):", font=("Arial", 10), bg="#f0f0f0").pack(anchor="w")
        self.seq_key5 = ttk.Combobox(
            self.sequence_mode_frame,
            values=["Tidak"] + keys,
            state="readonly",
            font=("Arial", 10),
            width=30
        )
        self.seq_key5.set("Tidak")
        self.seq_key5.pack(fill="x", pady=5)
        
        # ===== JEDA ANTAR TOMBOL =====
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
        
        # ===== HOLD TIME =====
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
        
        # ===== JUMLAH ULANGAN (UNTUK SINGLE MODE) =====
        count_frame = tk.LabelFrame(
            main_frame,
            text="Jumlah Pengulangan",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        count_frame.pack(fill="x", pady=10)
        
        tk.Label(count_frame, text="Berapa kali sequence diulangi?", font=("Arial", 10), bg="#f0f0f0").pack(anchor="w")
        
        self.entry_count = tk.Entry(count_frame, font=("Arial", 11), width=30)
        self.entry_count.insert(0, "10")
        self.entry_count.pack(fill="x", pady=5)
        
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
        
        # ===== INFO =====
        info_frame = tk.LabelFrame(
            main_frame,
            text="Shortcut Keyboard & Info",
            font=("Arial", 10, "bold"),
            bg="#fff3cd",
            padx=10,
            pady=10
        )
        info_frame.pack(fill="x", pady=10)
        
        info_text = tk.Label(
            info_frame,
            text="F6 = Mulai Klik\nF7 = Stop Klik\nESC = Exit Aplikasi\n\nSingle Mode: Tekan 1 tombol berkali-kali\nSequence Mode: Tekan 2-5 tombol berurutan\n\n⚠️ Jangan gunakan untuk cheating game!",
            font=("Arial", 9),
            bg="#fff3cd",
            justify="left"
        )
        info_text.pack(anchor="w")
        
    def update_ui_mode(self):
        """Update UI berdasarkan mode yang dipilih"""
        if self.mode_var.get() == "single":
            self.single_mode_frame.pack(fill="x", pady=10)
            self.sequence_mode_frame.pack_forget()
        else:
            self.single_mode_frame.pack_forget()
            self.sequence_mode_frame.pack(fill="x", pady=10)
        
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
            
            if count <= 0:
                raise ValueError("Jumlah pengulangan harus lebih dari 0!")
            if delay < 0 or hold < 0:
                raise ValueError("Nilai tidak boleh negatif!")
                
            return count, delay, hold
        except ValueError as e:
            messagebox.showerror("Error", f"Input tidak valid!\n{str(e)}")
            return None
            
    def get_sequence(self):
        """Get sequence dari input tombol"""
        sequence = []
        
        key1 = self.seq_key1.get().lower()
        key2 = self.seq_key2.get().lower()
        key3 = self.seq_key3.get().lower()
        key4 = self.seq_key4.get().lower()
        key5 = self.seq_key5.get().lower()
        
        sequence.append(key1)
        sequence.append(key2)
        
        if key3 != "tidak":
            sequence.append(key3)
        if key4 != "tidak":
            sequence.append(key4)
        if key5 != "tidak":
            sequence.append(key5)
        
        return sequence
            
    def start_clicking(self):
        """Mulai keyboard clicking"""
        if self.is_clicking:
            messagebox.showwarning("Warning", "Keyboard clicking sudah sedang berjalan!")
            return
            
        values = self.get_values()
        if values is None:
            return
            
        count, delay, hold = values
        mode = self.mode_var.get()
        
        if mode == "single":
            key = self.key_var.get().lower()
            key_list = [key]
        else:
            key_list = self.get_sequence()
        
        self.is_clicking = True
        self.total_clicks = 0
        self.btn_start.config(state="disabled")
        self.btn_stop.config(state="normal")
        self.status_label.config(text="Status: BERJALAN ▶", fg="#f44336")
        
        # Show mode info
        if mode == "single":
            messagebox.showinfo("Info", f"Mode: SINGLE CLICK\nTombol: {self.key_var.get()}\nJumlah: {count}x\n\nKlicking akan dimulai dalam 3 detik.")
        else:
            sequence_str = " → ".join([k.upper() for k in key_list])
            messagebox.showinfo("Info", f"Mode: SEQUENCE\nSequence: {sequence_str}\nUlangan: {count}x\n\nClicking akan dimulai dalam 3 detik.")
        
        # Start clicking thread
        self.click_thread = threading.Thread(
            target=self.click_loop,
            args=(key_list, count, delay, hold),
            daemon=True
        )
        self.click_thread.start()
        
    def click_loop(self, key_list, count, delay, hold):
        """Loop untuk melakukan klik berulang"""
        time.sleep(3)  # Countdown 3 detik
        
        for i in range(count):
            if not self.is_clicking:
                break
            
            # Tekan setiap tombol dalam sequence
            for key in key_list:
                if not self.is_clicking:
                    break
                    
                try:
                    # Tekan tombol
                    keyboard.press(key)
                    time.sleep(hold / 1000)  # Convert ms to seconds
                    keyboard.release(key)
                    
                    self.total_clicks += 1
                    self.update_counter()
                    
                except Exception as e:
                    print(f"Error: {e}")
                
                # Jeda antar tombol dalam sequence
                time.sleep(delay / 1000)
            
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
