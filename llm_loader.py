from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, BitsAndBytesConfig
from peft import PeftModel, get_peft_model, LoraConfig, TaskType
from huggingface_hub import login
import torch


class LLMLoader:
    
    def __init__(self, model_name:str, token:str=""):
        self.model_name = model_name
        self.token = token
    
    # load model with tokenizer
    def load_simple_model(self):       
        model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                token = self.token,
                device_map = "balanced"
            )      
        tokenizer = AutoTokenizer.from_pretrained(self.model_name, token=self.token)
        return model, tokenizer

    # load pipeline model
    def load_pipeline_model(self):     
        pipeline_model = pipeline(
                "text-generation",
                model = self.model_name,
                token=self.token,
                device_map="balanced"
            )
        return pipeline_model, None
    
    # load quantizing
    def load_quantized_model(self): 
        #load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(self.model_name, token=self.token)
        
        # Quantization configuration for efficient memory usage
        quant_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=False,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16
            )
        
        # Load the base model in 4-bit precision
        model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                token=self.token,
                quantization_config=quant_config,
                device_map="balanced"
            )
        
        return model, tokenizer


    # Qlora model
    def load_qlora_model(self): 
        #load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(self.model_name, token=self.token)
        
        # Quantization configuration for efficient memory usage
        quant_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=False,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16
            )
        
        # Load the base model in 4-bit precision
        model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                token=self.token,
                quantization_config=quant_config,
                device_map="balanced"
            )
        
        # Define LoRA configuration
        lora_config = LoraConfig(
                task_type=TaskType.CAUSAL_LM,  
                r=16,  
                lora_alpha=32,  
                target_modules=["q_proj", "v_proj"],  
                lora_dropout=0.1,  
                bias="none"  
            )
        
        # Add LoRA layers to the base model
        qlora_model = get_peft_model(model, lora_config)
        
        return qlora_model, tokenizer
    
    
class Loader:

    model_loader = {
            "simple": "load_simple_model",
            "pipeline": "load_pipeline_model",
            "qlora": "load_qlora_model",
            "quantized":"load_quantized_model" 
        }
    def __new__(cls, model_name:str, token:str="", load_type:str=""):
        loader = "LLMLoader(model_name=model_name, token=token)." + Loader.model_loader.get(load_type, "load_simple_model") + "()"
        return eval(loader)
        
# loader = LLMLoader(model_name="llama") 
# model, tokenizer = loader.load_simple_model()