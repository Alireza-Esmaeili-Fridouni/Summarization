from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from itertools import chain
import pandas as pd

def fetch_article_links(url):
    chrome_driver_path = "./chromedriver.exe"
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service)

    driver.get(url=url)

    # //*[@class="list"]//tr
    # articles = driver.find_elements(by='xpath', value='//*[@class="list"]//tr')
    # //a[contains(@href, "openreview.net")]
    
    tags = driver.find_elements(by='xpath', value='//a[contains(@href, "openreview.net")]')

    articles_adresses = [tag.get_attribute('href') for tag in tags]
    
    return articles_adresses


# https://horace.io/OpenReviewExplorer/?conf=iclr2020&limit=1000000000
# https://horace.io/OpenReviewExplorer/?conf=iclr2019&limit=1000000000
# https://horace.io/OpenReviewExplorer/?conf=iclr2018&limit=1000000000
# https://horace.io/OpenReviewExplorer/?conf=iclr2017&limit=1000000000

webpages = ['https://horace.io/OpenReviewExplorer/?conf=iclr2017&limit=1000000000',
           'https://horace.io/OpenReviewExplorer/?conf=iclr2018&limit=1000000000',
           'https://horace.io/OpenReviewExplorer/?conf=iclr2019&limit=1000000000',
           'https://horace.io/OpenReviewExplorer/?conf=iclr2020&limit=1000000000']



# iclr_2017 = fetch_article_links(webpages[0])
# iclr_2018 = fetch_article_links(webpages[1])
# iclr_2019 = fetch_article_links(webpages[2])
# iclr_2020 = fetch_article_links(webpages[3])
# article_urls = iclr_2017 + iclr_2018 + iclr_2019 + iclr_2020

article_urls = [fetch_article_links(list_url) for list_url in webpages]
article_urls = list(chain(*article_urls))

urls_dict = {'urls':article_urls}

urls_df = pd.DataFrame(urls_dict)
urls_df.to_csv('urls_df.csv', index=False)