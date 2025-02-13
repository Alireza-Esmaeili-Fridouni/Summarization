from summarization_dataset import BaseAbstractDataset, AdvancedAbstractDataset
from summarization_pipeline import SummarizationPipeline
import config
import util
    
dataset_name = ""
prompt = ""
dataset_class = ""
    
if __name__ == "__main__":
   
    for model_name in config.model_name_list:
        for prompt_name, prompt in config.prompt_list.items():
            dataset = util.read_csv(config.dataset_path)
            pipeline = SummarizationPipeline(model_name=config.model_name,
                                            load_type="qlora",
                                            batch_size=2,
                                            token=config.token
                                            )
            output = pipeline.run(dataset=dataset,
                        dataset_class=dataset_class,
                        prompt=prompt)
            file_name = f"{model_name}-{prompt_name}-evaluation.csv"
            # save_dataframe(df, directory, filename