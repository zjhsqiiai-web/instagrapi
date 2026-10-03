import time
import random
import os
import gc
from instagrapi import Client

# Zero-width non-printing characters for Meta duplicate-content filter evasion
INVISIBLE_CHARS = ["\u200B", "\u200C", "\u200D", "\uFEFF"]

# Stateful Heart Array: All lines in a single message block share the exact same heart
HEART_EMOJIS = ["💚", "💙", "❤️", "🖤", "🤎", "💛", "💜", "🧡", "🤍", "🩶", "🩷"]

def generate_locked_heart_block(base_text: str, chosen_heart: str, line_count: int = 35) -> str:
    lines = []
    current_len = 0
    
    for _ in range(line_count):
        stealth_hash = "".join(random.choices(INVISIBLE_CHARS, k=3))
        line = f"{base_text} <{chosen_heart}> {stealth_hash}"
        addition = len(line) + 2 
        
        # Enforce Instagram's 920-character payload ceiling per transmission
        if current_len + addition > 920:
            break
            
        lines.append(line)
        current_len += addition
        
    return "\n\n".join(lines)

class EngineerAPISpammer:
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
            print(f"[+] Session active. Authenticated UID: {self.client.user_id}", flush=True)
            return True
        except Exception as e:
            print(f"[-] Authentication failed (Dead session cookie?): {e}", flush=True)
            return False

    def send_message(self, thread_id: str, text: str):
        try:
            self.client.direct_send(text, thread_ids=[thread_id])
            return True
        except Exception as e:
            print(f"[!] Packet dispatch error on thread {thread_id}: {e}", flush=True)
            return False

    def run_omni_poll_loop(self):
        print(f"[+] High-Performance Omni-Listener Online. Monitoring inbox for '{self.prefix}'...", flush=True)
        
        poll_ticks = 0
        while self.is_running:
            try:
                # Dynamic inbox scanning across active threads
                threads = self.client.direct_threads(amount=10)
                
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
                        
                        # Bounded memory set to prevent leaks
                        if len(self.processed_msg_ids) > 150:
                            self.processed_msg_ids.pop()
                            
                        if msg_text.startswith(self.prefix):
                            print(f"[+] Command captured in Thread {thread_id}: {msg_text}", flush=True)
                            self.handle_command(thread_id, msg_text)
                            
                # Periodic garbage collection sweep to protect Railway RAM limits
                poll_ticks += 1
                if poll_ticks >= 30:
                    gc.collect()
                    poll_ticks = 0
                            
            except Exception as e:
                print(f"[!] Polling loop exception (re-syncing): {e}", flush=True)
            
            time.sleep(1.0)

    def handle_command(self, thread_id: str, full_text: str):
        parts = full_text.split(" ")
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd == f"{self.prefix}ping":
            self.send_message(thread_id, "Pong! 🏓 Engineer Engine Responding Instantly! ⚡")

        elif cmd == f"{self.prefix}spam":
            if not args:
                self.send_message(thread_id, "Usage: ^spam <text>")
                return
            
            spam_text = " ".join(args)
            self.active_spam_threads[thread_id] = True
            self.send_message(thread_id, f"⚡ Locked Heart Block Spammer Initialized!")
            
            self.execute_max_speed_spam(thread_id, spam_text)

        elif cmd == f"{self.prefix}unspam":
            if thread_id in self.active_spam_threads:
                self.active_spam_threads[thread_id] = False
                self.send_message(thread_id, "🛑 Spam engine halted.")

    def execute_max_speed_spam(self, thread_id: str, base_text: str):
        heart_index = 0
        message_counter = 0
        
        while self.active_spam_threads.get(thread_id, False):
            try:
                # 1. Select locked heart for the current multi-line block
                current_heart = HEART_EMOJIS[heart_index % len(HEART_EMOJIS)]
                
                # 2. Build dense block payload with hash evasion
                payload = generate_locked_heart_block(base_text, current_heart, line_count=35)
                
                # 3. Push payload directly via API route
                self.client.direct_send(payload, thread_ids=[thread_id])
                
                # 4. Advance states
                heart_index += 1
                message_counter += 1
                
                # Force memory sweep every 50 transmissions
                if message_counter % 50 == 0:
                    gc.collect()
                
                # Optimized throughput delay floor
                time.sleep(0.08)
            except Exception as e:
                print(f"[!] Execution loop anomaly: {e}", flush=True)
                time.sleep(0.4)

if __name__ == "__main__":
    SESSION_ID = os.getenv("INSTAGRAM_SESSION_ID", "41189314550%3A7WhcJAptbbpNKs%3A26%3AAYkNdytwwPKGvE5tlG9skpmHpiucQ_Krtg9OMZXmrg")
    
    bot = EngineerAPISpammer(SESSION_ID)
    if bot.authenticate():
        bot.run_omni_poll_loop()
