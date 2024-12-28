from bs4 import BeautifulSoup
import requests
import pandas as pd
import time



def extract_article_data(web_address, years:int): 
    try:
        source = requests.get(web_address).text
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {web_address}: {e}")
        return None, None, None, None, None

    soup = BeautifulSoup(source, 'html.parser')

    
    article = soup.find('div', class_='forum-container')
    
    # Check for the existence of the 'forum-container' element
    if not article:
        raise Exception(f"Error: 'forum-container' not found for {web_address}")

    if years != 2024:
        title_element = article.find('div', class_='title_pdf_row')
    else:
        title_element = article.find('div', class_='forum-title')
    
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
        sibling = field.find_next_sibling("span", class_="note-content-value")
        if sibling:
            # Use the extract_combined_text function to get combined text
            combined_text = extract_combined_text(sibling)
            if "Keywords" in field.get_text(strip=True):
                keywords_value = combined_text.replace(',', ';')
            elif "TL;DR" in field.get_text(strip=True):
                tldr_value = combined_text
            elif "Abstract" in field.get_text(strip=True):
                abstract_value = combined_text
            elif "One-sentence Summary" in field.get_text(strip=True):
                one_sent_summ_value = combined_text
    
    if not keywords_value:
        keywords_value = 'None'
    if not tldr_value:
        tldr_value = 'None'
    if not abstract_value:
        abstract_value = 'None'
    if not one_sent_summ_value:
        one_sent_summ_value = 'None'        

    return title, keywords_value, tldr_value, abstract_value, one_sent_summ_value




# This function extracts text from an HTML element, combining normal text and MathJax.
def extract_combined_text(element):
    combined_text = []
    
    for content in element.contents:
        if isinstance(content, str):
            # If the content is a string, add it directly
            combined_text.append(content)
        elif content.name == 'mjx-container':
            # If the content is a MathJax element, extract its text
            combined_text.append(content.get_text(strip=True))
        else:
            # If it's another element, process it recursively
            combined_text.append(extract_combined_text(content))
    
    return ''.join(combined_text)


# Creator batch from urls
def batch_creator(urls_list, batch_size, delay_minute):
    for index in range(0, len(urls_list), batch_size):
        batch = urls_list[index:index+batch_size]
        yield batch
        time.sleep(delay_minute*60)



urls_df = pd.read_csv('urls/iclr_2024_urls_df.csv')
urls_list = urls_df['urls'].tolist()

counter = 1
batch_counter = 0


for batch in batch_creator(urls_list, 200, 2):
    urls = []
    titles = []
    keywords = []
    tldrs = []
    abstracts = []
    one_sentence_summ = []
    
    for address in batch:
        try:
            title, keyword, tldr, abstract, one_s_summ = extract_article_data(web_address=address, years=2024)
            if title is None: 
                continue
            urls.append(address)
            titles.append(title)
            keywords.append(keyword)
            tldrs.append(tldr)
            abstracts.append(abstract)
            one_sentence_summ.append(one_s_summ)
            
            if counter % 30 == 0:
                print('Number of extract data: ', counter)
                time.sleep(60)
            counter += 1
            
        except Exception as e:
            print(f"An error occurred with URL {address}: {e}")
            continue
        
    batch_counter += 1
    data_dict = {'urls':urls, 'titles':titles, 'keywords':keywords,
                'tldrs':tldrs, 'abstracts':abstracts, 'one_sentence_summ':one_sentence_summ}
    
    df_iclr = pd.DataFrame(data_dict)
    df_iclr.to_csv(f"iclr_2024/df_iclr_2024_{urls_list.index(df_iclr.iloc[0]['urls'])}_{urls_list.index(df_iclr.iloc[-1]['urls'])}.csv",
                   index=False, encoding='utf-8')
    
    print('Number of batch: ', batch_counter)
