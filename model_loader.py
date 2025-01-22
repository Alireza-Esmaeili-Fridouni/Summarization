from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, BitsAndBytesConfig
from peft import PeftModel, get_peft_model, LoraConfig, TaskType
from huggingface_hub import login
import torch

# load model with tokenizer
def load_model(model_name:str, model_kwargs={}, tokenizer_kwargs={}):
    
    if 'llama' in model_name.lower():
        lama_token = input("please enter lama's access token: ")
        login(lama_token)
    
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map = "auto",
        **model_kwargs    
        )
    
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        return_tensors = "pt",
        **tokenizer_kwargs
        )
    
    return model, tokenizer

# load pipeline model
def load_pipeline_model(model_name: str, pipeline_kwargs={}):
    
    if 'llama' in model_name.lower():
        lama_token = input("please enter lama's access token: ")
        login(lama_token)
        
    pipeline_model = pipeline(
        "text-generation",
        model = model_name,
        device_map="auto",
        **pipeline_kwargs
        )
    
    return pipeline_model


# Qlora model
def load_qlora_model(
                    model_name:str,
                    tokenizer_kwargs={},
                    quant_config_kwargs={},
                    model_kwargs={},
                    lora_config_kwargs={}
                    ):
    
    if 'llama' in model_name.lower():
        lama_token = input("please enter lama's access token: ")
        login(lama_token)
    
    #load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        return_tensors = "pt",
        **tokenizer_kwargs
        )
    
    # Quantization configuration for efficient memory usage
    quant_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=False,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        **quant_config_kwargs
        )
    
    # Load the base model in 4-bit precision
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=quant_config,
        device_map="auto",
        **model_kwargs
        )
    
    # Define LoRA configuration
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,  # Task type: causal language modeling
        r=16,  # LoRA rank
        lora_alpha=32,  # LoRA scaling factor
        target_modules=["q_proj", "v_proj"],  # Target modules for adaptation
        lora_dropout=0.1,  # Dropout rate
        bias="none",  # Bias strategy
        **lora_config_kwargs
        )
    # Add LoRA layers to the base model
    qlora_model = get_peft_model(model, lora_config)
    
    return tokenizer, qlora_model