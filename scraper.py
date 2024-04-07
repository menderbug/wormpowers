import requests
import bs4
import os
import re

from urllib.parse import urljoin


def get_powers(url):
    print(f"starting {url}")
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    abilities_and_powers_header = soup.find(
        "span", id=lambda x: isinstance(x, str) and "abilities" in x.lower()
    )

    # If the "Abilities and Powers" header is found, find the next <h2> tag
    if not abilities_and_powers_header:
        return

    next_h2 = abilities_and_powers_header.find_next("h2")

    character_element = soup.find("span", {"class": "mw-page-title-main"}) or soup.find(
        "h1", {"class": "page-header__title"}
    )
    character_name = character_element.get_text(strip=True)

    # Initialize an empty list to store the text content
    contents = [f"# {character_name}"]

    # Iterate over the elements between the headers and extract their text content
    current_element = abilities_and_powers_header.find_next()
    while current_element and current_element != next_h2:
        for sup in current_element.find_all("sup"):
            sup.extract()

        # Extract headings (<h3>, <h4>, etc.) and <p> tags
        if current_element.name == "p":
            contents.append(current_element.get_text())

        if current_element.name.startswith("h"):
            span = current_element.find("span")
            contents.append(f"## {span.get_text()}")

        current_element = current_element.find_next()

    # Join the extracted text content into a single string
    result = "\n".join(contents)
    result = re.sub(r"\bwas\b", "is", result)
    result = re.sub(r"\bhad\b", "has", result)
    filename = os.path.join(directory, f"{character_name}.md")
    with open(filename, "w", encoding="utf-8") as file:
        file.write(result)


directory = "Characters"
if not os.path.exists(directory):
    os.makedirs(directory)


URLS = [
    "https://worm.fandom.com/wiki/Category:Characters",
    "https://worm.fandom.com/wiki/Category:Characters?from=Eric+Kingston",
    "https://worm.fandom.com/wiki/Category:Characters?from=Murder+Rat",
    "https://worm.fandom.com/wiki/Category:Characters?from=Murder+Rat",
]
for url in URLS:
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    for tag in soup.find_all("a", {"class": "category-page__member-link"}):
        link = tag.get("href")
        get_powers(urljoin(url, link))
