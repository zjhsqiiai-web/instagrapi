import time
import random
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from instagrapi import Client
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

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

class MultiAccountShardedSpammer:
    def __init__(self, session_ids: list, prefix: str = "^"):
        self.session_ids = session_ids
        self.prefix = prefix
        self.is_running = True
        self.clients = []
        self.client_index = 0
        self.processed_msg_ids = set()
        self.active_spam_threads = {}
        
        # Massive worker pool to support multi-client concurrent execution
        self.executor = ThreadPoolExecutor(max_workers=100)

    def authenticate_all(self):
        for sid in self.session_ids:
            sid = sid.strip()
            if not sid:
                continue
            try:
                cl = Client()
                # Independent connection pool per client shard
                adapter = HTTPAdapter(
                    pool_connections=50,
                    pool_maxsize=50,
                    max_retries=Retry(total=1, backoff_factor=0.1)
                )
                cl.private.mount('https://', adapter)
                cl.private.mount('http://', adapter)
                
                cl.login_by_sessionid(sid)
                self.clients.append(cl)
                print(f"[+] Sharded Token Active -> UID: {cl.user_id}", flush=True)
            except Exception as e:
                print(f"[-] Token Auth Failed (Skipping dead session): {e}", flush=True)
        
        if not self.clients:
            print("[-] CRITICAL: No valid session tokens loaded in pool!")
            return False
        
        print(f"[+] Sharding Pool Online. Total Active Tokens: {len(self.clients)}")
        return True

    def get_next_client(self):
        # Round-robin load balancer across active account tokens
        client = self.clients[self.client_index % len(self.clients)]
        self.client_index += 1
        return client

    def send_message_sync(self, thread_id: str, text: str):
        client = self.get_next_client()
        try:
            client.direct_send(text, thread_ids=[thread_id])
            return True
        except Exception as e:
            print(f"[!] Shard Error (UID {getattr(client, 'user_id', 'unknown')}): {e}", flush=True)
            return False

    async def send_message_async(self, thread_id: str, text: str):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.executor, self.send_message_sync, thread_id, text)

    async def run_omni_poll_loop(self):
        print(f"[+] Sharded Omni-Listener Online. Monitoring inbox for '{self.prefix}'...", flush=True)
        # Use the primary shard for inbox polling to conserve request quota
        primary_client = self.clients[0]
        
        while self.is_running:
            try:
                loop = asyncio.get_running_loop()
                threads = await loop.run_in_executor(
                    self.executor, 
                    lambda: primary_client.direct_threads(amount=10)
                )
                
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
            await self.send_message_async(thread_id, "Pong! 🏓 Sharded Multi-Account Engine Live! ⚡")

        elif cmd == f"{self.prefix}spam":
            if not args:
                await self.send_message_async(thread_id, "Usage: ^spam <text>")
                return
            
            spam_text = " ".join(args)
            self.active_spam_threads[thread_id] = True
            await self.send_message_async(thread_id, f"⚡ Sharded Token Pool Initialized!")
            
            asyncio.create_task(self.execute_sharded_spam(thread_id, spam_text))

        elif cmd == f"{self.prefix}unspam":
            if thread_id in self.active_spam_threads:
                self.active_spam_threads[thread_id] = False
                await self.send_message_async(thread_id, "🛑 Spam engine halted.")

    async def execute_sharded_spam(self, thread_id: str, base_text: str):
        heart_index = 0
        
        while self.active_spam_threads.get(thread_id, False):
            try:
                # Fire 20 parallel requests sharded across your multi-account pool
                batch_tasks = []
                for _ in range(20):
                    current_heart = HEART_EMOJIS[heart_index % len(HEART_EMOJIS)]
                    payload = generate_locked_heart_block(base_text, current_heart, line_count=35)
                    batch_tasks.append(self.send_message_async(thread_id, payload))
                    heart_index += 1

                await asyncio.gather(*batch_tasks)
                await asyncio.sleep(0.0)
            except Exception as e:
                print(f"[!] Shard execution anomaly: {e}", flush=True)
                await asyncio.sleep(0.1)

if __name__ == "__main__":
    # Pull session IDs. Supports comma-separated list for multi-account rotation:
    # INSTAGRAM_SESSION_IDS = "session_cookie_1,session_cookie_2,session_cookie_3"
    raw_sessions = os.getenv("INSTAGRAM_SESSION_IDS", os.getenv("INSTAGRAM_SESSION_ID", ""))
    session_list = [s.strip() for s in raw_sessions.split(",") if s.strip()]
    
    bot = MultiAccountShardedSpammer(session_list)
    if bot.authenticate_all():
        asyncio.run(bot.run_omni_poll_loop())
