from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from itertools import chain
import pandas as pd
import time


def fetch_links(url, id):
    chrome_driver_path = "./chromedriver.exe"
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service)


    driver.get(url=url)

    wait = WebDriverWait(driver, 15)

    isNextDisable = False 
    articles_adresses = []
    while not isNextDisable:
        try:
        
            links = wait.until(EC.presence_of_all_elements_located((By.XPATH, f'//*[@id="{id}"]//a[contains(@href, "/forum")]')))
            articles_adresses.extend([tag.get_attribute('href') for tag in links])
        
            # next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".pagination .right-arrow a")))
            
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, \
            f'//*[@id="{id}"]//ul[@class="pagination"]// \
            li[contains(@class, "right-arrow") and not(contains(@class, "disabled"))]/a')))
            
            next_button.click()
            time.sleep(3)
            
        except Exception as e:
            print(f"Stopping due to: {e}")
            isNextDisable = True

    return articles_adresses


chrome_driver_path = "./chromedriver.exe"
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)

# url of iclr 2022
# url = 'https://openreview.net/group?id=ICLR.cc/2022/Conference'

# url of iclr 2023
# url = 'https://openreview.net/group?id=ICLR.cc/2023/Conference'

# url of iclr 2024
url = 'https://openreview.net/group?id=ICLR.cc/2024/Conference'

# url of iclr 2025
# url = 'https://openreview.net/group?id=ICLR.cc/2025/Conference'

driver.get(url=url)

wait = WebDriverWait(driver, 15)

tags = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "tab-pane")]')))

tab_names = [tag.get_attribute('id') for tag in tags if tag.get_attribute('id') not in ['your-consoles', 'recent-activity']]

# reference addresse of iclr 2022 
# ref_address = 'https://openreview.net/group?id=ICLR.cc/2022/Conference#'

# reference addresse of iclr 2023 
# ref_address = 'https://openreview.net/group?id=ICLR.cc/2023/Conference#'

# reference addresse of iclr 2024 
ref_address = 'https://openreview.net/group?id=ICLR.cc/2024/Conference#tab-'

# reference addresse of iclr 2025 
# ref_address = 'https://openreview.net/group?id=ICLR.cc/2025/Conference#tab-'

article_urls = [fetch_links(url=f"{ref_address}{tab_name}", id=tab_name) for tab_name in tab_names]
article_urls = list(chain(*article_urls))

urls_dict = {'urls':article_urls}

# creating dataframe from iclr 2022
# iclr_2022_urls_df = pd.DataFrame(urls_dict)
# iclr_2022_urls_df.to_csv('urls/iclr_2022_urls_df.csv', index=False)

# creating dataframe from iclr 2023
# iclr_2023_urls_df = pd.DataFrame(urls_dict)
# iclr_2023_urls_df.to_csv('urls/iclr_2023_urls_df.csv', index=False)

# creating dataframe from iclr 2024
iclr_2024_urls_df = pd.DataFrame(urls_dict)
iclr_2024_urls_df.to_csv('urls/iclr_2024_urls_df.csv', index=False)

# creating dataframe from iclr 2025
# iclr_2025_urls_df = pd.DataFrame(urls_dict)
# iclr_2025_urls_df.to_csv('urls/iclr_2025_urls_df.csv', index=False)

