from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, BitsAndBytesConfig
from peft import PeftModel, get_peft_model, LoraConfig, TaskType
from huggingface_hub import login
import torch


class LLMLoader:
    
    def __init__(self, model_name:str, token:str=""):
        self.model_name = model_name
        if 'llama' in self.model_name.lower():
            login(token)
    
    # load model with tokenizer
    def load_model(self):
        
        model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            device_map = "balanced"    
            )
        
        tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            )
        
        return model, tokenizer

    # load pipeline model
    def load_pipeline_model(self):
            
        pipeline_model = pipeline(
            "text-generation",
            model = self.model_name,
            device_map="balanced"
            )
        
        return pipeline_model


    # Qlora model
    def load_qlora_model(self):
          
        #load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            )
        
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
            quantization_config=quant_config,
            device_map="balanced"
            )
        
        # Define LoRA configuration
        lora_config = LoraConfig(
            task_type=TaskType.CAUSAL_LM,  # Task type: causal language modeling
            r=16,  # LoRA rank
            lora_alpha=32,  # LoRA scaling factor
            target_modules=["q_proj", "v_proj"],  # Target modules for adaptation
            lora_dropout=0.1,  # Dropout rate
            bias="none"  # Bias strategy
            )
        # Add LoRA layers to the base model
        qlora_model = get_peft_model(model, lora_config)
        
        return qlora_model, tokenizer