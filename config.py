
standard_prompt = '''Generate a short summary from the title and abstract of a paper as content into a concise single sentence of no 
more than 30 words. Follow these instructions:
- Ensure the output is a single cohesive sentence without title and abstract.
- Focus solely on the essential information from the title and abstract, ensuring clarity and precision.
- Do not include unnecessary details or additional information or exceed the specified word count of 30 words.
Title: {title}
Abstract: {abstract}
One sentence summary:'''

cot_prompt = '''Generate a short summary from the title and abstract of a paper as content into a concise single sentence of no 
more than 30 words. Follow these instructions:
  - Ensure the output is a single cohesive sentence without title and abstract.
  - Focus solely on the essential information from the title and abstract, ensuring clarity and precision.
  - Do not include unnecessary details or additional information or exceed the specified word count of 30.
  Step-by-step approach to obtain a short summary (one sentence summary):
  First, identify the main topic based on the title and abstract.
  Next, extract the key findings and contributions from the abstract.
  Finally, combine this information into a single, concise sentence that reflects the essence of the paper.
Title: {title}
Abstract: {abstract}
One sentence summary:'''

dsp_prompt = '''Generate a short summary from the title and abstract of a paper as content into a concise single sentence of no 
more than 30 words. Follow these instructions:
- Ensure the output is a single cohesive sentence without title and abstract.
- Focus solely on the essential information from the title and abstract, ensuring clarity and precision.
- Do not include unnecessary details or additional information or exceed the specified word count of 30 words.
Title: {title}
Abstract: {abstract}
This short summary must accurately and completely include the provided keywords.
Keywords: {keywords}
One sentence summary:'''


instruction = "You are an advanced model specializing in one sentence summary generation."
prompt_list = [standard_prompt, cot_prompt]
model_name_list = ["Qwen/Qwen2.5-1.5B-Instruct",
                   "Qwen/Qwen2.5-7B-Instruct",
                   "meta-llama/Llama-3.2-1B-Instruct",
                   "meta-llama/Llama-3.1-8B-Instruct",
                   "microsoft/Phi-3.5-mini-instruct",
                   "mistralai/Mistral-7B-Instruct-v0.3",
                   "tiiuae/Falcon3-1B-Instruct",
                   "tiiuae/falcon-mamba-7b-instruct",
                   "tiiuae/Falcon3-7B-Instruct",
                   "ministral/Ministral-3b-instruct"
                  ]
token = ""
loader_type = "quantized"
model_name = "meta-llama/Llama-3.2-1B-Instruct"
test_path = ""
train_path = ""