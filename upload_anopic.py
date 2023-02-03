from flask import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from proxy import get_chromedriver
import os
import time
import requests



def get_anopic_link(file_path):

    driver = get_chromedriver(use_proxy=True, user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15')

    driver.get("https://anopic.net/")
    
    driver.find_element(By.CLASS_NAME, "dz-hidden-input").send_keys(file_path)
    time.sleep(5)
    driver.find_element(By.XPATH, r'/html/body/main/div/div/div').click()
    time.sleep(3)

    anopic_link = ''

    while anopic_link == '':
        try:
            anopic_link = driver.find_element(By.XPATH, r'/html/body/div[2]/div/div/div[2]/p').text
        except:
            pass

    driver.close()
    driver.quit()

    print("[+] Anopic success")
    
    return anopic_link


print(get_anopic_link('temp_files/11.jpg'))