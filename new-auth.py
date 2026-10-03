import time
import random
import os
import json
from instagrapi import Client

# Stealth invisible characters for hash evasion
INVISIBLE_CHARS = ["\u200B", "\u200C", "\u200D", "\uFEFF"]
HEART_EMOJIS = ["💚", "💙", "❤️", "🖤", "🤎", "💛", "💜", "🧡", "🤍", "🩶", "🩷"]

class DynamicAPIBot:
    def __init__(self, session_id: str, prefix: str = "^"):
        self.client = Client()
        self.session_id = session_id
        self.prefix = prefix
        self.is_running = True
        self.processed_msg_ids = set()
        self.active_spam_threads = {}  # thread_id -> bool (tracking active spam loops)

    def authenticate(self):
        try:
            self.client.login_by_sessionid(self.session_id)
            print(f"[+] Authenticated successfully as UID: {self.client.user_id}", flush=True)
            return True
        except Exception as e:
            print(f"[-] Authentication failed: {e}", flush=True)
            return False

    def send_message(self, thread_id: str, text: str):
        try:
            self.client.direct_send(text, thread_ids=[thread_id])
            return True
        except Exception as e:
            print(f"[!] Send error on thread {thread_id}: {e}", flush=True)
            return False

    def run_omni_poll_loop(self):
        print(f"[+] OMNI-CHANNEL POLLING ACTIVE. Listening across all recent chats for '{self.prefix}'...", flush=True)
        
        while self.is_running:
            try:
                # Pull recent threads from inbox (covers both 1:1 and group chats)
                threads = self.client.direct_threads(amount=15)
                
                for thread in threads:
                    thread_id = thread.id
                    messages = thread.messages
                    
                    if not messages:
                        continue
                        
                    latest_msg = messages[0]
                    msg_id = latest_msg.id
                    msg_text = latest_msg.text or ""
                    
                    # If this is a brand new message we haven't handled yet
                    if msg_id not in self.processed_msg_ids:
                        self.processed_msg_ids.add(msg_id)
                        
                        # Keep memory set size manageable
                        if len(self.processed_msg_ids) > 200:
                            self.processed_msg_ids.pop()
                            
                        if msg_text.startswith(self.prefix):
                            print(f"[+] Command detected in Thread {thread_id}: {msg_text}", flush=True)
                            self.handle_command(thread_id, msg_text)
                            
            except Exception as e:
                print(f"[!] Polling cycle exception: {e}", flush=True)
            
            # Scan interval (fast enough for responsiveness, safe from 429 errors)
            time.sleep(1.2)

    def handle_command(self, thread_id: str, full_text: str):
        parts = full_text.split(" ")
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd == f"{self.prefix}ping":
            self.send_message(thread_id, "Pong! 🏓 Omni-Detection Engine Active & Linked! ⚡")

        elif cmd == f"{self.prefix}spam":
            if not args:
                self.send_message(thread_id, "Usage: ^spam <text>")
                return
            
            spam_text = " ".join(args)
            self.active_spam_threads[thread_id] = True
            self.send_message(thread_id, f"⚡ Auto-Detected Target Thread! Launching Max-Speed Spam...")
            
            # Execute spam sequence for this specific thread
            self.execute_spam_loop(thread_id, spam_text)

        elif cmd == f"{self.prefix}unspam":
            if thread_id in self.active_spam_threads:
                self.active_spam_threads[thread_id] = False
                self.send_message(thread_id, "🛑 Spam engine halted for this chat.")

    def execute_spam_loop(self, thread_id: str, base_text: str):
        # Runs a fast burst loop targeted explicitly at the auto-detected thread
        while self.active_spam_threads.get(thread_id, False):
            try:
                heart = random.choice(HEART_EMOJIS)
                stealth_hash = "".join(random.choices(INVISIBLE_CHARS, k=3))
                payload = f"{base_text} <{heart}>{stealth_hash}"

                self.send_message(thread_id, payload)
                
                # Near-instant delay for high throughput
                time.sleep(0.3)
            except Exception as e:
                print(f"[!] Spam loop error on thread {thread_id}: {e}", flush=True)
                time.sleep(1)

if __name__ == "__main__":
    SESSION_ID = os.getenv("INSTAGRAM_SESSION_ID", "41189314550%3A7WhcJAptbbpNKs%3A26%3AAYkNdytwwPKGvE5tlG9skpmHpiucQ_Krtg9OMZXmrg")
    
    bot = DynamicAPIBot(SESSION_ID)
    if bot.authenticate():
        bot.run_omni_poll_loop()
