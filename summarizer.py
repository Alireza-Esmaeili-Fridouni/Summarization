from llm_loader import Loader
import util

class SummarizerLLM:
    
    def __init__(self, model_name, load_type='qlora'):
        self.model, self.tokenizer = Loader(model_name=model_name, load_type=load_type)
        
    def summarize(self, input_text):
        text = self.tokenizer.apply_chat_template(
                input_text,
                tokenize=False,
                add_generation_prompt=True
            )
        encoded_data = self.tokenizer([text], return_tensors="pt").to(self.model.device)
        generated_ids = self.model.generate(
                **encoded_data,
                max_new_tokens=512
            )
        generated_ids = [
                output_ids[len(input_ids):] 
                for input_ids, output_ids in zip(encoded_data["input_ids"], generated_ids)
            ]
        decoded_data = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return decoded_data
    
    def summarize_batch(self, input_texts):
        summaries = []
        for text in input_texts:
            summary = self.summarize(input_text=text)
            summaries.append(summary)
        return summaries