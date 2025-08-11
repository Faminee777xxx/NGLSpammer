import requests
import time
import random
import os, sys
from datetime import datetime
import threading


from colorama import Fore, Back, Style
fore_colors = {
	"black": Fore.BLACK,
	"red": Fore.RED,
	"green": Fore.GREEN,
	"yellow": Fore.YELLOW,
	"blue": Fore.BLUE,
	"magenta": Fore.MAGENTA,
	"cyan": Fore.CYAN,
	"white": Fore.WHITE,
	"reset": Fore.RESET
}

back_colors = {
	"black": Back.BLACK,
	"red": Back.RED,
	"green": Back.GREEN,
	"yellow": Back.YELLOW,
	"blue": Back.BLUE,
	"magenta": Back.MAGENTA,
	"cyan": Back.CYAN,
	"white": Back.WHITE,
	"reset": Back.RESET
}

styles = {
	"dim": Style.DIM,
	"normal": Style.NORMAL,
	"bright": Style.BRIGHT,
	"reset": Style.RESET_ALL
}

def banner():
    print(f"""
 __    _  _______  _______    _______  _______  __    _  __    _  _______    ___      ___   _______ 
|  |  | ||       ||       |  |       ||       ||  |  | ||  |  | ||   _   |  |   |    |   | |       |
|   |_| ||   _   ||_     _|  |    ___||   _   ||   |_| ||   |_| ||  |_|  |  |   |    |   | |    ___|
|       ||  | |  |  |   |    |   | __ |  | |  ||       ||       ||       |  |   |    |   | |   |___ 
|  _    ||  |_|  |  |   |    |   ||  ||  |_|  ||  _    ||  _    ||       |  |   |___ |   | |    ___|
| | |   ||       |  |   |    |   |_| ||       || | |   || | |   ||   _   |  |       ||   | |   |___ 
|_|  |__||_______|  |___|    |_______||_______||_|  |__||_|  |__||__| |__|  |_______||___| |_______|!!!
[{back_colors['green']}NGL-Spammer{back_colors['reset']}]>V.1
[{back_colors['green']}Github{back_colors['reset']}]: 

    """)
    
tor_answer = ["T", "t", "tor"]
proxy_answer = ["P", "p", "proxy"]
no_answer = ["N", "n", "no"]

counter = 0
counter_lock = threading.Lock()  # ใช้ล็อกเวลานับ counter ให้ปลอดภัยใน thread

# Check tor
def load_proxies(file_path):
    proxies_list = []
    try:
        with open(file_path, "r") as f:
            for line in f:
                proxy = line.strip()
                if proxy:
                    proxies_list.append(proxy)
    except FileNotFoundError:
        print(f"[{back_colors['red']}!{back_colors['reset']}] {styles['bright']}Proxy file {file_path} not found.{styles['reset']}")
    return proxies_list
    
def random_device_id(length=21):
    return ''.join(random.choice('0123456789abcdef') for _ in range(length * 2))
         
def send_message(username, message, proxy_list=None, use_tor=False):
    global counter
    url = "https://ngl.link/api/submit"

    headers = {
        "User-Agent": f"{user_agents}",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Referer": f"https://ngl.link/{username}",
        "Origin": "https://ngl.link"
    }

    while True:
        try:
            now = datetime.now().strftime("%H:%M")
            device_id = random_device_id()

            data = {
                "username": username,
                "question": message,
                "deviceId": device_id,
                "gameSlug": "",
                "referrer": ""
            }

            # เลือก proxy
            proxies = None
            if use_tor:
                proxies = {
                    "http": "socks5h://127.0.0.1:9050",
                    "https": "socks5h://127.0.0.1:9050"
                }
            elif proxy_list:
                proxy_addr = random.choice(proxy_list)
                proxies = {
                    "http": f"socks5h://{proxy_addr}",
                    "https": f"socks5h://{proxy_addr}"
                }

            response = requests.post(url, headers=headers, data=data, timeout=10, proxies=proxies)

            if response.status_code != 200:
                print(f"[{back_colors['cyan']}{now}{back_colors['reset']}] [{back_colors['red']}Err{back_colors['reset']}] {styles['bright']}Ratelimited or blocked{styles['reset']}")
                time.sleep(25)
            else:
                with counter_lock:
                    counter += 1
                    print(f"[{back_colors['cyan']}{now}{back_colors['reset']}] [{back_colors['green']}Msg{back_colors['reset']}] Sent: {styles['bright']}{counter}{styles['reset']}")

        except Exception as e:
            print(f"[{back_colors['cyan']}{now}{back_colors['reset']}] [{back_colors['red']}Err{back_colors['reset']}] {styles['bright']}{e}{styles['reset']}")
            time.sleep(5)

def start_threads(username, message, thread_count, proxy_list=None, use_tor=False):
    threads = []
    for _ in range(thread_count):
        t = threading.Thread(target=send_message, args=(username, message, proxy_list, use_tor))
        t.daemon = True
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

# ตัวอย่างเรียกใช้
if __name__ == "__main__":
    banner()
    ua_path = os.path.join("user_agent", "user_agent_lists.txt")
    if not os.path.isfile(ua_path):
        print(f"[{back_colors['red']}ERROR{back_colors['reset']}] {styles['bright']}File not found: {ua_path}{styles['reset']}")
        print(f"[{back_colors['yellow']}INFO{back_colors['reset']}] Make sure the file exists and the path is correct.")
        sys.exit(1)  # หยุดโปรแกรม
    else:
        with open(ua_path, 'r', encoding='utf-8') as file:
            user_agents = [line.strip() for line in file if line.strip()]

        print(f"[{back_colors['green']}INFO{back_colors['reset']}] {styles['bright']}Loaded {len(user_agents)} user agents from{styles['reset']} {ua_path}")
    username = input(f"[{back_colors['green']}!{back_colors['reset']}] {styles['bright']}Target Username{styles['reset']}: ")  # ใส่ชื่อเป้าหมายที่ต้องการ
    message = input(f"[{back_colors['green']}!{back_colors['reset']}] {styles['bright']}Message{styles['reset']}: ")
    thread_count = int(input(f"[{back_colors['green']}+{back_colors['reset']}] {styles['bright']}Threads{styles['reset']}: "))
    if thread_count > 10:
        print(f"\n[{back_colors['yellow']}!{back_colors['reset']}] {styles['bright']}Threads max 10 (default: 5){styles['reset']}")
        thread_count = 5
    else:
        pass

    use_proxy_or_t = input(f"[{back_colors['magenta']}#{back_colors['reset']}] {styles['bright']}Proxy, Tor or No (P/T/N){styles['reset']}: ").strip().lower()
    if use_proxy_or_t in tor_answer:
        use_tor = True
        proxy_list = None
    elif use_proxy_or_t in proxy_answer:
        use_tor = False
        proxy_file_input = input(f"[{back_colors['green']}+] {styles['bright']}File proxies.txt{styles['reset']}: ")
        proxy_list = load_proxies(proxy_file_input)
        if not proxy_list:
            print(f"[{back_colors['red']}!{back_colors['reset']}] {styles['reset']}No proxies loaded, running without proxy{styles['reset']}")
            proxy_list = None
    else:
        use_tor = False
        proxy_list = None

    print(f"[{back_colors['yellow']}!{back_colors['reset']}] Ctrl+C to {styles['bright']}EXIT{styles['reset']}\n")
    time.sleep(1)
    start_threads(username, message, thread_count, proxy_list, use_tor)
