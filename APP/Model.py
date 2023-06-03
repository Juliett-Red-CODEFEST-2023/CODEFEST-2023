import transformers
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForTokenClassification
tokenizer = AutoTokenizer.from_pretrained("MMG/xlm-roberta-large-ner-spanish")
model = AutoModelForTokenClassification.from_pretrained("MMG/xlm-roberta-large-ner-spanish")

def ReviewData(dic):
    info=dic["TEXTO"]
    print(info)
    text=GetInfo(info)
    return text

