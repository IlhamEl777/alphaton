import requests
import time
import os
import pytz
from datetime import datetime
import random
import string

def generate_random_nonce(length=52):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

nonce_value = generate_random_nonce()
# Fungsi untuk membaca token dari file
def load_tokens(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Fungsi untuk melakukan request dengan token yang sesuai
def make_request(url, headers, json_payload):
    headers.update({
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
    })
    retries = 50  # Jumlah maksimal percobaan
    delay = 3    # Jeda dalam detik

    for i in range(retries):
        try:
            response = requests.post(url, headers=headers, json=json_payload)
            if response.status_code == 200:
                return response
            else:
                print(f"❌ Gagal dengan status {response.status_code}, mencoba lagi dalam {delay} detik...")
                time.sleep(delay)
        except Exception as e:
            print(f"❌ Kesalahan koneksi: {e}, mencoba lagi dalam {delay} detik...")
            time.sleep(delay)
    return None
# Load semua token
tokens = load_tokens('token.txt')

# URL dan endpoint yang sama untuk semua request
url = "https://api-gw-tg.memefi.club/graphql"

# Inisialisasi variabel untuk menghitung akun
account_number = 0

# Query untuk mendapatkan konfigurasi game
cek_stat = {
    "operationName": "QUERY_GAME_CONFIG",
    "variables": {},
    "query": """
    query QUERY_GAME_CONFIG {
      telegramGameGetConfig {
        ...FragmentBossFightConfig
        __typename
      }
    }

    fragment FragmentBossFightConfig on TelegramGameConfigOutput {
      _id
      coinsAmount
      currentEnergy
      maxEnergy
      weaponLevel
      energyLimitLevel
      energyRechargeLevel
      tapBotLevel
      currentBoss {
        _id
        level
        currentHealth
        maxHealth
        __typename
      }
      freeBoosts {
        _id
        currentTurboAmount
        maxTurboAmount
        turboLastActivatedAt
        turboAmountLastRechargeDate
        currentRefillEnergyAmount
        maxRefillEnergyAmount
        refillEnergyLastActivatedAt
        refillEnergyAmountLastRechargeDate
        __typename
      }
      bonusLeaderDamageEndAt
      bonusLeaderDamageStartAt
      bonusLeaderDamageMultiplier
      nonce
      __typename
    }
    """
}

tap_payload = {
    "operationName": "MutationGameProcessTapsBatch",
    "variables": {
        "payload": {
            "nonce": ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(52)),
            "tapsCount": 50
        }
    },
    "query": """
    mutation MutationGameProcessTapsBatch($payload: TelegramGameTapsBatchInput!) {
      telegramGameProcessTapsBatch(payload: $payload) {
        ...FragmentBossFightConfig
        __typename
      }
    }

    fragment FragmentBossFightConfig on TelegramGameConfigOutput {
      _id
      coinsAmount
      currentEnergy
      maxEnergy
      weaponLevel
      energyLimitLevel
      energyRechargeLevel
      tapBotLevel
      currentBoss {
        _id
        level
        currentHealth
        maxHealth
        __typename
      }
      freeBoosts {
        _id
        currentTurboAmount
        maxTurboAmount
        turboLastActivatedAt
        turboAmountLastRechargeDate
        currentRefillEnergyAmount
        maxRefillEnergyAmount
        refillEnergyLastActivatedAt
        refillEnergyAmountLastRechargeDate
        __typename
      }
      bonusLeaderDamageEndAt
      bonusLeaderDamageStartAt
      bonusLeaderDamageMultiplier
      nonce
      __typename
    }
    """
}

upgrade_payloads = {
    "wp": {
        "operationName": "telegramGamePurchaseUpgrade",
        "variables": {"upgradeType": "Damage"},
        "query": """
        mutation telegramGamePurchaseUpgrade($upgradeType: UpgradeType!) {
          telegramGamePurchaseUpgrade(type: $upgradeType) {
            ...FragmentBossFightConfig
            __typename
          }
        }
        fragment FragmentBossFightConfig on TelegramGameConfigOutput {
          _id
          coinsAmount
          currentEnergy
          maxEnergy
          weaponLevel
          energyLimitLevel
          energyRechargeLevel
          tapBotLevel
          currentBoss {
            _id
            level
            currentHealth
            maxHealth
            __typename
          }
          freeBoosts {
            _id
            currentTurboAmount
            maxTurboAmount
            turboLastActivatedAt
            turboAmountLastRechargeDate
            currentRefillEnergyAmount
            maxRefillEnergyAmount
            refillEnergyLastActivatedAt
            refillEnergyAmountLastRechargeDate
            __typename
          }
          bonusLeaderDamageEndAt
          bonusLeaderDamageStartAt
          bonusLeaderDamageMultiplier
          nonce
          __typename
        }
        """
    },
    "energy": {
        "operationName": "telegramGamePurchaseUpgrade",
        "variables": {"upgradeType": "EnergyCap"},
        "query": """
        mutation telegramGamePurchaseUpgrade($upgradeType: UpgradeType!) {
          telegramGamePurchaseUpgrade(type: $upgradeType) {
            ...FragmentBossFightConfig
            __typename
          }
        }
        fragment FragmentBossFightConfig on TelegramGameConfigOutput {
          _id
          coinsAmount
          currentEnergy
          maxEnergy
          weaponLevel
          energyLimitLevel
          energyRechargeLevel
          tapBotLevel
          currentBoss {
            _id
            level
            currentHealth
            maxHealth
            __typename
          }
          freeBoosts {
            _id
            currentTurboAmount
            maxTurboAmount
            turboLastActivatedAt
            turboAmountLastRechargeDate
            currentRefillEnergyAmount
            maxRefillEnergyAmount
            refillEnergyLastActivatedAt
            refillEnergyAmountLastRechargeDate
            __typename
          }
          bonusLeaderDamageEndAt
          bonusLeaderDamageStartAt
          bonusLeaderDamageMultiplier
          nonce
          __typename
        }
        """
    },
    "recharging": {
        "operationName": "telegramGamePurchaseUpgrade",
        "variables": {"upgradeType": "EnergyRechargeRate"},
        "query": """
        mutation telegramGamePurchaseUpgrade($upgradeType: UpgradeType!) {
          telegramGamePurchaseUpgrade(type: $upgradeType) {
            ...FragmentBossFightConfig
            __typename
          }
        }
        fragment FragmentBossFightConfig on TelegramGameConfigOutput {
          _id
          coinsAmount
          currentEnergy
          maxEnergy
          weaponLevel
          energyLimitLevel
          energyRechargeLevel
          tapBotLevel
          currentBoss {
            _id
            level
            currentHealth
            maxHealth
            __typename
          }
          freeBoosts {
            _id
            currentTurboAmount
            maxTurboAmount
            turboLastActivatedAt
            turboAmountLastRechargeDate
            currentRefillEnergyAmount
            maxRefillEnergyAmount
            refillEnergyLastActivatedAt
            refillEnergyAmountLastRechargeDate
            __typename
          }
          bonusLeaderDamageEndAt
          bonusLeaderDamageStartAt
          bonusLeaderDamageMultiplier
          nonce
          __typename
        }
        """
    }
}


def clear_console():
    # Clear the console based on the operating system
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def animate_energy_recharge(duration):
    frames = ["|", "/", "-", "\\"]
    end_time = time.time() + duration
    while time.time() < end_time:
        for frame in frames:
            print(f"\r🪫 Recharging energy {frame}", end="", flush=True)
            time.sleep(0.25)
    print("\r🔋 Energy recharge complete. ", flush=True)


tap_counts = {}
def perform_upgrade(upgrade_type, headers):
    global upgrade_interval
    upgrade_success = True

    while upgrade_success:
        print(f"⏫ Upgrading {upgrade_type}... ", end="", flush=True)
        time.sleep(1)

        response = requests.post(url, json=upgrade_payloads[upgrade_type], headers=headers)
        response_data = response.json()

        if response.status_code == 200 and 'errors' not in response_data:
            print(f"\r✅ Sukses upgrade {upgrade_type}                ")  # Spasi tambahan untuk menimpa teks sebelumnya jika perlu
        elif 'errors' in response_data:
            upgrade_success = False
            error_message = response_data['errors'][0]['message']
            if "You don't have enough coins to purchase this upgrade" in error_message:
                print(f"\r❌ Gagal upgrade {upgrade_type}: Koin tidak cukup.")
                # upgrade_success = False
            elif "max upgrade level reached" in error_message:
                print(f"\r❌ Gagal upgrade {upgrade_type}: Level upgrade max.")
                # upgrade_success = False  # Stop upgrading if max level reached
            elif "Unexpected error value" in error_message:
                # upgrade_success = False
                ms_before_next = int(response_data['errors'][0]['message'].split('msBeforeNext:')[1].split(',')[0].strip())
                hours = ms_before_next // 3600000
                minutes = (ms_before_next % 3600000) // 60000
                print(f"\r❌ Gagal upgrade {upgrade_type}: Upgrade berikutnya dalam: {hours} jam {minutes} menit")
                if hours > 0 or minutes > 0:
                    upgrade_interval = 100
            else:
                print(f"\r❌ Gagal upgrade {upgrade_type}, error: {response_data}")
                upgrade_success = False  # Stop upgrading on other errors
        else:
            print(f"\r❌ Gagal upgrade {upgrade_type}, status code: {response.status_code}")
            upgrade_success = False  # Stop upgrading on failed status code




def activate_energy_recharge_booster(headers):
    response_config = requests.post(url, json=cek_stat, headers=headers)
    config_data = response_config.json()['data']['telegramGameGetConfig']
    current_refill_amount = config_data['freeBoosts']['currentRefillEnergyAmount']
 
    if current_refill_amount > 0:
        recharge_booster_payload = {
            "operationName": "telegramGameActivateBooster",
            "variables": {"boosterType": "Recharge"},
            "query": """
            mutation telegramGameActivateBooster($boosterType: BoosterType!) {
              telegramGameActivateBooster(boosterType: $boosterType) {
                ...FragmentBossFightConfig
                __typename
              }
            }
            fragment FragmentBossFightConfig on TelegramGameConfigOutput {
              _id
              coinsAmount
              currentEnergy
              maxEnergy
              weaponLevel
              energyLimitLevel
              energyRechargeLevel
              tapBotLevel
              currentBoss {
                _id
                level
                currentHealth
                maxHealth
                __typename
              }
              freeBoosts {
                _id
                currentTurboAmount
                maxTurboAmount
                turboLastActivatedAt
                turboAmountLastRechargeDate
                currentRefillEnergyAmount
                maxRefillEnergyAmount
                refillEnergyLastActivatedAt
                refillEnergyAmountLastRechargeDate
                __typename
              }
              bonusLeaderDamageEndAt
              bonusLeaderDamageStartAt
              bonusLeaderDamageMultiplier
              nonce
              __typename
            }
            """
        }
        response = requests.post(url, json=recharge_booster_payload, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            if response_data and 'data' in response_data and response_data['data'] and 'telegramGameActivateBooster' in response_data['data']:
                new_energy = response_data['data']['telegramGameActivateBooster']['currentEnergy']
                print(f"\n🔋 Energi terisi. Energi saat ini: {new_energy}")
            else:
                print("❌ Gagal mengaktifkan Recharge Booster: Data tidak lengkap atau tidak ada.")
        else:
            print("❌ Gagal mengaktifkan Recharge Booster.")
    else:
        print("❌ Kondisi tidak memenuhi untuk mengaktifkan Recharge Booster.")


turbo_activated = False
def activate_turbo_boost(headers):
    # Memeriksa konfigurasi game untuk mendapatkan jumlah turbo saat ini
    global turbo_activated
    print(f"Turbo Status: {turbo_activated}"  )
    print("\n🚀 Mengaktifkan Turbo Boost ... ", end="", flush=True)
    
    response_config = make_request(url, headers, cek_stat)
    config_data = response_config.json()['data']['telegramGameGetConfig']
    current_turbo = config_data['freeBoosts']['currentTurboAmount']
    
    if current_turbo > 0:
        booster_payload = {
            "operationName": "telegramGameActivateBooster",
            "variables": {"boosterType": "Turbo"},
            "query": """
            mutation telegramGameActivateBooster($boosterType: BoosterType!) {
              telegramGameActivateBooster(boosterType: $boosterType) {
                ...FragmentBossFightConfig
                __typename
              }
            }
            fragment FragmentBossFightConfig on TelegramGameConfigOutput {
              _id
              coinsAmount
              currentEnergy
              maxEnergy
              weaponLevel
              energyLimitLevel
              energyRechargeLevel
              tapBotLevel
              currentBoss {
                _id
                level
                currentHealth
                maxHealth
                __typename
              }
              freeBoosts {
                _id
                currentTurboAmount
                maxTurboAmount
                turboLastActivatedAt
                turboAmountLastRechargeDate
                currentRefillEnergyAmount
                maxRefillEnergyAmount
                refillEnergyLastActivatedAt
                refillEnergyAmountLastRechargeDate
                __typename
              }
              bonusLeaderDamageEndAt
              bonusLeaderDamageStartAt
              bonusLeaderDamageMultiplier
              nonce
              __typename
            }
            """
        }
        if turbo_activated == False:
            response = make_request(url, headers, booster_payload)
            turbo_activated = True
            if response.status_code == 200:
                response_data = response.json()

                current_health = response_data['data']['telegramGameActivateBooster']['currentBoss']['currentHealth']
                if current_health == 0:
                    print("\nBos telah dikalahkan, mengatur bos berikutnya...")
                    set_next_boss(headers)
                    activate_turbo_boost(headers)
                else:
                    turbo_last_activated_at = response_data['data']['telegramGameActivateBooster']['freeBoosts']['turboLastActivatedAt']
                    # Mengonversi waktu ke UTC+7
                    utc_time = datetime.strptime(turbo_last_activated_at, "%Y-%m-%dT%H:%M:%S.%fZ")
                    local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Jakarta'))
                    formatted_time = local_time.strftime("%Y-%m-%d %H:%M:%S")
                    print(f"\n🚀 Turbo terakhir diaktifkan pada: {formatted_time}")
                    # Mengubah tapsCount menjadi 500 dan melakukan 5x taps tanpa jeda
                    tap_payload['variables']['payload']['tapsCount'] = 5000
                    for _ in range(20):
                        
                        tap_response = make_request(url, headers, tap_payload)
                        if tap_response.status_code == 200:
                            tap_data = tap_response.json()['data']['telegramGameProcessTapsBatch']
                            if tap_data['currentBoss']['currentHealth'] == 0:
                              print("\nBos telah dikalahkan, mengatur bos berikutnya...")
                              set_next_boss(headers)
                              activate_turbo_boost(headers)
                            print(f"✅ Tapped. Coins 🪙: {tap_data['coinsAmount']}, Monster ⚔️: {tap_data['currentBoss']['currentHealth']} - {tap_data['currentBoss']['maxHealth']}")

                        else:
                            print("❌ Gagal melakukan tapping.")
            else:
                print("❌ Gagal mengaktifkan Turbo Boost.")
                tap_payload['variables']['payload']['tapsCount'] = 5000
                for _ in range(10):             
                        tap_response = make_request(url, headers, tap_payload)
                        if tap_response.status_code == 200:
                            tap_data = tap_response.json()['data']['telegramGameProcessTapsBatch']
                            if tap_data['currentBoss']['currentHealth'] == 0:
                              print("\nBos telah dikalahkan, mengatur bos berikutnya...")
                              set_next_boss(headers)
                              activate_turbo_boost(headers)
                            print(f"✅ Tapped. Coins 🪙: {tap_data['coinsAmount']}, Monster ⚔️: {tap_data['currentBoss']['currentHealth']} - {tap_data['currentBoss']['maxHealth']}")
                        else:
                            print("❌ Gagal melakukan tapping.")

        else:
            print("❌ Turbo boost sudah diaktifkan.")


        
    else:
        print("❌ Turbo Boost tidak tersedia.")

def set_next_boss(headers):
    next_boss_payload = {
        "operationName": "telegramGameSetNextBoss",
        "variables": {},
        "query": """
        mutation telegramGameSetNextBoss {
          telegramGameSetNextBoss {
            ...FragmentBossFightConfig
            __typename
          }
        }
        fragment FragmentBossFightConfig on TelegramGameConfigOutput {
          _id
          coinsAmount
          currentEnergy
          maxEnergy
          weaponLevel
          energyLimitLevel
          energyRechargeLevel
          tapBotLevel
          currentBoss {
            _id
            level
            currentHealth
            maxHealth
            __typename
          }
          freeBoosts {
            _id
            currentTurboAmount
            maxTurboAmount
            turboLastActivatedAt
            turboAmountLastRechargeDate
            currentRefillEnergyAmount
            maxRefillEnergyAmount
            refillEnergyLastActivatedAt
            refillEnergyAmountLastRechargeDate
            __typename
          }
          bonusLeaderDamageEndAt
          bonusLeaderDamageStartAt
          bonusLeaderDamageMultiplier
          nonce
          __typename
        }
        """
    }
    next_boss_response = requests.post(url, json=next_boss_payload, headers=headers)
    if next_boss_response.status_code == 200:
        print("✅ Berhasil ganti bos.", flush=True)
    else:
        print("❌ Gagal ganti bos.", flush=True)

# Dictionary global untuk menyimpan status penyelesaian tugas setiap akun
tasks_completed = {}
def check_and_complete_tasks(account_number, headers):
    if tasks_completed.get(account_number, False):
        # print(f"[ Akun {account_number + 1} ] Semua tugas telah selesai. Tidak perlu cek lagi. ✅")
        return True
    task_list_payload = {
        "operationName": "GetTasksList",
        "variables": {"campaignId": "50ef967e-dd9b-4bd8-9a19-5d79d7925454"},
        "query": """
        fragment FragmentCampaignTask on CampaignTaskOutput {
          id
          name
          description
          status
          type
          position
          buttonText
          coinsRewardAmount
          link
          userTaskId
          isRequired
          iconUrl
          __typename
        }

        query GetTasksList($campaignId: String!) {
          campaignTasks(campaignConfigId: $campaignId) {
            ...FragmentCampaignTask
            __typename
          }
        }
        """
    }
    response = requests.post(url, json=task_list_payload, headers=headers)
    tasks = response.json()['data']['campaignTasks']
    all_completed = all(task['status'] == 'Completed' for task in tasks)
    
    if all_completed:
        tasks_completed[account_number] = True
        print(f"\n[ Akun {account_number + 1} ] Semua tugas telah selesai. ✅")
        return  True# Keluar dari fungsi jika semua tugas telah selesai

    
    print(f"\n[ Akun {account_number + 1} ]\nList Task:\n")
    for task in tasks:
        print(f"{task['name']} | {task['status']}")

        if task['name'] == "Follow telegram channel" and task['status'] == "Pending":
            print(f"⏩ Skipping task: {task['name']}")
            continue  # Skip task jika nama task adalah "Follow telegram channel" dan statusnya "Pending"

        if task['status'] == "Pending":
            # Melihat detail tugas
            print(f"\r🔍 Viewing task: {task['name']}", end="", flush=True)
            view_task_payload = {
                "operationName": "GetTaskById",



                "variables": {"taskId": task['id']},
                "query": """
                fragment FragmentCampaignTask on CampaignTaskOutput {
                  id
                  name
                  description
                  status
                  type
                  position
                  buttonText
                  coinsRewardAmount
                  link
                  userTaskId
                  isRequired
                  iconUrl
                  __typename
                }

                query GetTaskById($taskId: String!) {
                  campaignTaskGetConfig(taskId: $taskId) {
                    ...FragmentCampaignTask
                    __typename
                  }
                }
                """
            }
            view_response = requests.post(url, json=view_task_payload, headers=headers)
           
            if view_response.status_code != 200 or 'data' not in view_response.json():
                print(f"\r❌ Gagal mendapatkan detail task: {task['name']}")
                continue  # Skip ke task berikutnya jika terjadi kesalahan
            view_result = view_response.json()
            if 'errors'  in view_result:
                print(f"\r❌ Gagal mendapatkan detail task: {task['name']}")
                # continue  # Skip ke task berikutnya jika terjadi kesalahan
            else:
                task_details = view_result['data']['campaignTaskGetConfig']
                print(f"\r🔍 Detail Task: {task_details['name']}", end="", flush=True)


            time.sleep(2)  # Jeda 5 detik setelah melihat detail

            print(f"\r🔍 Verifikasi task: {task['name']}                                                                ", end="", flush=True)
            # Memindahkan tugas ke verifikasi
            verify_task_payload = {


                "operationName": "CampaignTaskToVerification",
                "variables": {"userTaskId": task['userTaskId']},
                "query": """
                fragment FragmentCampaignTask on CampaignTaskOutput {
                  id
                  name
                  description
                  status
                  type
                  position
                  buttonText
                  coinsRewardAmount
                  link
                  userTaskId
                  isRequired
                  iconUrl
                  __typename
                }

                mutation CampaignTaskToVerification($userTaskId: String!) {
                  campaignTaskMoveToVerification(userTaskId: $userTaskId) {
                    ...FragmentCampaignTask
                    __typename
                  }
                }
                """
            }
            verify_response = requests.post(url, json=verify_task_payload, headers=headers)
            verify_result = verify_response.json()
            
            if 'errors' not in verify_result:
                print(f"\r✅ {task['name']} | Moved to Verification", flush=True)
            else:
                print(f"\r❌ {task['name']} | Failed to move to Verification", flush=True)
            time.sleep(2)  # Jeda 5 detik setelah verifikasi

    # Cek ulang task setelah memindahkan ke verification
    response = requests.post(url, json=task_list_payload, headers=headers)
    updated_tasks = response.json()['data']['campaignTasks']
    print("\nUpdated Task List After Verification:\n")
    for task in updated_tasks:
        print(f"{task['name']} | {task['status']}")
        if task['status'] == "Verification":
            # Menyelesaikan tugas yang telah diverifikasi
            print(f"\r🔥 Menyelesaikan task: {task['name']}", end="", flush=True)
            complete_task_payload = {
                "operationName": "CampaignTaskCompleted",

                "variables": {"userTaskId": task['userTaskId']},
                "query": """
                fragment FragmentCampaignTask on CampaignTaskOutput {
                  id
                  name
                  description
                  status
                  type
                  position
                  buttonText
                  coinsRewardAmount
                  link
                  userTaskId
                  isRequired
                  iconUrl
                  __typename
                }

                mutation CampaignTaskCompleted($userTaskId: String!) {
                  campaignTaskMarkAsCompleted(userTaskId: $userTaskId) {
                    ...FragmentCampaignTask
                    __typename
                  }
                }
                """
            }
            complete_response = requests.post(url, json=complete_task_payload, headers=headers)
            complete_result = complete_response.json()
            if 'errors' not in complete_result:
                print(f"\r✅ {task['name']} | Completed                         ", flush=True)
            else:
                print(f"\r❌ {task['name']} | Failed to complete            ", flush=True)

                print(complete_result)
            time.sleep(3)  # Jeda 5 detik setelah menyelesaikan tugas
    return False

tap_count = 0


def animate_energy_recharge(duration):
    frames = ["|", "/", "-", "\\"]
    end_time = time.time() + duration
    while time.time() < end_time:
        remaining_time = int(end_time - time.time())
        for frame in frames:
            print(f"\r🪫 Mengisi ulang energi {frame} - Tersisa {remaining_time} detik         ", end="", flush=True)
            time.sleep(0.25)
    print("\r🔋 Pengisian energi selesai.                            ", flush=True)

printed_user_details = {}

def print_user_details_once(tokens):
    for index, token in enumerate(tokens):
        print(f"\r ⏳ Pengecekan akun {index + 1}...", end="", flush=True)
        time.sleep(1.5)
        user_data = check_token_validity(token)
        if not user_data:
            print(f"\r❌ Akun {index + 1} | Token tidak valid.", flush=True)
        else:
            first_name = user_data['firstName']

            last_name = user_data['lastName']
            league = user_data['league']
            print(f"\r✅ [ Akun {first_name} {last_name} ] | League 🏆 {league}", flush=True)
            printed_user_details[index] = True



def perform_operations(account_number, token, auto_upgrade, auto_booster):
    user_data = check_token_validity(token)
    
    if user_data is None:
        print(f"\r❌ Akun {account_number + 1} | Token tidak valid.", flush=True)
        return
    first_name = user_data.get('firstName', 'Unknown')
    last_name = user_data.get('lastName', 'Unknown')

    
  
    global tap_count, upgrade_interval, turbo_activated
    turbo_activated = False
       # Reset tap_count untuk akun ini jika belum ada
    if account_number not in tap_counts:
        tap_counts[account_number] = 0

    token = tokens[account_number % len(tokens)]
    headers = {
        "Accept" : "*/*",
        "Content-Length": "1035",
        "Content-Type": "application/json",
        "Priority": "u=1, i",
        "Authorization": f"Bearer {token}",
        "Origin": "https://tg-app.memefi.club",
        "Referer": "https://tg-app.memefi.club/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Sec-Ch-Ua": "Google Chrome;v=\"125\", Chromium;v=\"125\", Not.A/Brand;v=\"24\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "Windows",
        "Sec-Fetch-Dest" : "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
    }


    check_and_complete_tasks(account_number,headers)

    while True:
          # clear_console()
          response_config = make_request(url, headers, cek_stat)
          config_data = response_config.json()['data']['telegramGameGetConfig']
          tap_counts[account_number] += 1  # Menambah tap_count untuk akun ini

      
          output = (
              f"\n============\n"
              f"[ Akun {account_number + 1} - {first_name} {last_name} ]\n"
              f"Coin 🪙 {config_data['coinsAmount']} 🔋 {config_data['currentEnergy']} - {config_data['maxEnergy']}\n"
              f"Level 🔫 {config_data['weaponLevel']} 🔋 {config_data['energyLimitLevel']} ⚡ {config_data['energyRechargeLevel']} 🤖 {config_data['tapBotLevel']}\n"
              f"Boss 👾 {config_data['currentBoss']['level']} ❤️ {config_data['currentBoss']['currentHealth']} - {config_data['currentBoss']['maxHealth']}\n"

              f"Free 🚀 {config_data['freeBoosts']['currentTurboAmount']} 🔋 {config_data['freeBoosts']['currentRefillEnergyAmount']}\n"
          )


          print(output, end="", flush=True)
          print("\rTapping 👆", end="", flush=True)
          # Ambil nilai currentEnergy dan weaponLevel dari config_data
          
          energy_sekarang = config_data['currentEnergy']
          energy_used = energy_sekarang - 100
          damage = config_data['weaponLevel']+1
          # Hitung total_tap dengan pembagian bulat

          total_tap = energy_used // damage

          if total_tap < 5:
            if energy_sekarang < 200:
              if auto_booster == 'y':
                if config_data['freeBoosts']['currentRefillEnergyAmount'] > 0:
                  print("\r🪫 Energy Habis, mengaktifkan Recharge Booster... \n", end="", flush=True)
                  activate_energy_recharge_booster(headers)
                  continue  # Lanjutkan tapping setelah recharge
                else:
                  print("\r🪫 Energy Habis, tidak ada booster tersedia. Beralih ke akun berikutnya.\n", flush=True)
                  break
              break
            else:
                break

      


         
          # print(f"Total tap: {total_tap}")
          tap_payload['variables']['payload']['tapsCount'] = total_tap
   
          tap_request = make_request(url, headers, tap_payload)          
          hasil = tap_request.json()
          data_game = hasil['data']['telegramGameProcessTapsBatch']
          current_energy = data_game['currentEnergy']
          current_health = data_game['currentBoss']['currentHealth']
          
          if auto_booster == 'y':
            if config_data['freeBoosts']['currentTurboAmount'] > 0:
                activate_turbo_boost(headers)
          if current_health == 0:
            print("\nBos telah dikalahkan, mengatur bos berikutnya...", flush=True)
            next_boss_payload = {
                "operationName": "telegramGameSetNextBoss",
                "variables": {},
                "query": """
                mutation telegramGameSetNextBoss {
                  telegramGameSetNextBoss {
                    ...FragmentBossFightConfig
                    __typename
                  }
                }

                fragment FragmentBossFightConfig on TelegramGameConfigOutput {
                  _id
                  coinsAmount
                  currentEnergy
                  maxEnergy
                  weaponLevel
                  energyLimitLevel
                  energyRechargeLevel
                  tapBotLevel
                  currentBoss {
                    _id
                    level
                    currentHealth
                    maxHealth
                    __typename
                  }
                  freeBoosts {
                    _id
                    currentTurboAmount
                    maxTurboAmount
                    turboLastActivatedAt
                    turboAmountLastRechargeDate
                    currentRefillEnergyAmount
                    maxRefillEnergyAmount
                    refillEnergyLastActivatedAt
                    refillEnergyAmountLastRechargeDate
                    __typename
                  }
                  bonusLeaderDamageEndAt
                  bonusLeaderDamageStartAt
                  bonusLeaderDamageMultiplier
                  nonce
                  __typename
                }
                """
            }
            next_boss_response = requests.post(url, json=next_boss_payload, headers=headers)
            if next_boss_response.status_code == 200:
                print("✅ Berhasil ganti bos.", flush=True)
            else:
                print("❌ Gagal ganti bos.", flush=True)




          # if current_energy < 200:
          #   if auto_booster == 'y':
          #     if config_data['freeBoosts']['currentRefillEnergyAmount'] > 0:
          #         print("\r🪫 Energy Habis, mengaktifkan Recharge Booster... \n", end="", flush=True)
          #         activate_energy_recharge_booster(headers)
          #         continue  # Lanjutkan tapping setelah recharge
          #     else:
          #         print("\r🪫 Energy Habis, tidak ada booster tersedia. Beralih ke akun berikutnya.\n", flush=True)
          #         break
          #   else:

          #       # if auto_booster == 'y':
          #       #     print("\r🪫 Energy Habis, tidak ada booster tersedia. Beralih ke akun berikutnya.\n", flush=True)
          #   # else:
          #     print("\r🪫 Energy Habis, Beralih ke akun berikutnya.\n", flush=True)
          #     break  # Keluar dari loop jika tidak ada booster dan energi habis

          # tap_request = make_request(url, headers, tap_payload)
          tap_count += 1
        
          if tap_request.status_code != 200:
              print("\r❌ Gagal Tapping", flush=True)
              break  # Keluar dari loop jika terjadi error saat tapping
          else:
            print(f"\rTapped ✅\n ")


          if auto_upgrade == 'y' and tap_count % upgrade_interval == 0:
            perform_upgrade("wp", headers)
            perform_upgrade("energy", headers)
            perform_upgrade("recharging", headers)

    
def check_token_validity(token):
    url = "https://api-gw-tg.memefi.club/graphql"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    query_payload = {
        "operationName": "QueryTelegramUserMe",
        "variables": {},
        "query": """
        query QueryTelegramUserMe {
          telegramUserMe {
            firstName
            lastName
            telegramId
            username
            referralCode
            isDailyRewardClaimed
            referral {
              username
              lastName
              firstName
              bossLevel
              coinsAmount
              __typename
            }
            isReferralInitialJoinBonusAvailable
            league
            leagueIsOverTop10k
            leaguePosition
            _id
            __typename
          }
        }
        """
    }
    response = requests.post(url, json=query_payload, headers=headers)
    if response.status_code == 200:
        user_data = response.json()['data']['telegramUserMe']
        return user_data
    else:
        return None

# Mengambil input dari pengguna untuk konfigurasi upgrade otomatis
while True:
    auto_upgrade = input("Upgrade Otomatis (default y) ? (y/n): ").strip().lower()
    if auto_upgrade in ['y', 'n', '']:
        auto_upgrade = auto_upgrade or 'y'
        break
    else:
        print("Masukkan 'y' atau 'n'.")

upgrade_interval = 10  # Default jeda upgrade
if auto_upgrade == 'y':
    while True:
        try:
            upgrade_interval_input = input("Jeda Upgrade tiap Tap (default 10)? ").strip()
            upgrade_interval = int(upgrade_interval_input) if upgrade_interval_input else 10
            break
        except ValueError:
            print("Masukkan angka yang valid.")

# Mengambil input dari pengguna untuk penggunaan booster otomatis
while True:
    auto_booster = input("Auto use booster (default n)? (y/n): ").strip().lower()
    if auto_booster in ['y', 'n', '']:
        auto_booster = auto_booster or 'n'
        break
    else:
        print("Masukkan 'y' atau 'n'.")

while True:
    try:
        jeda_energi_input = input("Jeda pengisian energi (default 10)? ").strip()
        jeda_energi = int(jeda_energi_input) if jeda_energi_input else 10
        break
    except ValueError:
        print("Masukkan angka yang valid.")


print_user_details_once(tokens)
while True:

    for index, token in enumerate(tokens):
        perform_operations(index, token, auto_upgrade, auto_booster)
    
    clear_console()

    animate_energy_recharge(jeda_energi)  # Tunggu selama 5 detik sebelum memulai siklus berikutnya



