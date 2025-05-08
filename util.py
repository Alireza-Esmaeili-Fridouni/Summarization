import pandas as pd
import os

def read_csv(dataset_name:str):
    if not os.path.exists(dataset_name):
        print("Error: File not found.")
        return None
    try:
        df = pd.read_csv(dataset_name)
        return df
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def save_dataframe(df, directory, filename):
    if not os.path.exists(directory):
        os.mkdir(directory)
    file_path = os.path.join(directory, filename)
    df.to_csv(file_path, index=False, encoding='utf-8')
    print(f"DataFrame saved successfully at: {file_path}")
        
def base_prompt_filler(prompt_template, instruction, title, abstract):
    prompt = prompt_template.format(title=title, abstract=abstract)
    message = [
        {"role": "system", "content": instruction},
        {"role": "user", "content": prompt}
    ]
    return message

def advanced_prompt_filler(prompt_template, instruction, title, abstract, keywords):
    prompt = prompt_template.format(title=title, abstract=abstract, keywords=keywords)
    message = [
        {"role": "system", "content": instruction},
        {"role": "user", "content": prompt}
    ]
    return message