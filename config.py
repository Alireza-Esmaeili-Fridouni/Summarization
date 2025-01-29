
standard_prompt = '''Generate a short summary from the title and abstract of a paper as content into a concise single sentence of no 
more than 30 words. Follow these instructions:
- Ensure the output is a single cohesive sentence without title and abstract.
- Focus solely on the essential information from the title and abstract, ensuring clarity and precision.
- Do not include unnecessary details or additional information or exceed the specified word count of 30 words.
Title: 
Abstract: 
One sentence summary: '''

COT_prompt = '''Generate a short summary from the title and abstract of a paper as content into a concise single sentence of no 
more than 30 words. Follow these instructions:
  - Ensure the output is a single cohesive sentence without title and abstract.
  - Focus solely on the essential information from the title and abstract, ensuring clarity and precision.
  - Do not include unnecessary details or additional information or exceed the specified word count of 30.
  Step-by-step approach to obtain a short summary (one sentence summary):
  First, identify the main topic based on the title and abstract.
  Next, extract the key findings and contributions from the abstract.
  Finally, combine this information into a single, concise sentence that reflects the essence of the paper.
Title: 
Abstract: 
One sentence summary: '''

token = ""
loader_type = "quantized"
model_name = "meta-llama/Llama-3.2-1B-Instruct"
test_path = ""
train_path = ""