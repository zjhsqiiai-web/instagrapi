import time
import random
import requests
from instagrapi import Client

class APIInstagramBot:
    def __init__(self, session_id: str, thread_id: str):
        self.client = Client()
        self.thread_id = thread_id
        self.session_id = session_id
        
    def authenticate(self):
        try:
            # Load session safely without wiping device tokens
            self.client.login_by_sessionid(self.session_id)
            print(f"[+] Authenticated successfully as UID: {self.client.user_id}", flush=True)
            return True
        except Exception as e:
            print(f"[-] Authentication failed: {e}", flush=True)
            return False

    def send_api_message(self, text: str):
        try:
            # Direct API mutation call (skips browser entirely)
            # target_ids expects a list of thread_ids for group/direct routing
            self.client.direct_send(text, thread_ids=[self.thread_id])
            return True
        except Exception as e:
            print(f"[!] API send error: {e}", flush=True)
            return False

    async def run_spam_loop(self, base_text: str, delay: float = 0.3):
        print(f"[+] Starting pure API spam loop on thread {self.thread_id}...", flush=True)
        while True:
            try:
                # Append invisible hash characters to evade spam filters (just like your previous design)
                stealth_hash = "".join(random.choices(["\u200B", "\u200C", "\u200D", "\uFEFF"], k=3))
                payload = f"{base_text} {stealth_hash}"
                
                success = self.send_api_message(payload)
                if not success:
                    print("[!] Packet dropped or rate-limited by server. Backing off...", flush=True)
                    time.sleep(2)
                
                # Jittered delay to maintain socket stability
                time.sleep(random.uniform(delay, delay + 0.05))
            except Exception as e:
                print(f"[!] Loop exception: {e}", flush=True)
                time.sleep(1)

if __name__ == "__main__":
    SESSION_ID = "YOUR_SESSION_ID_HERE"
    THREAD_ID = "1038149162311376"
    
    bot = APIInstagramBot(SESSION_ID, THREAD_ID)
    if bot.authenticate():
        # Test run
        bot.send_api_message("⚡ Pure API Engine Online! Zero-Browser Mode Active.")
