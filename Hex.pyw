# This Gui Was CodedBy Hex#0001 | Marodim

import tkinter as tk
from tkinter import font, messagebox, ttk
import requests
import threading
import time
import datetime
import webbrowser
import re
from colorama import init

# Rich Presence
from pypresence import Presence

init(autoreset=True)

class MARODIMSpammer:
    def __init__(self, root):
        self.root = root
        self.root.title("MARODIM - WebhookSpammer / Deleter / Info")
        self.root.geometry("1300x900")
        self.root.configure(bg="#000000")
        self.root.resizable(True, True)

        # RPC & App Config
        self.application_id = "1416501361281073295" 
        self.RPC = None
        self.start_time = int(time.time())

        # Tkinter vars
        self.custom_font = font.Font(family="Segoe UI", size=10)
        self.webhook_url = tk.StringVar()
        self.spam_message = tk.StringVar(value="Spam message")
        self.spam_delay_ms = tk.StringVar(value="1000")
        self.running = False
        self.spam_thread = None

        self.root.columnconfigure(0, weight=1)
        for i in range(4):
            self.root.rowconfigure(i, weight=1 if i == 2 else 0)

        
        self.create_widgets()

        
        self.connect_rpc()
        self.update_rpc(state="Idle", details="MARODIM - WebhookSpammer")

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def connect_rpc(self):
        try:
            self.RPC = Presence(self.application_id)
            self.RPC.connect()
        except Exception as e:
            self.RPC = None

    def update_rpc(self, state="Idle", details="MARODIM - WebhookSpammer"):
        if self.RPC is None:
            return
        try:
            self.RPC.update(
                state=state,
                details=details,
                large_image="MARODIM_icon",  
                large_text="MARODIM",
                start=self.start_time,
                buttons=[{"label": "Join Server", "url": "https://discord.gg/5zyUYf3Gcd"}]
            )
        except Exception as e:
            
            try:
                self.log(f"[RPC ERROR] Failed to update: {e}")
            except:
                print(f"[RPC ERROR] Failed to update: {e}")

    def on_closing(self):
        if self.RPC:
            try:
                self.RPC.close()
            except:
                pass
        self.root.destroy()

    def create_widgets(self):
        title_frame = tk.Frame(self.root, bg="#1a1a1a")
        title_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        title_frame.columnconfigure(1, weight=1)

        logo = tk.Label(title_frame, text="M", font=("Arial", 24), bg="#1a1a1a", fg="#FFFFFF")
        logo.grid(row=0, column=0, padx=5, sticky="w")

        title_label = tk.Label(
            title_frame,
            text="MARODIM - Webhook Spammer",
            font=("Segoe UI", 16, "bold"),
            bg="#1a1a1a",
            fg="#ffffff"
        )
        title_label.grid(row=0, column=1, sticky="w", padx=5)

        notebook_frame = tk.Frame(self.root, bg="#1a1a1a")
        notebook_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
        notebook_frame.columnconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background="#1a1a1a", borderwidth=0)
        style.configure("TNotebook.Tab", 
                       background="#2d2d2d", 
                       foreground="#ffffff",
                       font=self.custom_font,
                       padding=[15, 8])
        style.map("TNotebook.Tab", 
                 background=[("selected", "#FF0000")],
                 foreground=[("selected", "white")])

        self.tab_control = ttk.Notebook(notebook_frame)
        self.tab_control.grid(row=0, column=0, sticky="ew")

        self.info_frame = tk.Frame(self.tab_control, bg="#1a1a1a")
        self.spammer_frame = tk.Frame(self.tab_control, bg="#1a1a1a")
        self.remover_frame = tk.Frame(self.tab_control, bg="#1a1a1a")
        
        self.tab_control.add(self.info_frame, text="Info")
        self.tab_control.add(self.spammer_frame, text="Spammer")
        self.tab_control.add(self.remover_frame, text="Remover")

        self.create_spammer_tab()
        self.create_remover_tab()
        self.create_info_tab()

        log_frame = tk.Frame(self.root, bg="#1a1a1a")
        log_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=5)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        self.log_text = tk.Text(
            log_frame, 
            bg="#2d2d2d", 
            fg="#ffffff", 
            font=("Consolas", 9),
            wrap=tk.WORD, 
            height=6,
            relief="flat"
        )
        self.log_text.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        self.log_text.config(state="disabled")

        scrollbar = tk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.log_text.config(yscrollcommand=scrollbar.set)

        status_frame = tk.Frame(self.root, bg="#1a1a1a", height=20)
        status_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=5)
        status_frame.columnconfigure(0, weight=1)

        self.status_label = tk.Label(
            status_frame, 
            text="Marodim Log", 
            bg="#1a1a1a", 
            fg="#888888", 
            font=("Segoe UI", 8)
        )
        self.status_label.grid(row=0, column=0, sticky="e")

    def create_spammer_tab(self):
        frame = self.spammer_frame
        card = tk.Frame(frame, bg="#2d2d2d", padx=30, pady=30, relief="solid", bd=1)
        card.pack(expand=True, fill="both", padx=20, pady=20)
        card.columnconfigure(0, weight=1)

        tk.Label(card, text="Webhook URL", bg="#2d2d2d", fg="#ffffff", font=self.custom_font).pack(pady=5)
        tk.Entry(card, textvariable=self.webhook_url, width=60, bg="#3a3a3a", fg="white", insertbackground="white", font=self.custom_font).pack(pady=5)

        tk.Button(
            card,
            text="🔍 View Webhook Info",
            command=self.view_webhook_info,
            bg="#0400fd",
            fg="white",
            relief="flat",
            font=self.custom_font
        ).pack(pady=10)

        self.info_display = tk.Text(card, height=8, width=60, bg="#3a3a3a", fg="#00ff99", font=("Consolas", 9), wrap=tk.WORD)
        self.info_display.pack(pady=10)
        self.info_display.insert(tk.END, "Paste a webhook and click 'View Info' to see details.")
        self.info_display.config(state="disabled")

        tk.Label(card, text="Message to Spam", bg="#2d2d2d", fg="#ffffff", font=self.custom_font).pack(pady=5)
        tk.Entry(card, textvariable=self.spam_message, width=60, bg="#3a3a3a", fg="white", font=self.custom_font).pack(pady=5)

        tk.Label(card, text="Delay (ms)", bg="#2d2d2d", fg="#ffffff", font=self.custom_font).pack(pady=(15, 5))
        tk.Entry(card, textvariable=self.spam_delay_ms, width=10, bg="#3a3a3a", fg="white", font=self.custom_font, justify="center").pack(pady=5)

        tk.Button(
            card,
            text="🚀 START SPAMMING",
            command=self.start_spamming,
            bg="#00ff00",
            fg="white",
            relief="flat",
            font=("Segoe UI", 12, "bold"),
            padx=20,
            pady=10
        ).pack(pady=(15, 5))

        tk.Button(
            card,
            text="⏹️ STOP SPAMMING",
            command=self.stop_spamming,
            bg="#ff0033",
            fg="white",
            relief="flat",
            font=("Segoe UI", 12, "bold"),
            padx=20,
            pady=10
        ).pack(pady=(5, 15))

        self.spam_status_label = tk.Label(card, text="Status: Idle", bg="#2d2d2d", fg="#888888", font=self.custom_font)
        self.spam_status_label.pack(pady=5)

    def create_remover_tab(self):
        frame = self.remover_frame
        card = tk.Frame(frame, bg="#2d2d2d", padx=30, pady=30, relief="solid", bd=1)
        card.pack(expand=True, fill="both", padx=20, pady=20)
        card.columnconfigure(0, weight=1)

        tk.Label(card, text="Webhook URL to Delete", bg="#2d2d2d", fg="#ffffff", font=self.custom_font).pack(pady=5)
        tk.Entry(card, textvariable=self.webhook_url, width=60, bg="#3a3a3a", fg="white", insertbackground="white", font=self.custom_font).pack(pady=5)

        tk.Button(
            card,
            text="🗑️ DELETE WEBHOOK",
            command=self.delete_webhook,
            bg="#dc143c",
            fg="white",
            relief="flat",
            font=("Segoe UI", 12, "bold"),
            padx=20,
            pady=10
        ).pack(pady=15)

        self.delete_status_label = tk.Label(card, text="", bg="#2d2d2d", fg="#ffcc00", font=self.custom_font)
        self.delete_status_label.pack(pady=5)

    def create_info_tab(self):
        frame = self.info_frame
        center_frame = tk.Frame(frame, bg="#1a1a1a")
        center_frame.pack(expand=True, fill="both", padx=20, pady=20)
        center_frame.columnconfigure(0, weight=1)

        card = tk.Frame(center_frame, bg="#2d2d2d", padx=30, pady=30, relief="solid", bd=1)
        card.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        card.columnconfigure(0, weight=1)

        info_text = (
            "MARODIM WebhookSpammer v1.0\n\n"
            "Full Access To Marodim Legion\n\n"
            "Features:\n"
            "- Spam until you press STOP\n"
            "- Instantly delete webhooks\n"
            "- View webhook info\n"
            "- Real-time logging\n"
            "- Modern dark UI\n"
            "- Custom delay (ms)\n\n"
            "Discord: "
        )

        tk.Label(
            card,
            text=info_text,
            bg="#2d2d2d",
            fg="#ffffff",
            justify="left",
            wraplength=550,
            font=self.custom_font
        ).grid(row=0, column=0, sticky="w", padx=10, pady=10)

        discord_link = tk.Label(
            card,
            text="https://discord.gg/5zyUYf3Gcd",
            bg="#2d2d2d",
            fg="#1A81C5",
            font=self.custom_font,
            cursor="hand2"
        )
        discord_link.grid(row=1, column=0, sticky="w", padx=30, pady=2)
        discord_link.bind("<Button-1>", lambda e: webbrowser.open("https://discord.gg/5zyUYf3Gcd"))

    def validate_webhook(self, url):
        return re.match(r'^https://discord\.com/api/webhooks/[0-9]+/[a-zA-Z0-9_-]+$', url) is not None

    def log(self, message):
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        full_message = f"[{timestamp}] {message}"
        print(full_message)

        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, full_message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def stop_spamming(self):
        if self.running:
            self.running = False
            self.spam_status_label.config(text="Status: Stopping...", fg="#ffcc00")
            self.log("[STOP] User requested to stop spamming")
            self.update_rpc(state="Idle", details="MARODIM - WebhookSpammer")
        else:
            self.log("[INFO] Spamming is not currently running")

    def start_spamming(self):
        url = self.webhook_url.get().strip()
        message = self.spam_message.get().strip()

        if not url:
            messagebox.showerror("Error", "❌ Webhook URL is required")
            return
        if not self.validate_webhook(url):
            messagebox.showerror("Error", "❌ Invalid Webhook URL")
            return
        if not message:
            messagebox.showerror("Error", "❌ Message cannot be empty")
            return

        try:
            delay_ms = int(self.spam_delay_ms.get())
            if delay_ms < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "❌ Delay must be a positive number (in ms)")
            return

        if self.running:
            messagebox.showinfo("Warning", "⚠️ Spamming is already running")
            return

        self.running = True
        self.spam_status_label.config(text="Status: Running...", fg="#00ff00")
        self.update_rpc(state="Spamms A Webhook", details="MARODIM - WebhookSpammer")

        self.spam_thread = threading.Thread(target=self.spam_loop, args=(url, message, delay_ms), daemon=True)
        self.spam_thread.start()
        self.log(f"[START] Spamming started with {delay_ms}ms delay.")

    def spam_loop(self, url, message, delay_ms):
        sent_count = 0
        while self.running:
            try:
                res = requests.post(url, json={"content": message}, params={'wait': True})
                if res.status_code in (200, 204):
                    sent_count += 1
                    self.log(f"[SUCCESS] Message #{sent_count} sent")
                elif res.status_code == 429:
                    retry = res.json().get('retry_after', 1)
                    self.log(f"[RATELIMIT] Waiting {retry}s")
                    time.sleep(retry)
                    continue
                else:
                    self.log(f"[ERROR] HTTP {res.status_code}")
            except Exception as e:
                self.log(f"[EXCEPTION] {e}")
            time.sleep(delay_ms / 1000.0)

        self.root.after(0, lambda: self.spam_status_label.config(
            text=f"Status: Stopped ({sent_count} sent)", fg="#ff6b6b"
        ))
        self.log(f"[STOPPED] Total messages sent: {sent_count}")

    def delete_webhook(self):
        url = self.webhook_url.get().strip()
        if not url or not self.validate_webhook(url):
            messagebox.showerror("Error", "❌ Invalid or missing Webhook URL")
            return

        if not messagebox.askyesno("Confirm", "⚠️ Delete this webhook? This cannot be undone."):
            return

        self.update_rpc(state="Deleting Webhook...", details="MARODIM - WebhookSpammer")

        try:
            res = requests.delete(url)
            if res.status_code == 204:
                self.delete_status_label.config(text="✅ Webhook Deleted", fg="#00ff00")
                self.log("[SUCCESS] Webhook deleted")
                messagebox.showinfo("Success", "✅ Webhook deleted!")
            else:
                self.delete_status_label.config(text=f"❌ Failed (Status: {res.status_code})", fg="#ff0000")
                self.log(f"[ERROR] Delete failed. Status: {res.status_code}")
                messagebox.showerror("Error", f"❌ Failed. Status: {res.status_code}")
        except Exception as e:
            self.delete_status_label.config(text=f"❌ Error: {e}", fg="#ff0000")
            self.log(f"[EXCEPTION] {e}")
            messagebox.showerror("Error", f"❌ {e}")
        finally:
            self.root.after(2000, lambda: self.update_rpc(state="Idle", details="MARODIM - WebhookSpammer"))

    def view_webhook_info(self):
        url = self.webhook_url.get().strip()
        if not url or not self.validate_webhook(url):
            messagebox.showerror("Error", "❌ Invalid Webhook URL")
            return

        try:
            self.log("[INFO] Fetching webhook info...")
            res = requests.get(url)
            if res.status_code == 200:
                data = res.json()
                info = "\n".join([
                    f"Name: {data.get('name', 'N/A')}",
                    f"ID: {data.get('id', 'N/A')}",
                    f"Channel ID: {data.get('channel_id', 'N/A')}",
                    f"Guild ID: {data.get('guild_id', 'N/A')}",
                    f"Avatar: {data.get('avatar', 'None')}",
                    f"Token: {data.get('token', 'N/A')}",
                    f"Type: {'Incoming' if data.get('type') == 1 else 'Unknown'}",
                ])
                self.info_display.config(state="normal")
                self.info_display.delete(1.0, tk.END)
                self.info_display.insert(tk.END, info)
                self.info_display.config(state="disabled")
                self.log("[SUCCESS] Webhook info displayed")
            else:
                self.log(f"[ERROR] HTTP {res.status_code}")
                messagebox.showerror("Error", f"❌ HTTP {res.status_code}")
        except Exception as e:
            self.log(f"[EXCEPTION] {e}")
            messagebox.showerror("Error", f"❌ {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MARODIMSpammer(root)
    root.mainloop()