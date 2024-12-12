
# https://horace.io/OpenReviewExplorer/?conf=iclr2020&limit=1000000000
# https://horace.io/OpenReviewExplorer/?conf=iclr2019&limit=1000000000
# https://horace.io/OpenReviewExplorer/?conf=iclr2018&limit=1000000000
# https://horace.io/OpenReviewExplorer/?conf=iclr2017&limit=1000000000

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import requests


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



def extract_article_data(web_address): 
    source = requests.get(web_address).text

    soup = BeautifulSoup(source, 'html.parser')

    article = soup.find('div', class_='forum-container')

    #fetch title of article
    title = article.find('div', class_='title_pdf_row').h2.text


    fields = article.find_all("strong", class_="note-content-field")

    # fetch keywords, tldr and abstract
    for field in fields:
        if "Keywords" in field.get_text(strip=True):
            sibling = field.find_next_sibling("span", class_="note-content-value")
            if sibling:
                keywords_value = sibling.get_text(strip=True)
                keywords_value = keywords_value.replace(',', ';')
                
        elif "TL;DR" in field.get_text(strip=True):
            sibling = field.find_next_sibling("span", class_="note-content-value")
            if sibling:
                tldr_value = sibling.get_text(strip=True)
                
        elif "Abstract" in field.get_text(strip=True):
            sibling = field.find_next_sibling("span", class_="note-content-value")
            if sibling:
                abstract_value = sibling.get_text(strip=True)

    return title, keywords_value, tldr_value, abstract_value



