import requests
from bs4 import BeautifulSoup
import csv
import openai
import os

def call_openai_chat(prompt):
    openai.api_type = "azure"
    openai.api_key = os.environ["OPENAI_API_KEY"]
    openai.api_base = os.environ('OPENAI_API_ENDPOINT')
    openai.api_version = "2023-03-15-preview"

    try:
        response = openai.ChatCompletion.create(
          engine=os.environ('OPENAI_ENGINE'),
          model="gpt-3.5-turbo",  # specify the model you want to use
          messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return str(e)

def call_ai_service_for_classification(description):
    return call_openai_chat("Please categorize the following description as `GA`, `Preview`, or `Retire`: " + description)

def call_ai_service_for_product_name(description):
    return call_openai_chat("Please return the name of the Microsoft service (e.g., `Azure Kubernetes Service` that the following description is about (Only return a single name of the service and nothing else): " + description)

def fetch_and_parse_html(url):
    # Fetch HTML content from the URL
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the website")
        return None

    # Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def extract_information(soup):
    # Find all update rows
    updates = soup.find_all("div", class_="row update-row row-size6")

    extracted_data = []
    for update in updates:
        # Extract date
        date_element = update.find("div", class_="column medium-1")
        date = date_element.text.strip() if date_element else "No Date"

        # Extract title
        title_element = update.find("h3", class_="text-body2")
        title = title_element.text.strip() if title_element else "No Title"

        # Extract availability status
        status_element = update.find("span", class_="status-indicator__label")
        status = status_element.text.strip() if status_element else "No Status"

        # Extract description (excluding the specific paragraph you mentioned)
        description_paragraphs = update.find_all("p")
        description = ' '.join(p.text.strip() for p in description_paragraphs if "Target availability:" not in p.text)
        #description = ' '.join(p.text.strip() for p in description_paragraphs if "ターゲット可用性:" not in p.text)
        
        extracted_data.append([date, title, status, description])

    return extracted_data

def write_to_csv(data, filename="azure_updates.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)

def main():
    base_url = "https://azure.microsoft.com/en-us/updates/?Page="
    all_data = []

    startpage = 1
    for page in range(startpage, 9):  # Looping through pages
        full_url = base_url + str(page)
        soup = fetch_and_parse_html(full_url)
        if soup:
            page_data = extract_information(soup)
            all_data.extend(page_data)
        else:
            print(f"No data found for page {page}")

    if (True):
        for data_row in all_data:
            description = data_row[3]  # Assuming description is the fourth element

            # Call AI service for classification
            classification = call_ai_service_for_classification(description)
            data_row.append(classification)

            # Call AI service for product name
            product_name = call_ai_service_for_product_name(description)
            data_row.append(product_name)

    write_to_csv(all_data)

if __name__ == "__main__":
    main()
