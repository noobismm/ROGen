import time
import random
import os
import threading

import concurrent.futures
import asyncio
from roblox import Client
from roblox import UserNotFound
from roblox.utilities.exceptions import InternalServerError
from roblox import InternalServerError

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

client = Client()

script_path = os.path.abspath(__file__)
file_path = os.path.join(os.path.dirname(script_path), 'ROBLOSECURITYS.txt')
print("Getting accounts...")
lines = open(file_path, 'r').readlines()


options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

def loginAccount(token):
    driver_path = 'chromedriver.exe'
    driver = webdriver.Chrome(driver_path, options=options)
    driver.get('https://www.roblox.com/login')

    username_box = driver.find_element('id', 'login-username') 
    password_box = driver.find_element('id', 'login-password')
    login_button = driver.find_element('id', 'login-button')

    wait = WebDriverWait(driver, 10)
    accept_cookies = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.btn-cta-lg.cookie-btn.btn-primary-md.btn-min-width')))

    accept_cookies.click()

    cookie = {
        'name': '.ROBLOSECURITY',
        'value': token,
        "domain": ".roblox.com"
    }


    driver.add_cookie(cookie)   

    driver.refresh()

    #input("Press Enter to log out..")
random_line = random.choice(lines)
random_line = random_line.strip()

tokens = []

with open(file_path, 'r') as file:
    for line in file:
        line = line.strip()
        tokens.append(line)
    #loginAccount(line)

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(loginAccount, tokens)


#loginAccount(random_line)
#
#loginAccount(token2)
