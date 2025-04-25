import gradio as gr
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

# Load your fine-tuned model
model_dir = "trained_model/clinical-qa-model"  # Path where your trained model is saved
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)

# Create pipeline
qa_pipeline = pipeline("text2text-generation", model=model, tokenizer=tokenizer)

# Define prediction function
def answer_question(question):
    output = qa_pipeline(
        question,
        max_length=256,
        do_sample=True,
        top_p=0.95,
        temperature=0.7,          # Soft randomness
        no_repeat_ngram_size=3    # Do not repeat 3-word phrases
    )
    return output[0]['generated_text']


# Create Gradio interface
iface = gr.Interface(
    fn=answer_question,
    inputs=gr.Textbox(lines=2, placeholder="Ask a medical question..."),
    outputs=gr.Textbox(),
    title="Clinical Q&A Assistant",
    description="Ask clinical or health-related questions based on NHS guidelines.",
)

# Launch app
if __name__ == "__main__":
    iface.launch()
