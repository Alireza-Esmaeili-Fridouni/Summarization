from torch.utils.data import Dataset, DataLoader
import pandas as pd
import os
import util
import config

class SummaryDataset(Dataset):
    def __init__(self, path:str, csv_file_name:str):
        super().__init__()
        self.path = path
        self.data = pd.read_csv(os.path.join(self.path, csv_file_name))
        
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        title = self.data.iloc[index]['titles']
        abstract = self.data.iloc[index]['abstracts'] 
        message = util.prompt_filler(prompt_template=config.standard_prompt,
                                     instruction=config.instruction,
                                     title=title,
                                     abstract=abstract
                                     )
        return message
    
    
def get_dataloader(path:str, csv_file_name:str, shuffle=True, batch_size=2):
    dataset = SummaryDataset(path, csv_file_name)
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)