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


# def batch_addresses(url_list, batch_size, delay_minute):
#     for index in range(0, len(url_list), batch_size):
#         segment = url_list[index:index+batch_size]
#         yield batch
#         time.sleep(delay_minute * 60)
        
urls_df = pd.read_csv('urls_df.csv')

chunk_urls = urls_df['urls'][0:200]
chunk_urls = urls_df['urls'][200:400]
chunk_urls = urls_df['urls'][400:600]
chunk_urls = urls_df['urls'][600:800]
chunk_urls = urls_df['urls'][800:1000]
chunk_urls = urls_df['urls'][1000:1200]
chunk_urls = urls_df['urls'][1200:1400]
chunk_urls = urls_df['urls'][1400:1600]
chunk_urls = urls_df['urls'][1600:1800]
chunk_urls = urls_df['urls'][1800:2000]


urls = []
titles = []
keywords = []
tldrs = []
abstracts = []
counter = 1
batch_counter = 1

# for batch in batch_addresses(urls_df, batch_size=200, delay_minute=4):
#     print('batch counter: ', batch_counter)
#     for address in batch:
        
#         title, keyword, tldr, abstract = extract_article_data(web_address=address)
#         urls.append(address)
#         titles.append(title)
#         keywords.append(keyword)
#         tldrs.append(tldr)
#         abstracts.append(abstract)
#         if counter % 30 == 0:
#             time.sleep(60)
#         counter += 1
#     batch_counter += 1

for address in chunk_urls:
    try:
        title, keyword, tldr, abstract = extract_article_data(web_address=address)
        if title is None: 
            continue
        urls.append(address)
        titles.append(title)
        keywords.append(keyword)
        tldrs.append(tldr)
        abstracts.append(abstract)
        
        if counter % 15 == 0:
            print('number of extract data: ', counter)
            time.sleep(60)
        counter += 1
    except Exception as e:
        print(f"An error occurred with URL {address}: {e}")
        continue
    
data_dict = {'urls':urls, 'titles':titles, 'keywords':keywords, 'tldrs':tldrs, 'abstracts':abstracts}

df_1800_1999 = pd.DataFrame(data_dict)
df_1800_1999.to_csv('df_1800_1999.csv', index=False)
