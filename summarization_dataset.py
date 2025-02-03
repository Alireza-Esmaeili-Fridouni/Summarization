from torch.utils.data import Dataset, DataLoader
import pandas as pd
import os
import util
import config

class SummaryDataset(Dataset):
    def __init__(self, path:str, tokenizer):
        super().__init__()
        self.data = pd.read_csv(path)
        self.tokenizer = tokenizer
        
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        title = self.data.iloc[index]['titles']
        abstract = self.data.iloc[index]['abstracts'] 
        summary = self.data.iloc[index]['one_sentence_summary']
        message = util.prompt_filler(prompt_template=config.standard_prompt,
                                     instruction=config.instruction,
                                     title=title,
                                     abstract=abstract
                                     )
        text = self.tokenizer.apply_chat_template(
                message,
                tokenize=False,
                add_generation_prompt=True
            )
        return text, summary 
    
    
def get_dataloader(path:str, tokenizer, shuffle=True, batch_size=2):
    dataset = SummaryDataset(path, tokenizer)
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)