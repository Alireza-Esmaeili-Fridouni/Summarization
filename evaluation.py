import spacy
import evaluate
from bert_score import BERTScorer
import pandas as pd

class Evaluator:
  def __init__(self, generated_summary:str, bert_scorer=None, bert_model_name='allenai/scibert_scivocab_uncased'):
    self.generated_summary = generated_summary
    self.bert_model_name = bert_model_name
    self.bert_scorer = bert_scorer if bert_scorer else BERTScorer(model_type=bert_model_name)
  
  def get_word_count(self):
    return len(str(self.generated_summary).split(" "))
  
  def get_sentence_count(self, model_name='en_core_web_sm'):
    nlp = spacy.load(model_name)  
    sentence_count = len([sent.text for sent in nlp(str(self.generated_summary)).sents])
    return sentence_count
  
  def BLEU_Score(self, ground_truth:str):
    bleu = evaluate.load("bleu")
    score = bleu.compute(predictions=[str(self.generated_summary)], references=[str(ground_truth)])
    return score['bleu']
  
  def ROUGE_Score(self, ground_truth:str):
    rouge = evaluate.load("rouge")
    score = rouge.compute(predictions=[str(self.generated_summary)], references=[str(ground_truth)])
    return score['rouge1'], score['rougeL']
  
  def BERT_Score(self, ground_truth:str):
    precision, recall, f1 = self.bert_scorer.score(cands=[self.generated_summary], refs=[ground_truth])
    return round(precision.item(), 3), round(recall.item(), 3), round(f1.item(), 3)
  

class Evaluation_df(Evaluator):
  def __init__(self, df:pd.DataFrame, new_col_name:str, generated_col_name:str):
    self.df = df
    self.new_col_name = new_col_name
    self.generated_col_name = generated_col_name

  def get_word_count(self):
    self.df[f"{self.new_col_name}_word_count"] = self.df[self.generated_col_name].apply(lambda x:Evaluator(x).get_word_count())
    return self.df

  def get_sentence_count(self, model_name='en_core_web_sm'): 
    self.df[f"{self.new_col_name}_sentence_count"] = self.df[self.generated_col_name].apply(
                                  lambda x:Evaluator(x).get_sentence_count(model_name)
                                  )
    return self.df

  def BLEU_Score(self, ground_truth_col_name:str):
    self.df[f"{self.new_col_name}_BLEU_Score"] = self.df.apply(
                                  lambda x:Evaluator(x[self.generated_col_name]).BLEU_Score(x[ground_truth_col_name]), axis=1
                                  )
    return self.df
  
  def ROUGE_Score(self, ground_truth_col_name:str):
    self.df[f"{self.new_col_name}_ROUGE_Score"] = self.df.apply(
                                  lambda x:Evaluator(x[self.generated_col_name]).ROUGE_Score(x[ground_truth_col_name]), axis=1
                                  )
    return self.df

  def BERT_Score(self, ground_truth_col_name:str, model_name:str= 'allenai/scibert_scivocab_uncased'):
    self.df[f"{self.new_col_name}_BERT_Score(Precision, Recall, F1)"] = self.df.apply(
        lambda x: ", ".join(map(str, Evaluator(x[self.generated_col_name], bert_model_name=model_name).BERT_Score(x[ground_truth_col_name]))),
        axis=1
    )
    return self.df

def EVALUATION(df:pd.DataFrame, bert_model_name:str):
  evaluation = Evaluation_df(df=df, new_col_name="Evaluation", generated_col_name="generated-summary")
  df = evaluation.get_word_count()
  df = evaluation.get_sentence_count()
  df = evaluation.BLEU_Score(ground_truth_col_name="one_sentence_summary")
  df = evaluation.ROUGE_Score(ground_truth_col_name="one_sentence_summary")
  df = evaluation.BERT_Score(model_name=bert_model_name, ground_truth_col_name="one_sentence_summary")
  return df

  
  