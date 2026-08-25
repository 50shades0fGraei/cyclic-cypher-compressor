#!/usr/bin/env python3
# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.

import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, simpledialog

try:
    import licensing_engine
except ImportError:
    licensing_engine = None

# Fallback safely if run directly without Double Crunch logic installed
try:
    import double_crunch_marketplace as lujan_core
except ImportError:
    lujan_core = None

APP_TYPE = "UNIVERSAL" # Can be UNIVERSAL, MEDIA, or DOCUMENT

# --- UI CONSTANTS ---
BG_COLOR = "#05050A"
FG_COLOR = "#FFFFFF"
ACCENT_COLOR = "#00f2ff"
TERMINAL_BG = "#0a0e17"
FONT_PRIMARY = ("Segoe UI", 12, "bold")
FONT_TITLE = ("Segoe UI", 24, "bold")
FONT_MONO = ("Consolas", 10)

class PrintRedirector:
    """Redirects stdout to the Tkinter Text widget"""
    def __init__(self, text_widget):
        self.text_widget = text_widget
        
    def write(self, str_data):
        self.text_widget.configure(state='normal')
        self.text_widget.insert(tk.END, str_data)
        self.text_widget.see(tk.END)
        self.text_widget.configure(state='disabled')
        
    def flush(self):
        pass

class SovereignVaultApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        if APP_TYPE == "MEDIA":
            self.title("Sovereign Media Vault")
        elif APP_TYPE == "DOCUMENT":
            self.title("Sovereign Document Vault")
        else:
            self.title("Sovereign Double Crunch Vault")
            
        self.geometry("800x600")
        self.configure(bg=BG_COLOR)
        
        # Center the window
        self.eval('tk::PlaceWindow . center')
        
        self.setup_ui()
        
        # Override printing
        sys.stdout = PrintRedirector(self.terminal)
        
        print("=" * 80)
        print("LUJAN DEDUCTIVE VAULT: SECURE DESKTOP ENVIRONMENT INITIATED")
        print("True Cypher Gap Sum Engine Online. Awaiting targets...")
        print("=" * 80)
        print()
        
        if lujan_core is None:
            print("[WARNING] core files missing! Ensure cyberdna_engine.py is present.")
            
        
        if not self.check_license():
            self.destroy()
            return
            
    def check_license(self):
        if licensing_engine is None:
            print("[WARNING] licensing module missing.")
            return True
            
        if licensing_engine.verify_license():
            self.terminal.configure(state='normal')
            self.terminal.insert(tk.END, "DEVICE LICENSE VERIFIED. Welcome Sovereign.\n\n")
            self.terminal.configure(state='disabled')
            return True
            
        # Prompt for key
        messagebox.showinfo("Lujan Licensing", "This application requires a 1-Device Purchase Key.\nPlease enter it to unlock.")
        purchase_key = simpledialog.askstring("Activation", "Enter your $80 Sovereign Purchase Key:")
        
        if purchase_key and len(purchase_key) > 5:
            licensing_engine.activate_license(purchase_key)
            messagebox.showinfo("Success", "Device Licensed successfully. Engine Unlocked.")
            self.terminal.configure(state='normal')
            self.terminal.insert(tk.END, "DEVICE LICENSE ACTIVATED.\n\n")
            self.terminal.configure(state='disabled')
            return True
        else:
            messagebox.showerror("Error", "Invalid Purchase Key. The application will close.")
            return False

    def setup_ui(self):
        # Header
        title_text = "LUJAN DOUBLE CRUNCH VAULT"
        if APP_TYPE == "MEDIA":
            title_text = "LUJAN MEDIA VAULT"
        elif APP_TYPE == "DOCUMENT":
            title_text = "LUJAN DOCUMENT VAULT"
            
        header = tk.Label(self, text=title_text, bg=BG_COLOR, fg=ACCENT_COLOR, font=FONT_TITLE)
        header.pack(pady=(30, 20))
        
        # Button Frame
        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(fill=tk.X, padx=50, pady=10)
        
        # Compress Button
        self.btn_compress = tk.Button(btn_frame, text="TARGET: DOUBLE CRUNCH", 
                                      bg=ACCENT_COLOR, fg="black", font=FONT_PRIMARY, 
                                      activebackground="white", activeforeground="black",
                                      relief=tk.FLAT, borderwidth=0, padx=20, pady=15,
                                      command=self.handle_compress)
        self.btn_compress.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        
        # Restore Button
        self.btn_restore = tk.Button(btn_frame, text="TARGET: RESTORE", 
                                     bg="#333344", fg="white", font=FONT_PRIMARY, 
                                     activebackground="white", activeforeground="black",
                                     relief=tk.FLAT, borderwidth=0, padx=20, pady=15,
                                     command=self.handle_restore)
        self.btn_restore.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(10, 0))
        
        # Terminal Label
        lbl_term = tk.Label(self, text="SYSTEM INTELLIGENCE", bg=BG_COLOR, fg="#8892b0", font=("Segoe UI", 10))
        lbl_term.pack(anchor="w", padx=50, pady=(30, 5))
        
        # Terminal Output
        self.terminal = scrolledtext.ScrolledText(self, bg=TERMINAL_BG, fg=ACCENT_COLOR, 
                                                  font=FONT_MONO, borderwidth=1, relief=tk.SOLID)
        self.terminal.pack(fill=tk.BOTH, expand=True, padx=50, pady=(0, 30))
        self.terminal.configure(state='disabled')
        
    def run_thread(self, target_func, *args):
        # Disable buttons during operation
        self.btn_compress.config(state=tk.DISABLED)
        self.btn_restore.config(state=tk.DISABLED)
        
        def wrapper():
            try:
                target_func(*args)
            except Exception as e:
                print(f"[FATAL EXCEPTION] {e}")
            finally:
                self.btn_compress.config(state=tk.NORMAL)
                self.btn_restore.config(state=tk.NORMAL)
                
        threading.Thread(target=wrapper, daemon=True).start()

    def handle_compress(self):
        if lujan_core is None:
            print("ERROR: Engine core not loaded.")
            return

        filetypes = [("All Files", "*.*")]
        if APP_TYPE == "MEDIA":
            filetypes = [("Media Files", "*.mp4 *.avi *.mkv *.jpg *.png *.jpeg")]
        elif APP_TYPE == "DOCUMENT":
            filetypes = [("Document Files", "*.pdf *.docx *.txt *.xlsx *.csv")]
            
        target_file = filedialog.askopenfilename(title="Select File to Crunch", filetypes=filetypes)
        if not target_file: return
        
        output_file = target_file + ".cdv6"
        self.run_thread(lujan_core.double_crunch_compress, target_file, output_file)

    def handle_restore(self):
        if lujan_core is None:
            print("ERROR: Engine core not loaded.")
            return

        target_file = filedialog.askopenfilename(title="Select .cdv6 Artifact to Restore", filetypes=[("Lujan Vault Files", "*.cdv6"), ("All Files", "*.*")])
        if not target_file: return
        
        # Remove .cdv6 or just append .restored
        if target_file.endswith(".cdv6"):
            output_file = target_file[:-5]
        else:
            output_file = target_file + ".restored"
            
        self.run_thread(lujan_core.iterative_decompress, target_file, output_file)

if __name__ == "__main__":
    app = SovereignVaultApp()
    app.mainloop()
