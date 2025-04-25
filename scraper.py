import requests
from bs4 import BeautifulSoup
import json
import os
import time

def load_slugs(filepath="model/condition_slugs.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        slugs = json.load(f)
    return slugs

def scrape_condition_page(slug):
    url = f"https://www.nhs.uk/conditions/{slug}/"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    qas = []

    condition_name = slug.replace("-", " ")

    for heading in soup.find_all("h2"):
        section_title = heading.get_text(strip=True)
        content = ""

        for sibling in heading.find_next_siblings():
            if sibling.name == "h2":
                break
            if sibling.name == "p":
                content += sibling.get_text(strip=True) + " "
            elif sibling.name == "ul":
                for li in sibling.find_all("li"):
                    content += "- " + li.get_text(strip=True) + " "

        if content:
            question = f"What is the {section_title.lower()} of {condition_name}?"
            answer = content.strip()
            qas.append({"question": question, "answer": answer})

    return qas

def main():
    os.makedirs("model", exist_ok=True)

    slugs = load_slugs()
    print(f"Loaded {len(slugs)} conditions from file.")

    all_qas = []

    for slug in slugs:
        print(f"Scraping {slug}...")
        qas = scrape_condition_page(slug)
        all_qas.extend(qas)
        time.sleep(1)  # polite pause

    with open("model/data.jsonl", "w", encoding="utf-8") as f:
        for qa in all_qas:
            f.write(json.dumps(qa) + "\n")

    print(f"Saved {len(all_qas)} Q&A pairs to model/data.jsonl.")

if __name__ == "__main__":
    main()
