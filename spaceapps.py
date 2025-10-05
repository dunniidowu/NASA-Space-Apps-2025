import pandas as pd
import csv
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup

df = pd.read_csv("~/Downloads/SB_publication_PMC.csv")
links = df["Link"].dropna().tolist()
print(f"Found {len(links)} links")

def extract_info_from_webpage(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.462.99 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        url_text = response.text
        soup = BeautifulSoup(url_text, 'html.parser')
        authors = set(soup.find_all('span', class_='name western'))
        author_list = list(authors)
        cleaned_authors = []
        for author in tqdm(author_list):
            try:
                author_name = str(author).split(">")[1].split("<")[0]
            except:
                pass
            cleaned_authors.append(author_name)
        title = soup.find('h1')
        abstract = soup.find('section', class_='abstract').text.strip() if soup.find('section', class_='abstract') else 'no abstract found'
        references = soup.find_all('cite')
        cleaned_references = []
        for reference in references:
            cleaned_reference = str(reference).split(">")[1].split("<")[0]
            cleaned_references.append(cleaned_reference)
        return cleaned_authors, cleaned_references, abstract, title
    
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return "error", "error"

csv_data = [["Title", "Authors", "References", "Abstract", "Link"]]   
for link in tqdm(links):
    link_authors, link_references, link_abstract, link_title = extract_info_from_webpage(link)
    link_list = [link_title, link_authors, link_references, link_abstract, link]
    csv_data.append(link_list)

with open("output.csv", "w") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerows(csv_data)
