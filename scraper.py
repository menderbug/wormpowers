
import requests
import bs4
import html2text
import os

from urllib.parse import urljoin



def get_powers(url):
    print(f"starting {url}")
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    abilities_and_powers_header = soup.find("span", id=lambda x: isinstance(x, str) and "abilities" in x.lower())
    character_name = soup.find("span", {"class": "mw-page-title-main"}).get_text()

    # Initialize an empty list to store the text content
    contents = [f"# {character_name}"]

    # If the "Abilities and Powers" header is found, find the next <h2> tag
    if abilities_and_powers_header:
        next_h2 = abilities_and_powers_header.find_next("h2")

        # Iterate over the elements between the headers and extract their text content
        current_element = abilities_and_powers_header.find_next()
        while current_element and current_element != next_h2:
            for sup in current_element.find_all("sup"):
                sup.extract()
            
            # Extract headings (<h3>, <h4>, etc.) and <p> tags
            if current_element.name == 'p':
                contents.append(current_element.get_text())
            
            if current_element.name.startswith('h'):
                span = current_element.find("span")
                contents.append(f"## {span.get_text()}")
            
            current_element = current_element.find_next()

    # Join the extracted text content into a single string
    result = "\n".join(contents)
    filename = os.path.join(directory, f"{character_name}.md")
    with open(filename, "w", encoding="utf-8") as file:
        file.write(result)


directory = "Characters"
if not os.path.exists(directory):
    os.makedirs(directory)


URL = "https://worm.fandom.com/wiki/Character_Reference_Sheet"
response = requests.get(URL)
soup = bs4.BeautifulSoup(response.text, "html.parser")
for row in soup.find_all("th"):
    tag = row.find("a")
    if tag:
        link = tag.get("href")
        get_powers(urljoin(URL, link)) 
