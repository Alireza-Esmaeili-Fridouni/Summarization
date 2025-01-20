from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login
import torch

# function for loading model
def load_model(model_name:str):
    
    if 'llama' in model_name.lower():
        login()
    
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype = "auto",
        device_map = "auto"    
        )
    
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        return_tensors = "pt")
    
    return model, tokenizer