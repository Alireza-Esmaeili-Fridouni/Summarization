
# https://horace.io/OpenReviewExplorer/?conf=iclr2020&limit=1000000000
# https://horace.io/OpenReviewExplorer/?conf=iclr2019&limit=1000000000
# https://horace.io/OpenReviewExplorer/?conf=iclr2018&limit=1000000000
# https://horace.io/OpenReviewExplorer/?conf=iclr2017&limit=1000000000

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

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



