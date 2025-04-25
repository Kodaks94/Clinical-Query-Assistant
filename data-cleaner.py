import json
import os
import re
import html

def clean_text(text):
    text = html.unescape(text)
    text = text.replace('\u00a0', ' ')
    text = text.replace('\u2013', '-')
    text = text.replace('\u2019', "'")
    text = text.replace('\u2018', "'")
    text = text.replace('\u201c', '"')
    text = text.replace('\u201d', '"')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def rewrite_question(question):
    question = question.lower().strip()

    # Smart rewrites
    if "getting a diagnosis" in question or "diagnosis" in question:
        return "How is the condition diagnosed?"
    if "how alzheimer's disease is treated" in question or "treatment" in question:
        return "How is the condition treated?"
    if "preventing" in question or "prevention" in question or "reduce your risk" in question:
        return "How can the condition be prevented?"
    if "symptoms" in question:
        return "What are the symptoms of the condition?"
    if "causes" in question:
        return "What causes the condition?"
    if "outlook" in question:
        return "What is the outlook for the condition?"
    if "living with" in question:
        return "What is it like living with the condition?"

    # Default fallback
    return question.capitalize() + "?"

def clean_question(raw_q):
    q = clean_text(raw_q)

    # Skip empty or junk questions
    if len(q) < 10:
        return ""

    q = rewrite_question(q)

    # Final fix: replace "the condition" later with real disease name
    return q

def clean_answer(a):
    a = clean_text(a)
    return a

def clean_data(input_path="model/data.jsonl", output_path="model/data_clean.jsonl"):
    cleaned = []

    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            raw_q = item.get("question", "").strip()
            raw_a = item.get("answer", "").strip()

            q = clean_question(raw_q)
            a = clean_answer(raw_a)

            # Try to infer disease name from the raw question
            disease = raw_q.split("of")[-1].strip(" ?")
            if "condition" in q.lower():
                q = q.replace("the condition", disease)

            if q and len(q) > 10 and len(a) > 20:
                cleaned.append({"question": q, "answer": a})

    print(f"Keeping {len(cleaned)} good Q&A pairs out of {len(open(input_path).readlines())}.")

    with open(output_path, "w", encoding="utf-8") as f:
        for qa in cleaned:
            f.write(json.dumps(qa) + "\n")

    print(f"Saved cleaned data to {output_path}")

if __name__ == "__main__":
    clean_data()
