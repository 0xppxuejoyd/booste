import os
import requests
import uuid
import random

# Define color codes
green = '\033[1;32m'  # Bold Green
red = '\033[1;31m'    # Bold Red
reset = '\033[0m'      # Reset

folder_name = "/sdcard/Test"
file_names = ["toka.txt", "tokaid.txt", "tokp.txt", "tokpid.txt", "cok.txt", "cokid.txt"]

if not os.path.exists(folder_name):
    os.makedirs(folder_name, exist_ok=True)
    print(f"{green}Folder '{folder_name}' created.{reset}")

for file_name in file_names:
    file_path = os.path.join(folder_name, file_name)
    open(file_path, 'a').close()  # Ensures the file exists
    print(f"{green}File '{file_path}' checked/created.{reset}")

def count_lines(filepath):
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                return sum(1 for _ in file)
        else:
            return 0
    except Exception as e:
        print(f"{red}Error counting lines in {filepath}: {e}{reset}")
        return 0

def overview():
    print(f"\033[1;96m  ━━━━━━━━━━━━━━━━━━━━[{red}OVERVIEW{reset}]━━━━━━━━━━━━━━━━━━━━━━")
    total_accounts = count_lines("/sdcard/Test/toka.txt")
    total_pages = count_lines("/sdcard/Test/tokp.txt")
    print(f"  {red}TOTAL ACCOUNTS: {reset}{total_accounts}{red} | TOTAL PAGES: {reset}{total_pages} {red}")
    print(f'{reset}  ════════════════════════════════════════════════════════════')

def Initialize():
    print(f"  Please choose how you want to Extract.\n")
    print(f"     1. Manual through input")
    print(f"     2. Manual through File")
    print(f"     3. Automatic through File")
    print(f"     4. Overview")

    choice = input('   Choose: ')
    if choice == '1':
        Manual()
    elif choice == '2':
        ManFile()
    elif choice == '3':
        Auto()
    elif choice == '4':
        overview()
    else:
        print(f"{red}Invalid option.{reset}")
        Initialize()

def Manual():
    user_choice = input(" Input y or leave blank if it's an account. If it's a page then input n (y/N/d): ")
    user = input("USER ID/EMAIL: ")
    passw = input("PASSWORD: ")
    cuser(user, passw, user_choice)

def ManFile():
    file_path = input('Put file path: ')
    if os.path.isfile(file_path):
        try:
            user_choice = input(" Input y or leave blank if it's an account. If it's a page, input n (y/N/d): ")
            with open(file_path, 'r') as file:
                for line in file:
                    user_pass = line.strip().split('|')
                    process_users([user_pass], user_choice)
        except Exception as e:
            print(f'{red}Error reading the file: {e}{reset}')
    else:
        print(f'{red}File location not found.{reset}')

def Auto():
    directory = '/sdcard'
    txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]

    if not txt_files:
        print(f'{red}No .txt files found in {directory}{reset}')
        return

    for i, filename in enumerate(txt_files, start=1):
        print(f"    {i}. {filename}")

    try:
        choice = int(input('Choose: '))
        if 1 <= choice <= len(txt_files):
            selected_file = os.path.join(directory, txt_files[choice - 1])
            if os.path.isfile(selected_file):
                user_choice = input(" Input y or leave blank if it's an account. If it's a page, input n (y/N/d): ")
                with open(selected_file, 'r') as file:
                    for line in file:
                        user_pass = line.strip().split('|')
                        process_users([user_pass], user_choice)
            else:
                print(f'{red}File not found.{reset}')
        else:
            print(f'{red}Invalid option.{reset}')
    except ValueError:
        print(f'{red}Invalid input.{reset}')

def process_users(user_list, user_choice):
    for user_pass in user_list:
        if len(user_pass) == 2:
            user, passw = user_pass
            cuser(user, passw, user_choice)
        else:
            print(f"{red}Invalid format in line: {user_pass}{reset}")

def kyzer():
    android_version = f"{random.randint(5, 14)}.{random.randint(0, 9)}"
    fb_version = f"{random.randint(100, 999)}.0.0.{random.randint(10, 99)}.{random.randint(100, 999)}"
    
    models = ["Samsung", "Realme", "Oppo", "Vivo", "Xiaomi", "Huawei", "OnePlus", "Infinix", "Nokia", "Tecno"]
    model = random.choice(models) + f"-{random.randint(1000, 9999)}"

    ua = f"Mozilla/5.0 (Linux; Android {android_version}; {model}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{fb_version} Mobile Safari/537.36"
    return ua

def cuser(user, passw, user_choice):
    accessToken = '350685531728|62f8ce9f74b12f84c123cc23437a4a32'
    data = {
        'adid': str(uuid.uuid4()),
        'format': 'json',
        'device_id': str(uuid.uuid4()),
        'cpl': 'true',
        'family_device_id': str(uuid.uuid4()),
        'credentials_type': 'device_based_login_password',
        'email': user,
        'password': passw,
        'access_token': accessToken,
        'generate_session_cookies': '1',
        'locale': 'en_US',
        'method': 'auth.login',
        'fb_api_req_friendly_name': 'authenticate',
        'api_key': '62f8ce9f74b12f84c123cc23437a4a32',
    }
    headers = {
        'User-Agent': kyzer(),
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'b-api.facebook.com'
    }

    response = requests.post("https://b-api.facebook.com/method/auth.login", headers=headers, data=data, allow_redirects=False).json()

    if "session_key" in response:
        print(f"{green}Success: {user} extracted successfully.{reset}")

        cookie = ';'.join(f"{i['name']}={i['value']}" for i in response.get('session_cookies', []))
        c_user_value = next((i['value'] for i in response.get('session_cookies', []) if i['name'] == 'c_user'), None)

        if c_user_value:
            with open(f"/sdcard/Test/{'tokp' if user_choice.lower() in ['n', 'no'] else 'toka'}.txt", 'a') as f:
                f.write(f'{response["access_token"]}\n')
            with open(f"/sdcard/Test/{'tokpid' if user_choice.lower() in ['n', 'no'] else 'tokaid'}.txt", 'a') as f:
                f.write(f'{c_user_value}\n')
            with open('/sdcard/Test/cok.txt', 'a') as f:
                f.write(f'{cookie}\n')

    else:
        print(f"{red}Failed: {user} isn't extracted. Error: {response}{reset}")

Initialize()
