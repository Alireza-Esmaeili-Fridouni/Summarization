from summarization_dataset import BaseAbstractDataset, AdvancedAbstractDataset
from summarization_pipeline import SummarizationPipeline
import config
import util
import evaluation as ev
    
dataset_name = ""
prompt = ""
dataset_class = ""
    
if __name__ == "__main__":
    
    evaluate = ev.Evaluation()
    for model_name in config.model_name_list:
        for prompt_name, prompt in config.prompt_list.items():
            dataset = util.read_csv(config.dataset_path)
            pipeline = SummarizationPipeline(model_name=model_name,
                                            load_type="qlora",
                                            batch_size=2,
                                            token=config.token
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
        file_name = f"{model_name}-{prompt_name}-evaluation.csv"
        util.save_dataframe(df=dataset, directory="", filename=file_name)
