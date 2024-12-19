from bs4 import BeautifulSoup
import requests
import pandas as pd
import time



def extract_article_data(web_address): 
    try:
        source = requests.get(web_address).text
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {web_address}: {e}")
        return None, None, None, None

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
    one_sent_summ_value = None
    
    # Fetch keywords, tldr, abstract and one sentence summary
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
        
        elif "One-sentence Summary" in field.get_text(strip=True):
            sibling = field.find_next_sibling("span", class_="note-content-value")
            if sibling:
                one_sent_summ_value = sibling.get_text(strip=True)
    
    if not keywords_value:
        keywords_value = 'None'
    if not tldr_value:
        tldr_value = 'None'
    if not abstract_value:
        abstract_value = 'None'
    if not one_sent_summ_value:
        one_sent_summ_value = 'None'        

    return title, keywords_value, tldr_value, abstract_value, one_sent_summ_value





urls_df = pd.read_csv('urls/urls_iclr_2021_df.csv')

chunk_urls = urls_df['urls'][0:10]

urls = []
titles = []
keywords = []
tldrs = []
abstracts = []
one_sentence_summ = []
counter = 1



for address in chunk_urls:
    try:
        title, keyword, tldr, abstract, one_s_summ = extract_article_data(web_address=address)
        if title is None: 
            continue
        urls.append(address)
        titles.append(title)
        keywords.append(keyword)
        tldrs.append(tldr)
        abstracts.append(abstract)
        one_sentence_summ.append(one_s_summ)
        
        if counter % 15 == 0:
            print('number of extract data: ', counter)
            time.sleep(60)
        counter += 1
    except Exception as e:
        print(f"An error occurred with URL {address}: {e}")
        continue
    
data_dict = {'urls':urls, 'titles':titles, 'keywords':keywords,
             'tldrs':tldrs, 'abstracts':abstracts, 'one_sentence_summ':one_sentence_summ}

test = pd.DataFrame(data_dict)
test.to_csv('test/test.csv', index=False)
