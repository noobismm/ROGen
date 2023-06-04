import os
import time
import concurrent.futures
import ctypes
import warnings

try:
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from pystyle import Colorate, Colors, Center
    from fake_useragent import UserAgent
except ModuleNotFoundError:
    print("Required modules not installed, installing now...")
    os.system("python -m pip install --upgrade pip")
    os.system("pip install selenium")
    os.system("pip install pystyle")
    os.system("pip install UserAgent"); os.system("pip install fake_useragent")
    print("Successfully installed required modules.")

default_password = "defaultpassword"

options = Options()

print(Center.XCenter(Colorate.Vertical(Colors.red_to_black, """

                    ██████╗░░█████╗░██████╗░██╗░░░░░░█████╗░██╗░░██╗  ░██████╗░███████╗███╗░░██╗
                    ██╔══██╗██╔══██╗██╔══██╗██║░░░░░██╔══██╗╚██╗██╔╝  ██╔════╝░██╔════╝████╗░██║
                    ██████╔╝██║░░██║██████╦╝██║░░░░░██║░░██║░╚███╔╝░  ██║░░██╗░█████╗░░██╔██╗██║
                    ██╔══██╗██║░░██║██╔══██╗██║░░░░░██║░░██║░██╔██╗░  ██║░░╚██╗██╔══╝░░██║╚████║
                    ██║░░██║╚█████╔╝██████╦╝███████╗╚█████╔╝██╔╝╚██╗  ╚██████╔╝███████╗██║░╚███║
                    ╚═╝░░╚═╝░╚════╝░╚═════╝░╚══════╝░╚════╝░╚═╝░░╚═╝  ░╚═════╝░╚══════╝╚═╝░░╚══╝

""")))

warnings.filterwarnings("ignore", category=DeprecationWarning)
script_path = os.path.abspath(__file__)
file_path = os.path.join(os.path.dirname(script_path), 'ROBLOSECURITYS.txt')
lines = open(file_path, 'r').readlines()

def writeTokentoFile(token):
    with open(file_path, "a") as file:
        line = f"\n{token}"  # Replace with your desired line
        file.write(line)

def createAccount(username):
    driver_path = 'chromedriver.exe'

    ua = UserAgent()
    userAgent = ua.random
    print(userAgent)
    options.add_argument(f'user-agent={userAgent}')

    driver = webdriver.Chrome(chrome_options=options, executable_path=r'driver_path')
    driver.get('https://www.roblox.com')


    username_box = driver.find_element('id', 'signup-username') 
    password_box = driver.find_element('id', 'signup-password')
    male_button = driver.find_element("id", "MaleButton")
    signup_button = driver.find_element('id', 'signup-button')

    wait = WebDriverWait(driver, 10)
    accept_cookies = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.btn-cta-lg.cookie-btn.btn-primary-md.btn-min-width')))

    accept_cookies.click()

    dropdown = Select(driver.find_element("id", "MonthDropdown"))
    dropdown.select_by_value("May") 
    
    dropdown2 = Select(driver.find_element("id", "DayDropdown"))
    dropdown2.select_by_value("05") 

    dropdown = Select(driver.find_element("id", "YearDropdown"))
    dropdown.select_by_value("2000") 

    username_box.clear()
    password_box.clear()

    male_button.click()

    username_box.send_keys(username)
    password_box.send_keys(default_password)

    signup_button.click()

    wait = WebDriverWait(driver, 1000)
    wait.until(EC.url_to_be('https://www.roblox.com/home'))

    driver.refresh()

    cookies = driver.get_cookies()

    token = "N/A"

    for cookie in cookies:
        if cookie['name'] == ".ROBLOSECURITY":
            token = cookie['value']
            break

    writeTokentoFile(token)
    input("Completed")

def create_account_table(num_accounts, account_name):
    account_table = []
    for i in range(num_accounts):
        account_table.append(f"{account_name}{i+1}")
    return account_table

def main():
    ctypes.windll.kernel32.SetConsoleTitleW("Roblox Account Generator")

    num_accounts = int(input(Center.XCenter("How many accounts do you want to create? ")))
    account_name = input(Center.XCenter("Name of account to create? "))

    usernames = create_account_table(num_accounts, account_name)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(createAccount, usernames)

main()