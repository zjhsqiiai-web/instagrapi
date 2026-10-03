import time
import random
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
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
        
        if current_len + addition > 920:
            break
            
        lines.append(line)
        current_len += addition
        
    return "\n\n".join(lines)

class HyperSaturationSpammer:
    def __init__(self, session_id: str, prefix: str = "^"):
        self.client = Client()
        self.session_id = session_id
        self.prefix = prefix
        self.is_running = True
        self.processed_msg_ids = set()
        self.active_spam_threads = {}
        # Massive 80-worker pool for absolute zero queue latency
        self.executor = ThreadPoolExecutor(max_workers=80)

    def authenticate(self):
        try:
            self.client.login_by_sessionid(self.session_id)
            print(f"[+] Session active. Authenticated UID: {self.client.user_id}", flush=True)
            return True
        except Exception as e:
            print(f"[-] Authentication failed: {e}", flush=True)
            return False

    def send_message_sync(self, thread_id: str, text: str):
        try:
            self.client.direct_send(text, thread_ids=[thread_id])
            return True
        except Exception as e:
            return False

    async def send_message_async(self, thread_id: str, text: str):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.executor, self.send_message_sync, thread_id, text)

    async def run_omni_poll_loop(self):
        print(f"[+] Hyper-Saturation Omni-Listener Online. Monitoring inbox for '{self.prefix}'...", flush=True)
        
        while self.is_running:
            try:
                loop = asyncio.get_running_loop()
                threads = await loop.run_in_executor(self.executor, lambda: self.client.direct_threads(amount=10))
                
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
                        
                        if len(self.processed_msg_ids) > 150:
                            self.processed_msg_ids.pop()
                            
                        if msg_text.startswith(self.prefix):
                            print(f"[+] Command captured in Thread {thread_id}: {msg_text}", flush=True)
                            await self.handle_command(thread_id, msg_text)
                            
            except Exception as e:
                print(f"[!] Polling exception: {e}", flush=True)
            
            await asyncio.sleep(0.6)

    async def handle_command(self, thread_id: str, full_text: str):
        parts = full_text.split(" ")
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd == f"{self.prefix}ping":
            await self.send_message_async(thread_id, "Pong! 🏓 Hyper-Saturation Engine Live! ⚡")

        elif cmd == f"{self.prefix}spam":
            if not args:
                await self.send_message_async(thread_id, "Usage: ^spam <text>")
                return
            
            spam_text = " ".join(args)
            self.active_spam_threads[thread_id] = True
            await self.send_message_async(thread_id, f"⚡ Hyper-Saturation Engine Initialized!")
            
            asyncio.create_task(self.execute_hyper_saturation_spam(thread_id, spam_text))

        elif cmd == f"{self.prefix}unspam":
            if thread_id in self.active_spam_threads:
                self.active_spam_threads[thread_id] = False
                await self.send_message_async(thread_id, "🛑 Spam engine halted.")

    async def execute_hyper_saturation_spam(self, thread_id: str, base_text: str):
        heart_index = 0
        
        while self.active_spam_threads.get(thread_id, False):
            try:
                # Fire 20 parallel requests simultaneously per wave with zero latency bottlenecks
                batch_tasks = []
                for _ in range(20):
                    current_heart = HEART_EMOJIS[heart_index % len(HEART_EMOJIS)]
                    payload = generate_locked_heart_block(base_text, current_heart, line_count=35)
                    batch_tasks.append(self.send_message_async(thread_id, payload))
                    heart_index += 1

                # Execute massive batch concurrently without blocking
                await asyncio.gather(*batch_tasks)
                
                # Zero delay. Pure hardware saturation.
                await asyncio.sleep(0.0)
            except Exception as e:
                print(f"[!] Burst execution anomaly: {e}", flush=True)
                await asyncio.sleep(0.1)

if __name__ == "__main__":
    SESSION_ID = os.getenv("INSTAGRAM_SESSION_ID", "41189314550%3A7WhcJAptbbpNKs%3A26%3AAYkNdytwwPKGvE5tlG9skpmHpiucQ_Krtg9OMZXmrg")
    
    bot = HyperSaturationSpammer(SESSION_ID)
    if bot.authenticate():
        asyncio.run(bot.run_omni_poll_loop())
