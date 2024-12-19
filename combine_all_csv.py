import pandas as pd
import glob

names_datasets = glob.glob('df_*.csv')

df_iclr_2017_2020 = pd.DataFrame()

dfs = []

for file in names_datasets:
    df_temp = pd.read_csv(file)
    dfs.append(df_temp)
    
df_iclr_2017_2020 = pd.concat(dfs, ignore_index=True)

df_iclr_2017_2020.to_csv('df_iclr_2017_2020.csv', index=False)

