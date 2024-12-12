
# https://horace.io/OpenReviewExplorer/?conf=iclr2020&limit=1000000000
# https://horace.io/OpenReviewExplorer/?conf=iclr2019&limit=1000000000
# https://horace.io/OpenReviewExplorer/?conf=iclr2018&limit=1000000000
# https://horace.io/OpenReviewExplorer/?conf=iclr2017&limit=1000000000

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time


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
    
    # Check for the existence of the 'forum-container' element
    if not article:
        raise Exception(f"Error: 'forum-container' not found for {web_address}")

    
    title_element = article.find('div', class_='title_pdf_row')
    
    # Check for the existence of the 'title_pdf_row' element
    if not title_element or not title_element.h2:
        raise Exception(f"Error: Title not found for {web_address}")
    
    #fetch title of article
    title = title_element.h2.text

    fields = article.find_all("strong", class_="note-content-field")

    # set default value
    keywords_value = None
    tldr_value = None
    abstract_value = None
    
    # Fetch keywords, tldr, and abstract
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
    
    if not keywords_value:
        keywords_value = 'None'
    if not tldr_value:
        tldr_value = 'None'
    if not abstract_value:
        abstract_value = 'None'        

    return title, keywords_value, tldr_value, abstract_value



url = 'https://horace.io/OpenReviewExplorer/'
article_urls = fetch_article_links(url)

urls = []
titles = []
keywords = []
tldrs = []
abstracts = []

for address, counter in zip(article_urls, range(1, len(article_urls)+1)):
    
    title, keyword, tldr, abstract = extract_article_data(web_address=address)
    urls.append(address)
    titles.append(title)
    keywords.append(keyword)
    tldrs.append(tldr)
    abstracts.append(abstract)
    if counter % 30 == 0:
        time.sleep(60)
    
data_dict = {'urls':urls, 'titles':titles, 'keywords':keywords, 'tldrs':tldrs, 'abstracts':abstracts}

df = pd.DataFrame(data_dict)
df.to_csv('df.csv', index=False)
