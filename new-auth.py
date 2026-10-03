import time
import random
import os
from instagrapi import Client

# 500 IQ: Zero-width non-printing characters for Meta hash evasion
INVISIBLE_CHARS = ["\u200B", "\u200C", "\u200D", "\uFEFF"]

# Stateful Heart Array: Every line in a single message block gets this exact heart
HEART_EMOJIS = ["💚", "💙", "❤️", "🖤", "🤎", "💛", "💜", "🧡", "🤍", "🩶", "🩷"]

def generate_locked_heart_block(base_text: str, chosen_heart: str, line_count: int = 35) -> str:
    lines = []
    current_len = 0
    
    for _ in range(line_count):
        # Unique stealth signature for every single line
        stealth_hash = "".join(random.choices(INVISIBLE_CHARS, k=3))
        
        # Every line in this block uses the exact same chosen heart
        line = f"{base_text} <{chosen_heart}> {stealth_hash}"
        addition = len(line) + 2 
        
        # Stay safely under Instagram's hard 920-character message payload limit
        if current_len + addition > 920:
            break
            
        lines.append(line)
        current_len += addition
        
    return "\n\n".join(lines)

class AdvancedAPISpammer:
    def __init__(self, session_id: str, prefix: str = "^"):
        self.client = Client()
        self.session_id = session_id
        self.prefix = prefix
        self.is_running = True
        self.processed_msg_ids = set()
        self.active_spam_threads = {}

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
        print(f"[+] GOD-LEVEL API ENGINE ACTIVE. Listening across chats for '{self.prefix}'...", flush=True)
        
        while self.is_running:
            try:
                # Omni-channel scan across recent inbox threads
                threads = self.client.direct_threads(amount=15)
                
                for thread in threads:
                    thread_id = thread.id
                    messages = thread.messages
                    
                    if not messages:
                        continue
                        
                    latest_msg = messages[0]
                    msg_id = latest_msg.id
                    msg_text = latest_msg.text or ""
                    
                    if msg_id not in self.processed_msg_ids:
                        self.processed_msg_ids.add(msg_id)
                        if len(self.processed_msg_ids) > 200:
                            self.processed_msg_ids.pop()
                            
                        if msg_text.startswith(self.prefix):
                            print(f"[+] Command caught in Thread {thread_id}: {msg_text}", flush=True)
                            self.handle_command(thread_id, msg_text)
                            
            except Exception as e:
                print(f"[!] Polling glitch: {e}", flush=True)
            
            time.sleep(1.0)

    def handle_command(self, thread_id: str, full_text: str):
        parts = full_text.split(" ")
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd == f"{self.prefix}ping":
            self.send_message(thread_id, "Pong! 🏓 Max-Velocity API Engine Live! ⚡")

        elif cmd == f"{self.prefix}spam":
            if not args:
                self.send_message(thread_id, "Usage: ^spam <text>")
                return
            
            spam_text = " ".join(args)
            self.active_spam_threads[thread_id] = True
            self.send_message(thread_id, f"⚡ Locked Heart Block Spammer Initialized!")
            
            # Start background execution loop for this thread
            self.execute_max_speed_spam(thread_id, spam_text)

        elif cmd == f"{self.prefix}unspam":
            if thread_id in self.active_spam_threads:
                self.active_spam_threads[thread_id] = False
                self.send_message(thread_id, "🛑 Spam engine halted.")

    def execute_max_speed_spam(self, thread_id: str, base_text: str):
        heart_index = 0
        
        while self.active_spam_threads.get(thread_id, False):
            try:
                # 1. Select the heart for this entire block (all lines match this heart)
                current_heart = HEART_EMOJIS[heart_index % len(HEART_EMOJIS)]
                
                # 2. Generate multi-line block payload with locked heart
                payload = generate_locked_heart_block(base_text, current_heart, line_count=35)
                
                # 3. Fire instantly via API
                self.client.direct_send(payload, thread_ids=[thread_id])
                
                # 4. Advance heart index so the next message block rotates to the next heart
                heart_index += 1
                
                # 5. Optimized raw speed floor
                time.sleep(0.08)
            except Exception as e:
                print(f"[!] Spam execution glitch: {e}", flush=True)
                time.sleep(0.5)

if __name__ == "__main__":
    SESSION_ID = os.getenv("INSTAGRAM_SESSION_ID", "41189314550%3A7WhcJAptbbpNKs%3A26%3AAYkNdytwwPKGvE5tlG9skpmHpiucQ_Krtg9OMZXmrg")
    
    bot = AdvancedAPISpammer(SESSION_ID)
    if bot.authenticate():
        bot.run_omni_poll_loop()
