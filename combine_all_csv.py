import pandas as pd
import glob
import re
import os


def combine_csv(name_folder: str):
    # names_datasets = list(map(os.path.basename, glob.glob(f'{name_folder}/df_*.csv')))

    names_datasets = glob.glob(f'{name_folder}/df_*.csv')
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


iclr_20212 = combine_csv('iclr_from_2017_to_2020')
iclr_20212.to_csv('test_2021.csv', index=False)

