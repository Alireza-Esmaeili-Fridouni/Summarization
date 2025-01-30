from llm_loader import Loader
import util

class SummarizerLLM:
    
    def __init__(self, model_name, load_type='qlora'):
        self.model, self.tokenizer = Loader(model_name=model_name, load_type=load_type)
        
    def summarize(self, input_text):
        # ...
        pass
    
    def summarize_batch(self, input_texts):
        pass