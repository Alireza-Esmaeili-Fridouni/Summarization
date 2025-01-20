from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, BitsAndBytesConfig
from huggingface_hub import login
import torch

# load model with tokenizer
def load_model(model_name:str):
    
    if 'llama' in model_name.lower():
        lama_token = input("please enter lama's access token: ")
        login(lama_token)
    
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        # torch_dtype = "auto",
        device_map = "auto"    
        )
    
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        return_tensors = "pt"
        )
    
    return model, tokenizer

# load pipeline model
def load_pipeline_model(model_name: str):
    
    if 'llama' in model_name.lower():
        lama_token = input("please enter lama's access token: ")
        login(lama_token)
        
    pipeline_model = pipeline(
        "text-generation",
        model = model_name,
        device_map="auto"
        # torch_dtype=torch.float16
        )
    
    return load_pipeline_model


# Qlora model
def load_qlora_model(
                    model_name:str,load_in_4bit=True,
                    bnb_4bit_use_double_quant=False,
                    bnb_4bit_quant_type="nf4",
                    quant_config_kwargs={},
                    model_kwargs={},
                    lora_config_kwargs={}
                    ):
    
    