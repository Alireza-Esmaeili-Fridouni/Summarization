from llm_loader import Loader
import util

class SummarizerLLM:
    
    def __init__(self, model_name, load_type='qlora'):
        self.model, self.tokenizer = Loader(model_name=model_name, load_type=load_type)
        
    def summarize(self, input_text):
        encoded_data = self.tokenizer(input_text, return_tensors="pt").to(self.model.device)
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
        """
        Summarizes a batch of input texts using the model.

        Args:
            input_texts (list of str): A batch of texts to summarize.

        Returns:
            list of str: Summarized texts for each input.
        """
        # Tokenize the batch of input texts
        encoded_data = self.tokenizer(
            input_texts, 
            return_tensors="pt", 
            padding=True,  # Ensures uniform tensor sizes
            truncation=True  # Avoids excessively long inputs
        ).to(self.model.device)

        # Generate summaries for all inputs in the batch
        generated_ids = self.model.generate(
            **encoded_data,
            max_new_tokens=512
        )

        # Remove input tokens from generated output (useful for models like T5)
        generated_ids = [
            output_ids[len(input_ids):] 
            for input_ids, output_ids in zip(encoded_data["input_ids"], generated_ids)
        ]

        # Decode the generated summaries
        decoded_data = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)

        return decoded_data  # Returns a list of summaries
