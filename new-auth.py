import time
import random
import os
from instagrapi import Client

# Stealth invisible characters for hash evasion (prevents duplicate message blocks)
INVISIBLE_CHARS = ["\u200B", "\u200C", "\u200D", "\uFEFF"]
HEART_EMOJIS = ["💚", "💙", "❤️", "🖤", "🤎", "💛", "💜", "🧡", "🤍", "🩶", "🩷"]

def generate_formatted_block(base_text: str, line_count: int = 25) -> str:
    lines = []
    current_len = 0
    
    for _ in range(line_count):
        # Generate a unique cryptographic stealth signature for EVERY single line
        stealth_hash = "".join(random.choices(INVISIBLE_CHARS, k=3))
        heart = random.choice(HEART_EMOJIS)
        
        # Format matching your multi-line layout example
        line = f"{base_text} <{heart}> {stealth_hash}"
        addition = len(line) + 2 
        
        # Stay safely under Instagram's hard 950-character message payload limit
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
            self.send_message(thread_id, f"⚡ Multi-Line Block Spammer Active!")
            
            self.execute_spam_loop(thread_id, spam_text)

        elif cmd == f"{self.prefix}unspam":
            if thread_id in self.active_spam_threads:
                self.active_spam_threads[thread_id] = False
                self.send_message(thread_id, "🛑 Spam engine halted.")

    def execute_spam_loop(self, thread_id: str, base_text: str):
        while self.active_spam_threads.get(thread_id, False):
            try:
                # Generate the custom multi-line stacked block
                payload = generate_formatted_block(base_text, line_count=30)
                
                self.send_message(thread_id, payload)
                
                # Jittered ultra-low delay to push max throughput without triggering 429 drops
                delay = random.uniform(0.15, 0.28)
                time.sleep(delay)
            except Exception as e:
                print(f"[!] Loop error: {e}", flush=True)
                time.sleep(1)

if __name__ == "__main__":
    SESSION_ID = os.getenv("INSTAGRAM_SESSION_ID", "41189314550%3A7WhcJAptbbpNKs%3A26%3AAYkNdytwwPKGvE5tlG9skpmHpiucQ_Krtg9OMZXmrg")
    
    bot = AdvancedAPISpammer(SESSION_ID)
    if bot.authenticate():
        bot.run_omni_poll_loop()
