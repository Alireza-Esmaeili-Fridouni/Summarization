from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from itertools import chain
import pandas as pd

def fetch_links(url):
    chrome_driver_path = "./chromedriver.exe"
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service)

    driver.get(url=url)

    wait = WebDriverWait(driver, 20)
    tags = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, "/forum")]')))
    articles_adresses = [tag.get_attribute('href') for tag in tags]
    
    return articles_adresses


ref_address = 'https://openreview.net/group?id=ICLR.cc/2021/Conference#'
all_pages = ['oral-presentations', 'spotlight-presentations',
             'poster-presentations', 'withdrawn-rejected-submissions']

article_urls = [fetch_links(url=f"{ref_address}{page}") for page in all_pages]
article_urls = list(chain(*article_urls))

urls_dict = {'urls':article_urls}

iclr_2021_urls_df = pd.DataFrame(urls_dict)
iclr_2021_urls_df.to_csv('iclr_2021_urls_df.csv', index=False)     