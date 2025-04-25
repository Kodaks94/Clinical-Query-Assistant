# Clinical-Query-Assistant

🩺 **Clinical-Query-Assistant** is a fine-tuned version of [FLAN-T5 Base](https://huggingface.co/google/flan-t5-base), specialized for answering medical and clinical questions based on NHS Health A–Z guidelines.

This model was trained to assist with:
- Understanding symptoms
- Describing treatments
- Providing general medical advice
- Offering prevention strategies

 Fine-tuned with **LoRA (Low-Rank Adaptation)** for parameter-efficient training.

---

## Model Details

- **Base model**: [google/flan-t5-base](https://huggingface.co/google/flan-t5-base)
- **Fine-tuning technique**: LoRA (via [PEFT](https://huggingface.co/docs/peft/index))
- **Framework**: PyTorch
- **Dataset**: Custom scraped clinical Q&A from [NHS Health A-Z](https://www.nhs.uk/conditions/)
- **Training epochs**: 5
- **Batch size**: 4
- **Max sequence length**: 128 tokens

---

## How to Use

You can easily use this model for text-to-text generation with Hugging Face `pipeline`:

```python
from transformers import pipeline

qa_pipeline = pipeline("text2text-generation", model="KodaCodex/clinical-qa-model")

question = "What are the symptoms of pneumonia?"
response = qa_pipeline(question, max_length=256, do_sample=True, top_p=0.95, temperature=0.7, no_repeat_ngram_size=3)

print(response[0]['generated_text'])
```

Make sure to set `do_sample=True`, `top_p`, `temperature`, and `no_repeat_ngram_size`  
to avoid repetition and improve output quality.

---

## Example Outputs

| Question | Answer |
|:---|:---|
| "What are the symptoms of pneumonia?" | "The main symptoms include cough, fever, difficulty breathing, and chest pain." |
| "How is COPD treated?" | "Treatment includes inhalers, stopping smoking, pulmonary rehabilitation, and in some cases surgery." |
| "How can diabetes be prevented?" | "Maintaining a healthy weight, exercising regularly, eating a balanced diet, and avoiding smoking can help prevent diabetes." |

---

## Limitations

- This model **does not replace professional medical advice**.  
Always consult a licensed healthcare provider for medical diagnosis and treatment.
- Training was based on publicly available guidelines, not real-world patient records.
- The model may not generalize perfectly to all health topics or very recent research.

---

## License

- **Base model license**: Apache 2.0 (same as FLAN-T5)
- **Fine-tuned dataset**: Derived from public NHS website content.

---

## Credits

- Fine-tuning by **KodaCodex**
- Built using [Hugging Face Transformers](https://huggingface.co/docs/transformers/index) and [PEFT](https://huggingface.co/docs/peft/index).
- Data sourced from [NHS Health A-Z](https://www.nhs.uk/conditions/).

---

## Contact

Feel free to reach out for collaboration or questions!

- [Hugging Face Profile](https://huggingface.co/KodaCodex)
