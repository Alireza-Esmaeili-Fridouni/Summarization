import spacy
import evaluate
from bert_score import BERTScorer

def get_word_count(df, df_generated_summary:str, new_col_name:str):
  df[new_col_name] = df[df_generated_summary].apply(lambda x:len(str(x).split(" ")))
  return df

def get_sentence_count(df, df_generated_summary:str, new_col_name:str):
  nlp = spacy.load('en_core_web_sm')  
  df[new_col_name] = df[df_generated_summary].apply(lambda x:len([sent.text for sent in nlp(str(x)).sents]))
  return df

def BLUE_Score(df, df_ground_truth:str, df_generated_summary:str, new_col_name:str):
  bleu = evaluate.load("bleu")
  df[new_col_name] = df.apply(lambda x:bleu.compute(predictions=[str(x[df_generated_summary])],
                                                    references=[str(x[df_ground_truth])]), axis=1)
  return df

def BERT_Score(df, model_name:str, df_ground_truth:str, df_generated_summary:str, new_col_name:str):
  scorer = BERTScorer(model_type=model_name)
  ground_truth = df[df_ground_truth].tolist()
  generated_summary = df[df_generated_summary].tolist()
  precision, recall, f1 = scorer.score(cands=generated_summary, refs=ground_truth)
  combined = [f"{round(p.item(), 3)}, {round(r.item(), 3)}, {round(f.item(), 3)}" 
                for p, r, f in zip(precision, recall, f1)]
  df[new_col_name] = combined
  return df
  
  

  
  