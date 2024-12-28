from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from itertools import chain
import pandas as pd
import time


def fetch_links(url):
    chrome_driver_path = "./chromedriver.exe"
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service)


    driver.get(url=url)

    wait = WebDriverWait(driver, 15)

    isNextDisable = False 
    articles_adresses = []
    while not isNextDisable:
        try:
        
            links = wait.until(EC.presence_of_all_elements_located((By.XPATH, f'//a[contains(@href, "/forum")]')))
            articles_adresses.extend([tag.get_attribute('href') for tag in links])
        
            # next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".pagination .right-arrow a")))
            
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, \
            f'//ul[@class="pagination"]//li[contains(@class, "right-arrow") and not(contains(@class, "disabled"))]/a')))
            
            next_button.click()
            time.sleep(3)
            
        except Exception as e:
            print(f"Stopping due to: {e}")
            isNextDisable = True

    return articles_adresses

url = 'https://openreview.net/submissions?page=1&venue=ICLR.cc%2F2024%2FConference'

article_urls = fetch_links(url=url)

urls_dict = {'urls':article_urls}

iclr_2024_urls_df = pd.DataFrame(urls_dict)
iclr_2024_urls_df.to_csv('urls/iclr_2024_urls_df.csv', index=False)