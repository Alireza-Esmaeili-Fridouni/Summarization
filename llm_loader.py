from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, BitsAndBytesConfig
from peft import PeftModel, get_peft_model, LoraConfig, TaskType
from huggingface_hub import login
import torch


class ModelLoader:
    
    def __init__(self, model_name:str):
        self.model_name = model_name
    
    # load model with tokenizer
    def load_model(self, token:str=""):
        
        if 'llama' in self.model_name.lower():
            login(token)
        
        model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            device_map = "auto"    
            )
        
        tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            return_tensors = "pt"
            )
        
        return model, tokenizer

    # load pipeline model
    def load_pipeline_model(self, token:str=""):
        
        if 'llama' in self.model_name.lower():
            login(token)
            
        pipeline_model = pipeline(
            "text-generation",
            model = self.model_name,
            device_map="auto"
            )
        
        return pipeline_model


    # Qlora model
    def load_qlora_model(
                        self,
                        token:str=""
                        ):
        
        if 'llama' in self.model_name.lower():
            login(token)
        
        #load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            return_tensors = "pt"
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
            device_map="auto"
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
        
        return tokenizer, qlora_model