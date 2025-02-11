from summarization_dataset import BaseAbstractDataset, get_dataloader
from summarization_dataset import AdvancedAbstractDataset
from summarizer import SummarizerLLM
import config
import pandas as pd
import util
import os


class SummarizationPipeline:
    def __init__(self, model_name:str, load_type="qlora", batch_size=2, token=""):
        self.summarizer = SummarizerLLM(model_name=model_name, load_type=load_type, token=token)
        self.model, self.tokenizer = self.summarizer.get_model_and_tokenizer()
        self.batch_size = batch_size
        
    def batch_processing(self, data_loader):
        result = list()
        for batch in data_loader:
            input_texts, _ = batch
            summaries_batch = self.summarizer.summarize_batch(input_texts=input_texts)
            summaries = result.extend(summaries)
        return summaries 
        # for batch in data_loader:
        #     input_texts, grand_truth = batch
        #     summaries_batch = self.summarizer.summarize_batch(input_texts=input_texts)
        #     for gt, generated in zip(grand_truth, summaries_batch):
        #         result.append({"Ground_truth":gt, "Generated Summary":generated})
        # return result
        
    def run(self, dataset_class, input_path, prompt):
        if not os.path.exists(input_path):
            print(f"Input path {input_path} does not exist")
            return
        data_loader = get_dataloader(dataset_class=dataset_class,
                                     path=input_path,
                                     tokenizer=self.tokenizer,
                                     prompt=prompt,
                                     shuffle=False,
                                     batch_size=self.batch_size
                                    )
        results = self.batch_processing(data_loader)
        df = pd.DataFrame(results)
        return df
    
input_path = ""
prompt = ""
    
if __name__ == "__main__":
    pipeline = SummarizationPipeline(model_name=config.model_name,
                                     load_type="qlora",
                                     batch_size=2,
                                     token=config.token
                                    )
    pipeline.run(input_path=input_path, prompt=prompt)