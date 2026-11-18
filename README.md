# Scientific Paper One-Sentence Summarization

**Benchmarking open-weight large language models and prompting strategies for concise summaries of scientific papers.**

This research project generates **one-sentence summaries** from paper titles and abstracts, with a target of **no more than 30 words**. It compares different language models and prompting strategies using an ICLR/OpenReview-derived dataset and several automatic evaluation metrics.

> **Scope:** This repository is an experimental **inference and evaluation pipeline**, not a deployed summarization API or a fine-tuning framework. The 30-word limit is specified in the prompts but is not enforced by post-processing.

## Highlights

- **Scientific paper summarization:** Generate a compact summary from a paper's title and abstract.
- **Three prompting strategies:** Standard zero-shot, step-by-step (CoT-style), and keyword-guided directional stimulus prompting.
- **Multi-model comparison:** Experiment with instruction-tuned language models from the Llama, Qwen, Falcon, Mistral, Phi, Gemma, and DeepSeek families.
- **Memory-aware loading:** Support for 4-bit quantization and LoRA-adapter wrapping via Transformers, bitsandbytes, and PEFT.
- **Comprehensive evaluation:** BLEU, ROUGE-1, ROUGE-L, BERTScore precision/recall/F1, word count, and sentence count.
- **Reproducible data split:** The included preprocessing notebook prepares training and test CSV files using a fixed random seed.

## Project Workflow

```text
ICLR / OpenReview paper pages
            |
            v
Data collection (data_collector/)
            |
            v
Raw papers (titles, abstracts, keywords, reference summaries)
            |
            v
Filtering and train/test split (data-processing.ipynb)
            |
            v
Prompt construction (config.py + summarization_dataset.py)
            |
            v
Model inference (llm_loader.py + summarizer.py)
            |
            v
Evaluation (evaluation.py)
            |
            v
Per-model CSV results (results/)
```

## Dataset

The dataset is derived from publicly accessible **[OpenReview](https://openreview.net/)** pages for the **International Conference on Learning Representations (ICLR)**. The data-collection scripts cover conference years **2017–2024**.

The main CSV fields used by the pipeline are:

| Column | Description |
| --- | --- |
| `urls` | Source paper page on OpenReview |
| `titles` | Scientific paper title |
| `abstracts` | Paper abstract used as the main summarization input |
| `keywords` | Paper keywords used in the directional stimulus prompt |
| `one_sentence_summary` | Reference summary used for evaluation |

The preprocessing process in [`data-processing.ipynb`](data-processing.ipynb):

1. Removes rows with missing reference summaries or keywords.
2. Retains reference summaries with **15–40 words**.
3. Retains records with **2–7 keywords**.
4. Retains abstracts with **100–300 words**.
5. Drops duplicate titles.
6. Splits the cleaned data into **80% training / 20% testing** (`random_state=42`).

The saved outputs of the notebook report the following dataset sizes:

| Dataset | Number of papers | Repository file |
| --- | ---: | --- |
| Raw collection | 24,478 | [`dataset/raw_collected_data.csv`](dataset/raw_collected_data.csv) |
| Cleaned dataset | 11,120 | [`dataset/processed_data.csv`](dataset/processed_data.csv) |
| Training split | 8,896 | [`dataset/train_data.csv`](dataset/train_data.csv) |
| Test split | 2,224 | [`dataset/test_data.csv`](dataset/test_data.csv) |

**Note:** The training split is available for further experiments, but the current [`main.py`](main.py) script performs **inference/evaluation on the test split**; it does not train or fine-tune a model. Reference summaries can be longer than the 30-word generation target because preprocessing allows up to 40 words.

## Prompting Strategies

The prompt templates are defined in [`config.py`](config.py):

| Strategy | Configuration key | Inputs | Description |
| --- | --- | --- | --- |
| **Standard zero-shot** | `standard_prompt` | Title + abstract | Directly requests one cohesive sentence of at most 30 words. |
| **CoT-style zero-shot** | `cot_prompt` | Title + abstract | Includes step-by-step guidance for identifying the topic, findings, and contributions before summarizing. |
| **Directional stimulus** | `dsp_prompt` | Title + abstract + keywords | Adds paper keywords as optional cues to steer the summary. |

The pipeline formats these inputs as chat messages using each model tokenizer's chat template.

## Supported Model Experiments

The [`results/`](results/) directory contains evaluation CSVs for models in these families:

- **Meta Llama:** Llama 3.1 8B Instruct and Llama 3.2 1B/3B Instruct
- **Qwen:** Qwen2.5 0.5B/1.5B/7B Instruct and Qwen3 0.6B/1.7B/4B
- **Falcon:** Falcon3 1B/7B Instruct and Falcon3 Mamba 7B Instruct
- **Mistral:** Mistral 7B Instruct v0.3
- **Microsoft Phi:** Phi-3.5 mini instruct
- **Google Gemma:** Gemma 3 1B IT
- **DeepSeek:** DeepSeek-R1-Distill-Qwen 14B

This list describes **saved experiment artifacts**, not models that are automatically run. The current `model_name_list` in `config.py` is empty because its model entries are commented out. You must select at least one model before running `main.py`.

Some models may require acceptance of their upstream license or authentication on Hugging Face. Hardware and VRAM needs vary substantially by model.

## Installation

### Prerequisites

- Python 3.10+ is a reasonable starting point (no Python version is pinned in this repository).
- A CUDA-capable NVIDIA GPU is strongly recommended for the default 4-bit `qlora` loading path; supported PyTorch/CUDA/bitsandbytes versions and available VRAM depend on your machine.
- Internet access for downloading models and evaluation resources on the first run.
- A Hugging Face access token for any gated model you want to evaluate.

Clone the project and create a virtual environment:

```bash
git clone https://github.com/Alireza-Esmaeili-Fridouni/Summarization.git
cd Summarization
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

Install a compatible **PyTorch build for your hardware** first (see the [official PyTorch installation guide](https://pytorch.org/get-started/locally/)), then install the Python packages used by the evaluation pipeline:

```bash
pip install pandas python-dotenv tqdm transformers accelerate bitsandbytes peft huggingface_hub \
  spacy evaluate bert-score rouge-score nltk sentencepiece
python -m spacy download en_core_web_sm
```

> The repository does not currently include a pinned `requirements.txt` or lockfile. The command above reflects imports in the source and is a **starting point**, not a tested or version-locked environment. Some Transformers/PEFT/model combinations may need specific compatible versions.

### Environment variables

Copy the provided example file:

```bash
cp .env-example .env
```

Edit `.env`:

```dotenv
HUGGINGFACE_ACCESS_TOKEN="your_huggingface_token"
OPENAI_KEY=""
```

`config.py` reads **both** environment variables using `os.environ[...]`, so both keys must exist. `OPENAI_KEY` is **not used by the current `main.py` inference path** and can be left blank. Do not commit real credentials to version control (`.env` is already in `.gitignore`).

## Quick Start: Run an Evaluation

**1. Select one or more models** by editing `model_name_list` in [`config.py`](config.py). For example:

```python
model_name_list = [
    "Qwen/Qwen2.5-0.5B-Instruct",
]
```

**2. Adjust the inference batch size** in [`main.py`](main.py) for your GPU. The checked-in script uses `batch_size=128`, which may be too large. For an initial test, you might try:

```python
pipeline = SummarizationPipeline(
    model_name=model_name,
    load_type="qlora",
    batch_size=4,
    token=huggingface_token,
)
```

**3. Run the experiment** from the repository root:

```bash
python main.py
```

For every selected model, `main.py`:

1. Loads the model/tokenizer using the requested loading mode.
2. Reads [`dataset/test_data.csv`](dataset/test_data.csv).
3. Generates summaries with all three prompts.
4. Computes length and similarity metrics against `one_sentence_summary`.
5. Writes a CSV to `results/<model-short-name>-evaluation.csv`.

For example, evaluating `Qwen/Qwen2.5-0.5B-Instruct` writes:

```text
results/Qwen2.5-0.5B-Instruct-evaluation.csv
```

The output contains the original test records, a generated summary column for each prompt (`standard_prompt`, `cot_prompt`, `dsp_prompt`), and metric columns such as `standard_prompt_rouge1`, `standard_prompt_rougeL`, `standard_prompt_bert_score_f1`, and `standard_prompt_words_count`.

**Important:** Models are downloaded on demand. The 4-bit path uses `torch.bfloat16`, which may not be supported on every GPU. If you encounter GPU memory or compatibility errors, reduce the batch size or change the loader configuration. This project has not been packaged as a CPU-first, one-command application.

## Evaluation Metrics

The implementation is in [`evaluation.py`](evaluation.py).

| Metric | What it measures |
| --- | --- |
| **BLEU** | N-gram overlap between generated and reference summaries. |
| **ROUGE-1** | Unigram overlap with the reference summary. |
| **ROUGE-L** | Longest-common-subsequence similarity with the reference. |
| **BERTScore P / R / F1** | Contextual semantic similarity using `allenai/scibert_scivocab_uncased`. |
| **Word count** | Number of space-separated tokens in the generated text. |
| **Sentence count** | Number of sentences detected by spaCy's `en_core_web_sm`. |

The repository also includes [`results/result_summary.csv`](results/result_summary.csv), an aggregate table covering a **subset of nine models**. Here are selected **directional-stimulus (`dsp_prompt`)** values reported in that file:

| Model | ROUGE-1 | ROUGE-L | BERTScore F1 | Average words |
| --- | ---: | ---: | ---: | ---: |
| Llama-3.1-8B | 0.360 | 0.279 | 0.691 | 28.991 |
| Falcon3-Mamba-7B | 0.331 | 0.257 | 0.690 | 24.944 |
| Phi-3.5-mini | 0.314 | 0.236 | 0.671 | 25.197 |
| Qwen2.5-7B | 0.312 | 0.239 | 0.673 | 19.837 |

These numbers are **existing stored results**, not newly rerun measurements. Consult the per-model CSV files for individual predictions. The aggregate summary does not include every CSV currently present in `results/`.

## Repository Structure

```text
Summarization/
├── .env-example                 # Environment-variable template
├── config.py                    # Prompts, model selection, dataset paths
├── main.py                      # Main multi-model evaluation script
├── llm_loader.py                # Transformers, quantization, PEFT loading
├── summarizer.py                # Single/batched text generation
├── summarization_dataset.py    # PyTorch datasets and prompt formatting
├── summarization_pipeline.py   # Dataloader-driven inference pipeline
├── evaluation.py               # Evaluation metrics
├── util.py                     # CSV and prompt helpers
├── data-processing.ipynb       # Data cleaning and train/test split
├── summarization.ipynb         # Earlier model experiments / Colab work
├── test.ipynb                  # Development experiments
├── data_collector/             # OpenReview scraping scripts and URL lists
├── dataset/                    # Raw, processed, train, and test CSVs
└── results/                    # Per-model evaluations and aggregate summary
```

## Data Collection and Reproducibility

The historical collection scripts under [`data_collector/`](data_collector/) use **Selenium**, **Requests**, and **Beautiful Soup** to retrieve paper URLs and extract metadata from OpenReview pages. To experiment with these scripts separately, install:

```bash
pip install selenium requests beautifulsoup4
```

The collection code includes **hard-coded paths, year-specific page selectors, and ChromeDriver assumptions**. It should be treated as a research record rather than a ready-to-run general-purpose crawler. Depending on your environment and changes to OpenReview's website, paths, selectors, and browser/driver setup may need updating. When collecting data, respect OpenReview's terms and rate limits.

The processed CSV files are already included, so **data scraping is not required** to run the standard evaluation pipeline. The preprocessing notebook writes its exports to the working directory; if regenerating the data, place the resulting CSVs into `dataset/` to match the paths in `config.py`.

## Limitations and Notes

- **No default experiment is enabled:** All entries in `config.py`'s `model_name_list` are currently commented out.
- **No training loop:** `load_type="qlora"` attaches LoRA modules to a 4-bit quantized base model, but the repository does **not** train the adapters. Do not interpret these evaluations as results of fine-tuned models.
- **Prompt-only length constraint:** The desired single-sentence, 30-word output is not guaranteed by `model.generate(max_new_tokens=512)`.
- **Dependencies are not pinned:** Results can vary across software and model versions, hardware, and inference configurations.
- **Results coverage differs:** Individual model CSVs and the aggregate `result_summary.csv` cover different sets of models.
- **No production interface:** There is currently no CLI argument parser, REST API, web interface, or test suite for the pipeline.

## Credits and Data Source

- Paper metadata and reference summaries: [OpenReview](https://openreview.net/) / [ICLR](https://iclr.cc/), subject to the original content's terms and attribution requirements.
- Models and tokenizers: Their respective creators and repositories on [Hugging Face](https://huggingface.co/).
- Project repository: [Alireza-Esmaeili-Fridouni/Summarization](https://github.com/Alireza-Esmaeili-Fridouni/Summarization).

## License

**No `LICENSE` file is present in the repository at the time of writing.** The repository should not be assumed to be open-source licensed solely because it is publicly accessible. Please contact the maintainer about reuse permissions, and follow the licenses/terms of upstream models and datasets.
