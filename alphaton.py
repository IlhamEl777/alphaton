import asyncio
import json
import random
import string
import time
from asyncio import Semaphore
from urllib.parse import unquote

import aiohttp

from utils.headers import headers_set

sem = Semaphore(10)  # Batasi jumlah koneksi simultan
timeout = aiohttp.ClientTimeout(total=60)
max_retries = 3


# HANDLE SEMUA ERROR TAROH DISINI BANG SAFE_POST
async def safe_post(session, url, headers, json_payload):
    retries = 5
    for attempt in range(retries):
        async with session.post(url, headers=headers, json=json_payload) as response:
            if response.status == 200:
                return await response.json()  # Return the JSON response if successful
            else:
                print(f"❌ Gagal dengan status {response.status}, mencoba lagi ")
                if attempt < retries - 1:  # Jika ini bukan percobaan terakhir, tunggu sebelum mencoba lagi
                    await asyncio.sleep(10)
                else:
                    print("❌ Gagal setelah beberapa percobaan. Memulai ulang...")
                    return None
    return None


def generate_random_nonce(length=52):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


# Mendapatkan akses token
async def fetch(account_line):
    with open('query_id.txt', 'r') as file:
        lines = file.readlines()
        raw_data = lines[account_line - 1].strip()

    tg_web_data = unquote(unquote(raw_data))
    url = 'https://tapcoin-api.alphatongame.com/api/v1/Token/SignIn'
    headers = headers_set.copy()  # Membuat salinan headers_set agar tidak mengubah variabel global

    data = {
        "webAppData": tg_web_data
    }

    for attempt in range(max_retries):
        async with aiohttp.ClientSession(timeout=timeout) as session:
            try:
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        print(f"Attempt {attempt + 1} for user {account_line} failed with status {response.status}")
            except aiohttp.ClientError as e:
                print(f"Request error for user {account_line} on attempt {attempt + 1}: {e}")

        await asyncio.sleep(1)  # Optional: wait before retrying

    return None


# Cek akses token
async def cek_user(index):
    data = await fetch(index + 1)
    access_token = data['result']['token']['accessToken']

    headers = headers_set.copy()  # Membuat salinan headers_set agar tidak mengubah variabel global
    headers['Authorization'] = f'Bearer {access_token}'
    user_data = data['result']
    return user_data


async def submit_taps(json_payload, token):
    url = "https://tapcoin-api.alphatongame.com/api/v1/Plinko/PlinkoIncomeRegistration"

    headers = headers_set.copy()
    headers['Authorization'] = f'Bearer {token}'

    for attempt in range(max_retries):
        async with aiohttp.ClientSession(timeout=timeout) as session:
            try:
                async with session.post(url, headers=headers, json=json_payload) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        print(f"❌ Gagal dengan status {response.status}, mencoba lagi...")
            except aiohttp.ClientError as e:
                print(f"❌ Gagal. mencoba lagi... - {attempt + 1}")

        await asyncio.sleep(1)  # Optional: wait before retrying

    return None


async def upgrade_energy(token):
    url = "https://tapcoin-api.alphatongame.com/api/v1/Boost/LevelUp/0"

    headers = headers_set.copy()
    headers['Authorization'] = f'Bearer {token}'

    for attempt in range(max_retries):
        async with aiohttp.ClientSession(timeout=timeout) as session:
            try:
                async with session.post(url, headers=headers) as response:
                    if response.status == 200:
                        print(f"\r✅ Sukses Upgrade | Level 🔋 +1 \n ")
                        return await response.json()
                    else:
                        print(f"❌ Gagal dengan status {response.status}, mencoba lagi...")
            except aiohttp.ClientError as e:
                print(f"❌ Gagal. mencoba lagi... - {attempt + 1}")

        await asyncio.sleep(1)  # Optional: wait before retrying

    return None

async def main():
    print("Starting Alphaton bot...")
    print("\r Mendapatkan list akun valid...", end="", flush=True)
    while True:
        with open('query_id.txt', 'r') as file:
            lines = file.readlines()

        # Kumpulkan informasi akun terlebih dahulu
        accounts = []
        for index, line in enumerate(lines):
            result = await cek_user(index)
            if result is not None:
                first_name = result['user'].get('name', 'Unknown')
                telegram_id = result['user'].get('telegramId', 'Unknown')
                accounts.append((index, result, first_name, telegram_id))
            else:
                print(f"❌ Akun {index + 1}: Token tidak valid atau terjadi kesalahan")

        # Menampilkan daftar akun
        print("\rList akun:                                   ", flush=True)
        for index, _, first_name, telegram_id in accounts:
            print(f"✅ [ Akun {first_name} {telegram_id} ] ")

        # Setelah menampilkan semua akun, mulai memeriksa tugas
        for index, result, first_name, telegram_id in accounts:
            token = result['token']['accessToken']
            stat_result = await cek_user(index)

            if stat_result is not None:
                user_data = stat_result['user']
                coin = user_data['balanceCoin']
                energy = user_data['availableEnergy']
                level = user_data['limitEnergyLevel']['level']

                output = (
                    f"[ Akun {index + 1} - {first_name} {telegram_id} ]\n"
                    f"Coin 🪙  {coin:,} 🔋 {energy} - {user_data['limitEnergyLevel']['value']}\n"
                )
                print(output, end="", flush=True)

                # jika level kurang dari sama dengan 7 dan coin lebih besar sama dengan 128000
                if level < 7 and coin >= 128000:
                    output = (
                        f"Coin 🪙  {user_data['balanceCoin']:,} Level🔋 {user_data['limitEnergyLevel']['level']}\n"
                        f"Mencoba menaikkan Level 🔋\n"
                    )

                    print(output, end="", flush=True)
                    await upgrade_energy(token)

                availableEnergy = user_data['availableEnergy']
                energy_used = 200
                tap = 1000

                tap_payload = {
                    "usedEnergy": energy_used,
                    "totalProfit": tap
                }

                if availableEnergy < 200:
                    print(f"\rEnergi🔋 {availableEnergy} | 🔋 Energi kurang, minimal 200 \n ")
                    continue
                tap_result = await submit_taps(tap_payload, token)

                if tap_result['registrationStatus'] is not None:
                    print(f"\rTapped + {energy_used}✅ | 🔋 {tap_result['userInfo']['availableEnergy']} \n ")
                else:
                    print(f"❌ Gagal dengan status {json.dumps(tap_result)}, mencoba lagi...")

        print("=== [ SEMUA AKUN TELAH DI PROSES ] ===")

        animate_energy_recharge(15)


def animate_energy_recharge(duration):
    frames = ["|", "/", "-", "\\"]
    end_time = time.time() + duration
    while time.time() < end_time:
        remaining_time = int(end_time - time.time())
        for frame in frames:
            print(f"\r🪫 Mengisi ulang energi {frame} - Tersisa {remaining_time} detik         ", end="", flush=True)
            time.sleep(0.25)
    print("\r🔋 Pengisian energi selesai.                            ", flush=True)


asyncio.run(main())
