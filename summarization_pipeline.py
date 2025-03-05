from summarization_dataset import get_dataloader
from summarizer import SummarizerLLM


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
            result.extend(summaries_batch)
        return result 
        # for batch in data_loader:
        #     input_texts, grand_truth = batch
        #     summaries_batch = self.summarizer.summarize_batch(input_texts=input_texts)
        #     for gt, generated in zip(grand_truth, summaries_batch):
        #         result.append({"Ground_truth":gt, "Generated Summary":generated})
        # return result
        
    def run(self, dataset, dataset_class, prompt):
        data_loader = get_dataloader(dataset_class=dataset_class,
                                     dataset=dataset,
                                     tokenizer=self.tokenizer,
                                     prompt=prompt,
                                     shuffle=False,
                                     batch_size=self.batch_size
                                    )
        results = self.batch_processing(data_loader)
        # dataset['generated-summary'] = results
        return results