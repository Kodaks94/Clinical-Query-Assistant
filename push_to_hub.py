from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_dir = "trained_model/clinical-qa-model"

model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)
tokenizer = AutoTokenizer.from_pretrained(model_dir)

model.push_to_hub('clinical-qa-model')
tokenizer.push_to_hub('clinical-qa-model')

