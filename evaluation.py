import spacy
import evaluate
from bert_score import BERTScorer
import pandas as pd

class Evaluator:
  def __init__(self, bert_model_name='allenai/scibert_scivocab_uncased', model_name='en_core_web_sm'):
    self.bert_scorer = BERTScorer(model_type=bert_model_name)
    self.nlp = spacy.load(model_name) 
    self.bleu = evaluate.load("bleu")
    self.rouge = evaluate.load("rouge")
  
  def get_word_count(self, generated_summary):
    return len(str(generated_summary).split(" "))
  
  def get_sentence_count(self, generated_summary): 
    sentence_count = len([sent.text for sent in self.nlp(str(generated_summary)).sents])
    return sentence_count
  
  def bleu_score(self, ground_truth:str, generated_summary):
    if not generated_summary:
      return 0.0
    score = self.bleu.compute(predictions=[str(generated_summary)], references=[str(ground_truth)])
    return score['bleu']
  
  def rouge_score(self, ground_truth:str, generated_summary):
    if not generated_summary:
      return 0.0, 0.0
    score = self.rouge.compute(predictions=[str(generated_summary)], references=[str(ground_truth)])
    return round(score['rouge1'], 3), round(score['rougeL'], 3)
  
  def bert_score(self, ground_truth:str, generated_summary):
    try:
      if not generated_summary:
        return 0.0, 0.0, 0.0
      precision, recall, f1 = self.bert_scorer.score(cands=[generated_summary], refs=[ground_truth])
      return round(precision.item(), 3), round(recall.item(), 3), round(f1.item(), 3)
    except:
      return 0.0, 0.0, 0.0
  

class Evaluation(Evaluator):
  def __init__(self):
    self.evaluator = Evaluator()

  def word_count_eval(self, df, generated_col_name:str):
    df[f"{generated_col_name}_words_count"] = df[generated_col_name].apply(lambda x:self.evaluator.get_word_count(x))
    return df

  def sentence_count_eval(self, df, generated_col_name:str): 
    df[f"{generated_col_name}_sentences_count"] = df[generated_col_name].apply(
                                  lambda x:self.evaluator.get_sentence_count(x)
                                  )
    return df

  def bleu_score_eval(self, df, generated_col_name:str, ground_truth_col_name:str):
    df[f"{generated_col_name}_bleu"] = df.apply(
                                  lambda x:self.evaluator.bleu_score(ground_truth=x[ground_truth_col_name], generated_summary=x[generated_col_name]), 
                                  axis=1
                                  )
    return df
  
  def rouge_score_eval(self, df, generated_col_name:str, ground_truth_col_name:str):
    df[[f"{generated_col_name}_rouge1", f"{generated_col_name}_rougeL"]] = df.apply(
                                  lambda x:pd.Series(self.evaluator.rouge_score(
                                    ground_truth=x[ground_truth_col_name], generated_summary=x[generated_col_name]
                                  )), 
                                  axis=1
                                  )
    return df

  def bert_score_eval(self, df, generated_col_name:str, ground_truth_col_name:str):
    df[[f"{generated_col_name}_bert_score_precision", 
        f"{generated_col_name}_bert_score_recall", 
        f"{generated_col_name}_bert_score_f1"]] = df.apply(
        lambda x: pd.Series(self.evaluator.bert_score(ground_truth=x[ground_truth_col_name], generated_summary=x[generated_col_name])),
        axis=1
    )
    return df

  def evaluate_summary(self, df:pd.DataFrame, prompt_name:str):
    df = self.word_count_eval(df=df, generated_col_name=prompt_name)
    df = self.sentence_count_eval(df=df, generated_col_name=prompt_name)
    df = self.bleu_score_eval(df=df, generated_col_name=prompt_name, ground_truth_col_name="one_sentence_summary")
    df = self.rouge_score_eval(df=df, generated_col_name=prompt_name, ground_truth_col_name="one_sentence_summary")
    df = self.bert_score_eval(df=df, generated_col_name=prompt_name, ground_truth_col_name="one_sentence_summary")
    return df