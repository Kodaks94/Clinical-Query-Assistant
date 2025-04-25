from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, TrainingArguments, Trainer
from peft import get_peft_model, LoraConfig, TaskType
import torch
import json

model_name = 'google/flan-t5-base'
user_name = 'xxxxx'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Load cleaned dataset
with open('model/data_clean.jsonl', 'r', encoding='utf-8') as f:
    data = [json.loads(line) for line in f]

# Convert into a HuggingFace Dataset
dataset = Dataset.from_list([
    {"input_text": item["question"], "target_text": item["answer"]}
    for item in data
])

# Tokenization
def preprocess(example):
    inputs = tokenizer(
        example['input_text'],
        padding="max_length",
        truncation=True,
        max_length=128
    )
    labels = tokenizer(
        example['target_text'],
        padding="max_length",
        truncation=True,
        max_length=128
    )
    inputs['labels'] = labels['input_ids']
    return inputs

dataset = dataset.map(preprocess, batched=False)

# LoRA Config
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=['q', 'v'],
    lora_dropout=0.1,
    bias='none',
    task_type=TaskType.SEQ_2_SEQ_LM
)

model = get_peft_model(model, lora_config)

dataset = dataset.train_test_split(test_size=0.1)
train_dataset = dataset['train']
eval_dataset = dataset['test']

# Training arguments
training_args = TrainingArguments(
    output_dir='output',
    per_device_train_batch_size=4,
    num_train_epochs=5,
    logging_dir='logs',
    save_total_limit=1,
    save_steps=100,
    eval_strategy="steps",
    eval_steps=100,
    learning_rate=2e-4,
    report_to="none"
)
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,  # <-- add this line
    data_collator=None,
    tokenizer=tokenizer
)


trainer.train()

# Save model
model.save_pretrained( 'trained_model/clinical-qa-model')
tokenizer.save_pretrained('trained_model/clinical-qa-model')
