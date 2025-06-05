import os
import time
import random
import concurrent.futures

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set paths
script_path = os.path.abspath(__file__)
file_path = os.path.join(os.path.dirname(script_path), 'ROBLOSECURITYS.txt')

# Load all tokens
with open(file_path, 'r') as f:
    tokens = [line.strip() for line in f if line.strip()]

# Set Chrome options
options = Options()
options.add_experimental_option("detach", True)

def login_with_token(token):
    try:
        driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
        driver.get("https://www.roblox.com/")

        # Wait for page to load before setting cookies
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Add .ROBLOSECURITY cookie
        driver.add_cookie({
            'name': '.ROBLOSECURITY',
            'value': token,
            'domain': '.roblox.com',
            'path': '/',
            'secure': True,
            'httpOnly': True
        })

        # Navigate to homepage to trigger login
        driver.get("https://www.roblox.com/home")
        print(f"[+] Token used: {token[:15]}...")

        time.sleep(5)  # Keep session open
        driver.quit()

    except Exception as e:
        print(f"[!] Failed to login with token: {e}")

# Run in parallel
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(login_with_token, tokens)
