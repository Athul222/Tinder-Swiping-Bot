from time import sleep
from dotenv import load_dotenv, dotenv_values
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

load_dotenv(override= True)

config = {
    **dotenv_values("Tinder swipping bot/.env.secret")
}

facebook_id = config['ID']
facebook_password = config['PASSWORD']

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options= chrome_options)
driver.get("https://tinder.com/")

sleep(2)
cookie_popup = driver.find_element(By.XPATH, value='//*[@id="u-1919424827"]/div/div[2]/div/div/div[1]/div[1]/button')
sleep(2)
cookie_popup.click()

sleep(3)
login_button = driver.find_element(By.XPATH, value='//*[@id="u-1919424827"]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a')
sleep(2)
login_button.click()

sleep(2)
more_options = driver.find_element(By.XPATH, value='//*[@id="u647161393"]/main/div/div/div[1]/div/div/div[2]/div[2]/span/button')
sleep(2)
more_options.click()

sleep(3)
facebook_signin_button = driver.find_element(By.XPATH, value='//*[@id="u647161393"]/main/div/div/div[1]/div/div/div[2]/div[2]/span/div[2]/button')
sleep(5)
facebook_signin_button.click()

# driver.window_handles  => return list of windows 
# tinder window[Base window]
sleep(2)
base_window = driver.window_handles[0]

# facebook window[2nd oppened window]
# switching the selenium driver to the fb window so we can log in fb
fb_login_window = driver.window_handles[1]
driver.switch_to.window(fb_login_window)
print(driver.title) # prints the title of current selenium controlled window 

# Login to fb
sleep(5)
email_field = driver.find_element(By.NAME, value='email')
email_field.send_keys(facebook_id)
password_field = driver.find_element(By.NAME, value='pass')
password_field.send_keys(facebook_password)
password_field.send_keys(Keys.ENTER)

# reverting back to the base window[tinder in our case]
driver.switch_to.window(base_window)
print(driver.title)

sleep(5)
allow_location_button = driver.find_element(By.XPATH, value='//*[@id="u647161393"]/main/div/div/div/div[3]/button[1]')
driver.implicitly_wait(2)
allow_location_button.click()
reject_notification_button = driver.find_element(By.XPATH, value='//*[@id="u647161393"]/main/div/div/div/div[3]/button[2]')
sleep(2)
reject_notification_button.click()

sleep(3)
for n in range(10):
    sleep(2)
    try:
        hit_like = driver.find_element(By.XPATH, value='//*[@id="u-1919424827"]/div/div[1]/div/div/main/div/div/div[1]/div/div[3]/div/div[4]/button')
        driver.implicitly_wait(2)
        hit_like.click()
    except ElementClickInterceptedException:
        try:
            match_popup = driver.find_element_by_css_selector(".itsAMatch a")
            match_popup.click()
        except NoSuchElementException:
            sleep(2)
        
sleep(4)
print("Like limit has reached. Upgrade to premium for unlimitted like per day!")
driver.quit()