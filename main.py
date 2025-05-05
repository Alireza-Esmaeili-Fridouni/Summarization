from summarization_dataset import BaseAbstractDataset, AdvancedAbstractDataset
from summarization_pipeline import SummarizationPipeline
from config import model_name_list, prompt_list, train_df, test_df, huggingface_token, openai_token
from util import read_csv, save_dataframe
import evaluation as ev
    
    
if __name__ == "__main__":
    
    evaluate = ev.Evaluation()
    for model_name in model_name_list:
        dataset = read_csv(train_df)
        for prompt_name, prompt in prompt_list.items():
            pipeline = SummarizationPipeline(model_name=model_name,
                                            load_type="qlora",
                                            batch_size=2,
                                            token=huggingface_token
                                            )
            if prompt_name != "dsp_prompt":
                output = pipeline.run(dataset=dataset,
                            dataset_class=BaseAbstractDataset,
                            prompt=prompt)
            else:
                output = pipeline.run(dataset=dataset,
                            dataset_class=AdvancedAbstractDataset,
                            prompt=prompt)
            dataset[prompt_name] = output
            dataset = evaluate.evaluate_summary(df=dataset, prompt_name=prompt_name)
        file_name = f"{model_name}-evaluation.csv"
        save_dataframe(df=dataset, directory="", filename=file_name)
