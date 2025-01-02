import pandas as pd
import glob
import re
import os


def combine_csv(name_folder: str):
    # names_datasets = list(map(os.path.basename, glob.glob(f'{name_folder}/df_*.csv')))

    names_datasets = glob.glob(f'{name_folder}/*.csv')
    names_datasets = sorted(names_datasets,
                            key=lambda x: [int(num) for num in re.findall(r'\d+', os.path.basename(x))]
                            )

    df = pd.DataFrame()

    df_list = []

    for file in names_datasets:
        df_temp = pd.read_csv(file)
        df_list.append(df_temp)
        
    df = pd.concat(df_list, ignore_index=True)
    
    return df



name_folders = [name for name in os.listdir('.') if os.path.isdir(os.path.join('.', name)) and name.startswith('iclr')]

for name in name_folders:
    df = combine_csv(name)
    df.to_csv(f'collection_data/{name}.csv', index=False)


collection_dataset = combine_csv('collection_data')
collection_dataset.to_csv('collection_data/collection_dataset.csv', index=False)
