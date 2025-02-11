from torch.utils.data import Dataset, DataLoader
import os
import util
import config

class BaseAbstractDataset(Dataset):
    def __init__(self, dataset_name:str, tokenizer, prompt):
        super().__init__()
        self.data = util.read_csv(dataset_name)
        self.tokenizer = tokenizer
        self.prompt = prompt
        
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        title = self.data.iloc[index]['titles']
        abstract = self.data.iloc[index]['abstracts'] 
        summary = self.data.iloc[index]['one_sentence_summary']
        message = util.base_prompt_filler(prompt_template=self.prompt,
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
    
class AdvancedAbstractDataset(BaseAbstractDataset):
    def __getitem__(self, index):
        title = self.data.iloc[index]['titles']
        abstract = self.data.iloc[index]['abstracts']
        keywords = self.data.iloc[index]['keywords'] 
        summary = self.data.iloc[index]['one_sentence_summary']
        message = util.advanced_prompt_filler(prompt_template=self.prompt,
                                     instruction=config.instruction,
                                     title=title,
                                     abstract=abstract,
                                     keywords=keywords
                                     )
        text = self.tokenizer.apply_chat_template(
                message,
                tokenize=False,
                add_generation_prompt=True
            )
        return text, summary
        
    
    
def get_dataloader(dataset_class, dataset_name:str, tokenizer, prompt, shuffle=True, batch_size=2):
    dataset = dataset_class(dataset_name, tokenizer, prompt)
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)