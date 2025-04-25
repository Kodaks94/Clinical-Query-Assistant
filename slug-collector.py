from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import json
import os
import time


def get_all_condition_slugs():
    # Start Chrome browser in headless mode
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = "https://www.nhs.uk/conditions/"
    driver.get(url)
    time.sleep(3)  # Wait for page to load

    condition_slugs = []

    elements = driver.find_elements(By.CSS_SELECTOR, "ul.nhsuk-list--border li a")
    for elem in elements:
        href = elem.get_attribute('href')
        if href and "/conditions/" in href:
            slug = href.split("/conditions/")[1].strip("/")
            if slug:
                condition_slugs.append(slug)

    driver.quit()
    return condition_slugs


def main():
    os.makedirs("model", exist_ok=True)

    slugs = get_all_condition_slugs()
    print(f"Found {len(slugs)} conditions.")

    # Save the list for reuse
    with open("model/condition_slugs.json", "w", encoding="utf-8") as f:
        json.dump(slugs, f, indent=2)


if __name__ == "__main__":
    main()
