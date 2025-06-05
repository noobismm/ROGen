import os
import time
import concurrent.futures
import ctypes
import warnings
import requests

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select, WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from pystyle import Colorate, Colors, Center
    from fake_useragent import UserAgent
except ModuleNotFoundError:
    print("Installing required modules...")
    os.system("pip install selenium pystyle fake_useragent requests")
    exit("Please re-run the script after installation.")

# === CONFIG ===
default_password = "defaultpassword"
webhook_url = "https://discord.com/api/webhooks/1377366865252323430/_Id6scMVAqHO_f_l9mGFBfqpzwZ3mU_NYYxrpWtfuKLyg0TQ1p3m0vh5aOn6z7_lL4E4"  # Your webhook here

# === Browser Options ===
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")
warnings.filterwarnings("ignore", category=DeprecationWarning)

# === Token File Path ===
script_path = os.path.abspath(__file__)
file_path = os.path.join(os.path.dirname(script_path), 'ROBLOSECURITYS.txt')

# === Print Banner ===
print(Center.XCenter(Colorate.Vertical(Colors.red_to_black, """

                ██████╗░░█████╗░██████╗░██╗░░░░░░█████╗░██╗░░██╗  ░██████╗░███████╗███╗░░██╗
                ██╔══██╗██╔══██╗██╔══██╗██║░░░░░██╔══██╗╚██╗██╔╝  ██╔════╝░██╔════╝████╗░██║
                ██████╔╝██║░░██║██████╦╝██║░░░░░██║░░██║░╚███╔╝░  ██║░░██╗░█████╗░░██╔██╗██║
                ██╔══██╗██║░░██║██╔══██╗██║░░░░░██║░░██║░██╔██╗░  ██║░░╚██╗██╔══╝░░██║╚████║
                ██║░░██║╚█████╔╝██████╦╝███████╗╚█████╔╝██╔╝╚██╗  ╚██████╔╝███████╗██║░╚███║
                ╚═╝░░╚═╝░╚════╝░╚═════╝░╚══════╝░╚════╝░╚═╝░░╚═╝  ░╚═════╝░╚══════╝╚═╝░░╚══╝

""")))

# === Helper Functions ===
def writeTokentoFile(token):
    with open(file_path, "a") as file:
        file.write(f"\n{token}")

def send_to_webhook(username, token):
    data = {
        "embeds": [{
            "title": "✅ New Roblox Account Created",
            "color": 3066993,
            "fields": [
                {"name": "Username", "value": username, "inline": True},
                {"name": "Password", "value": default_password, "inline": True},
                {"name": "ROBLOSECURITY", "value": f"```{token}```", "inline": False}
            ]
        }]
    }
    try:
        requests.post(webhook_url, json=data)
    except Exception as e:
        print(f"[!] Webhook error: {e}")

def createAccount(username):
    ua = UserAgent()
    userAgent = ua.random
    options.add_argument(f'user-agent={userAgent}')

    service = Service('chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    driver.get('https://www.roblox.com')

    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "signup-username")))

        # Accept cookies
        try:
            cookie_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-cta-lg.cookie-btn.btn-primary-md.btn-min-width')))
            cookie_button.click()
        except: pass

        Select(driver.find_element(By.ID, "MonthDropdown")).select_by_value("May")
        Select(driver.find_element(By.ID, "DayDropdown")).select_by_value("05")
        Select(driver.find_element(By.ID, "YearDropdown")).select_by_value("2000")

        driver.find_element(By.ID, "signup-username").send_keys(username)
        driver.find_element(By.ID, "signup-password").send_keys(default_password)
        driver.find_element(By.ID, "MaleButton").click()
        driver.find_element(By.ID, "signup-button").click()

        wait.until(EC.url_to_be('https://www.roblox.com/home'))
        driver.refresh()

        cookies = driver.get_cookies()
        token = next((cookie['value'] for cookie in cookies if cookie['name'] == ".ROBLOSECURITY"), "N/A")

        writeTokentoFile(token)
        send_to_webhook(username, token)
        print(f"[+] Account '{username}' created and sent to webhook.")

    except Exception as e:
        print(f"[!] Error creating {username}: {e}")
    finally:
        driver.quit()

def create_account_table(num_accounts, base_name):
    return [f"{base_name}{i+1}" for i in range(num_accounts)]

def main():
    ctypes.windll.kernel32.SetConsoleTitleW("Roblox Account Generator")
    try:
        num_accounts = int(input(Center.XCenter("How many accounts do you want to create? ")))
        base_name = input(Center.XCenter("Base username? (e.g. 'TestAlt'): "))
        usernames = create_account_table(num_accounts, base_name)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(createAccount, usernames)

    except ValueError:
        print("Please enter a valid number.")
    except KeyboardInterrupt:
        print("\n[!] Script interrupted by user.")

main()
