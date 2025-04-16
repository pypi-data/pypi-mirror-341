import time
from fastapi import HTTPException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from instapy.login import login_to_instagram
from instapy.credentials import UserCredentials

class DMRequest(UserCredentials):
    target_username: str
    message: str

def send_dm(data: DMRequest):
    driver = login_to_instagram(data)

    try:
        driver.get(f"https://www.instagram.com/{data.target_username}/")
        time.sleep(5)

        # Click "Message"
        try:
            message_button = driver.find_element(By.XPATH, "//div[text()='Message']")
            message_button.click()
        except Exception:
            raise HTTPException(status_code=400, detail="Could not click Message button")

        time.sleep(5)

        # Dismiss "Turn on Notifications"
        try:
            wait = WebDriverWait(driver, 10)
            not_now_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Not Now')]")))
            not_now_btn.click()
            time.sleep(1)
        except TimeoutException:
            pass

        # Type & send message
        try:
            message_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='textbox' and @contenteditable='true']"))
            )
            message_box.click()
            time.sleep(1)
            message_box.send_keys(data.message)
            time.sleep(1)
            message_box.send_keys(Keys.ENTER)
        except Exception:
            raise HTTPException(status_code=500, detail="Failed to send the message")

        return {"status": "success", "message": "Message sent successfully."}

    finally:
        time.sleep(3)
        driver.quit()

