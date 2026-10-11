import tkinter as tk
from tkinter import messagebox, ttk
import keyboard
import threading
import time

class KeyboardClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Keyboard Clicker - Windows PC")
        self.root.geometry("600x700")
        self.root.resizable(True, True)
        self.root.configure(bg="#f0f0f0")
        
        self.is_clicking = False
        self.click_thread = None
        self.total_clicks = 0
        self.key_sequence = []
        
        self.setup_ui()
        self.setup_keyboard_shortcuts()
        
    def setup_ui(self):
        # Buat canvas + scrollbar
        canvas_frame = tk.Frame(self.root, bg="#f0f0f0")
        canvas_frame.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(canvas_frame, bg="#f0f0f0", highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Header
        header_frame = tk.Frame(scrollable_frame, bg="#2196F3", height=60)
        header_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        title = tk.Label(
            header_frame,
            text="⌨️ KEYBOARD CLICKER",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#2196F3"
        )
        title.pack(pady=15)
        
        main_frame = tk.Frame(scrollable_frame, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
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
        
        #===== SINGLE MODE =====
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
        
        keys = [
            "Space", "Enter", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
            "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
            "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
            "Tab", "Backspace", "Shift", "Ctrl", "Alt"
        ]
        
        key_combo = ttk.Combobox(
            self.single_mode_frame,
            textvariable=self.key_var,
            values=keys,
            state="readonly",
            font=("Arial", 10),
            width=30
        )
        key_combo.pack(fill="x", pady=5)
        
        #===== SEQUENCE MODE =====
        self.sequence_mode_frame = tk.LabelFrame(
            main_frame,
            text="Mode: Sequence (2-5 Tombol)",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        
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
        
        # ===== JUMLAH ULANGAN =====
        count_frame = tk.LabelFrame(
            main_frame,
            text="Jumlah Pengulangan",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        count_frame.pack(fill="x", pady=10)
        
        tk.Label(count_frame, text="Isi 0 atau kosong untuk tidak terbatas:", font=("Arial", 10), bg="#f0f0f0").pack(anchor="w")
        self.entry_count = tk.Entry(count_frame, font=("Arial", 11), width=30)
        self.entry_count.insert(0, "10")
        self.entry_count.pack(fill="x", pady=5)
        
        self.infinite_var = tk.BooleanVar(value=False)
        self.check_infinite = tk.Checkbutton(
            count_frame,
            text="Tidak terbatas (loop terus sampai STOP)",
            variable=self.infinite_var,
            bg="#f0f0f0",
            font=("Arial", 10)
        )
        self.check_infinite.pack(anchor="w", pady=5)
        
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
            text="F6 = Mulai Klik (langsung berjalan)\nF7 = Stop Klik\nESC = Exit Aplikasi\n\nSingle Mode: Tekan 1 tombol berkali-kali\nSequence Mode: Tekan 2-5 tombol berurutan\n\n✔ Tidak terbatas: isi 0 atau centang checkbox\n⚠️ Jangan gunakan untuk cheating game!",
            font=("Arial", 9),
            bg="#fff3cd",
            justify="left"
        )
        info_text.pack(anchor="w")
        
    def update_ui_mode(self):
        if self.mode_var.get() == "single":
            self.single_mode_frame.pack(fill="x", pady=10)
            self.sequence_mode_frame.pack_forget()
        else:
            self.single_mode_frame.pack_forget()
            self.sequence_mode_frame.pack(fill="x", pady=10)
        
    def setup_keyboard_shortcuts(self):
        keyboard.add_hotkey('f6', self.start_clicking)
        keyboard.add_hotkey('f7', self.stop_clicking)
        keyboard.add_hotkey('esc', self.exit_app)
        
    def get_values(self):
        try:
            raw_count = self.entry_count.get().strip()
            count = int(raw_count) if raw_count != "" else 0
            
            delay = int(self.entry_delay.get())
            hold = int(self.entry_hold.get())
            
            if count < 0:
                raise ValueError("Jumlah pengulangan tidak boleh negatif!")
            if delay < 0 or hold < 0:
                raise ValueError("Nilai jeda/tahan tidak boleh negatif!")
            
            return count, delay, hold
        except ValueError as e:
            messagebox.showerror("Error", f"Input tidak valid!\n{str(e)}")
            return None
        
    def get_sequence(self):
        sequence = []
        keys = [self.seq_key1, self.seq_key2, self.seq_key3, self.seq_key4, self.seq_key5]
        
        for combo in keys:
            value = combo.get().strip().lower()
            if value == "tidak" or value == "":
                continue
            sequence.append(value)
        
        if len(sequence) < 2:
            messagebox.showerror("Error", "Sequence mode harus berisi minimal 2 tombol.")
            return []
        
        if len(sequence) > 5:
            messagebox.showerror("Error", "Sequence mode maksimal 5 tombol.")
            return []
        
        return sequence
        
    def start_clicking(self):
        if self.is_clicking:
            messagebox.showwarning("Warning", "Keyboard clicking sudah sedang berjalan!")
            return
        
        values = self.get_values()
        if values is None:
            return
        
        count, delay, hold = values
        infinite = self.infinite_var.get() or count == 0
        
        mode = self.mode_var.get()
        if mode == "single":
            key = self.key_var.get().lower()
            key_list = [key]
        else:
            key_list = self.get_sequence()
            if not key_list:
                return
        
        self.is_clicking = True
        self.total_clicks = 0
        self.btn_start.config(state="disabled")
        self.btn_stop.config(state="normal")
        
        # Start clicking thread langsung tanpa countdown
        self.click_thread = threading.Thread(
            target=self.click_loop,
            args=(key_list, count, delay, hold, infinite),
            daemon=True
        )
        self.click_thread.start()
        
    def click_loop(self, key_list, count, delay, hold, infinite):
        # Langsung mulai tanpa countdown
        while self.is_clicking:
            # loop terbatas
            if not infinite:
                if count <= 0:
                    break
                
            # proses satu siklus
            for key in key_list:
                if not self.is_clicking:
                    break
                
                try:
                    keyboard.press(key)
                    time.sleep(hold / 1000)
                    keyboard.release(key)
                    self.total_clicks += 1
                except Exception as e:
                    print(f"Error: {e}")
                
                time.sleep(delay / 1000)
            
            # jika mode terbatas, kurangi hitung ulang
            if not infinite:
                count -= 1
                if count <= 0:
                    break
        
        self.stop_clicking()
        
    def stop_clicking(self):
        self.is_clicking = False
        self.btn_start.config(state="normal")
        self.btn_stop.config(state="disabled")
        
    def exit_app(self):
        self.is_clicking = False
        if messagebox.askokcancel("Exit", "Yakin ingin keluar?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyboardClicker(root)
    root.mainloop()
