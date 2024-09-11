import subprocess
import time
import asyncio
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CHROME_DRIVER_PATH = 'YOUR CHROME DRIVER PATH!'
URL = "http://192.168.0.1"
USERNAME = "user"
PASSWORD = "YOUR PASSWORD!"
PING_HOST = "8.8.8.8"
PING_COUNT = 3 # pings wanting to be sent. You SHOULD recieve all of these pings.
WAIT_INTERVAL = 10 # The main wait time most things use.
MAX_MISSED_PINGS = 1 # Maximum pings lost.
IPMONKEY_URL = "https://ipmonkey.com" # Recommended since its unprotected.

def ping(host):
    result = subprocess.run(["ping", host, "-n", "1", "-w", "80"], capture_output=True, text=True)
    return result.returncode == 0

def check_ipmonkey():
    try:
        response = requests.get(IPMONKEY_URL, timeout=5)
        if response.status_code == 200:
            return True
    except requests.RequestException as e:
        return False

def wait_for_router():
    while not ping("192.168.0.1"):
        print(f"Router is not responding, retrying in {WAIT_INTERVAL} seconds...")
        time.sleep(WAIT_INTERVAL)
    print(f"Router is responsive, continuing.")
    time.sleep(7)

async def monitor_ping():
    missed_pings = 0
    time.sleep(1)
    wait_for_router()

    while True:
        ping_responsive = [ping(PING_HOST) for _ in range(PING_COUNT)]
        ipmonkey_loss = check_ipmonkey()
        
        if not any(ping_responsive) or not ipmonkey_loss:
            missed_pings += 1
        else:
            missed_pings = 0
        
        if missed_pings >= MAX_MISSED_PINGS:
            print("Packetloss detected.")
            run_selenium_script()
            missed_pings = 0
            time.sleep(16)
            wait_for_router()

def run_selenium_script():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 10)

    def login():
        driver.get(URL)
        wait.until(EC.presence_of_element_located((By.ID, 'txtUser'))).send_keys(USERNAME)
        wait.until(EC.presence_of_element_located((By.ID, 'txtPwd'))).send_keys(PASSWORD)
        wait.until(EC.element_to_be_clickable((By.ID, 'btnLogin'))).send_keys(Keys.RETURN)

    def navigate_to_apn_settings():
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#internet_setting"]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#apn_setting"]'))).click()

    def set_default_profile():
        select_element = wait.until(EC.presence_of_element_located((By.NAME, 'profile')))
        select = Select(select_element)
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()='3internet']"))) # ALWAYS USES A PRIVATE PUBLIC FACIING IP ADDRESS
            select.select_by_value("three.co.uk")
            wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Set as default"]'))).click()
            time.sleep(2)
            select.select_by_value("3internet")
            time.sleep(4)
        except:
            wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()='three.co.uk']")))
            select.select_by_value("3internet")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Set as default"]'))).click()
    try:
        login()
        navigate_to_apn_settings()
        set_default_profile()
    finally:
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    asyncio.run(monitor_ping())