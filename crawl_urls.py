from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from itertools import chain
import pandas as pd

def fetch_article_links(url):
    chrome_driver_path = "./chromedriver.exe"
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service)

    driver.get(url=url)
    
    tags = driver.find_elements(by='xpath', value='//a[contains(@href, "openreview.net")]')

    articles_adresses = [tag.get_attribute('href') for tag in tags]
    
    return articles_adresses


webpages = ['https://horace.io/OpenReviewExplorer/?conf=iclr2017&limit=1000000000',
           'https://horace.io/OpenReviewExplorer/?conf=iclr2018&limit=1000000000',
           'https://horace.io/OpenReviewExplorer/?conf=iclr2019&limit=1000000000',
           'https://horace.io/OpenReviewExplorer/?conf=iclr2020&limit=1000000000']



article_urls = [fetch_article_links(list_url) for list_url in webpages]
article_urls = list(chain(*article_urls))

urls_dict = {'urls':article_urls}

urls_df = pd.DataFrame(urls_dict)
urls_df.to_csv('urls_df.csv', index=False)