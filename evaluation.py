import spacy
import evaluate
from bert_score import BERTScorer
import pandas as pd

class Evaluation:
  def __init__(self, generated_summary:str):
    self.generated_summary = generated_summary
  
  def get_word_count(self):
    return len(str(self.generated_summary).split(" "))
  
  def get_sentence_count(self, model_name='en_core_web_sm'):
    nlp = spacy.load(model_name)  
    sentence_count = len([sent.text for sent in nlp(str(self.generated_summary)).sents])
    return sentence_count
  
  def BLEU_ROUGE_Score(self, ground_truth:str, mode="bleu"):
    bleu = evaluate.load(mode)
    score = bleu.compute(predictions=[str(self.generated_summary)], references=[str(ground_truth)])
    return score
  
  def BERT_Score(self, model_name:str, ground_truth:str):
    scorer = BERTScorer(model_type=model_name)
    precision, recall, f1 = scorer.score(cands=[self.generated_summary], refs=[ground_truth])
    return round(precision.item(), 3), round(recall.item(), 3), round(f1.item(), 3)
  

class Evaluation_df(Evaluation):
  def __init__(self, df:pd.DataFrame, new_col_name:str, generated_col_name:str):
    # super().__init__()
    self.df = df
    self.new_col_name = new_col_name
    self.generated_col_name = generated_col_name

  def get_word_count(self):
    self.df[self.new_col_name] = self.df[self.generated_col_name].apply(lambda x:Evaluation(x).get_word_count())
    return self.df

  def get_sentence_count(self, model_name='en_core_web_sm'): 
    self.df[self.new_col_name] = self.df[self.generated_col_name].apply(
                                  lambda x:Evaluation(x).get_sentence_count(model_name)
                                  )
    return self.df

  def BLEU_ROUGE_Score(self, ground_truth_col_name:str, mode="bleu"):
    self.df[self.new_col_name] = self.df.apply(
                                  lambda x:Evaluation(x[self.generated_col_name]).BLEU_ROUGE_Score(x[ground_truth_col_name], mode=mode), axis=1
                                  )
    return self.df

  def BERT_Score(self, model_name:str, ground_truth_col_name:str):
    self.df[f"Precision, Recall, F1{self.new_col_name}"] = self.df.apply(
        lambda x: ", ".join(map(str, Evaluation(x[self.generated_col_name]).BERT_Score(model_name, x[ground_truth_col_name]))),
        axis=1
    )
    return self.df

  
  

  
  