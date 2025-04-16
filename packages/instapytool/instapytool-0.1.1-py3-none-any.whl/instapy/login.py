import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from instapy.credentials import UserCredentials

def login_to_instagram(credentials: UserCredentials):
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service("D:\\Programs\\chrome\\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://www.instagram.com/")
    time.sleep(2)

    # Set cookies for session-based login
    driver.add_cookie({'name': 'sessionid', 'value': credentials.session_id, 'domain': '.instagram.com', 'path': '/'})
    driver.add_cookie({'name': 'ds_user', 'value': credentials.username, 'domain': '.instagram.com', 'path': '/'})
    driver.refresh()
    driver.refresh()
    time.sleep(5)

    return driver
