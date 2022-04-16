from selenium import webdriver
import os


# Settings Chrome_driver

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(chrome_options=chrome_options)

# Settings data user

DATA_LOGIN = os.environ.get('LOGIN')
DATA_PASS = os.environ.get('PASS')

