from pymongo import MongoClient, errors
import requests
import json
from bs4 import BeautifulSoup

main_url = "https://quotes.toscrape.com/"


def get_author_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    full_name = soup.select("h3.author-title")[0].text.strip()
    birth_date = soup.select("span.author-born-date")[0].text.strip()
    born_location = soup.select("span.author-born-location")[0].text.strip()
    description = soup.select("div.author-description")[0].text.strip()

    return {
        "fullname": full_name,
        "born_date": birth_date,
        "born_locatione": born_location,
        "description": description,
    }


quotes_data = []
authors_data = []
unique_authors = set()

page = 1

while True:
    response = requests.get(f"{main_url}page/{page}")
    if "No quotes found!" in response.text:
        break
    soup = BeautifulSoup(response.text, "html.parser")
    quotes = soup.select("div.quote")
    for quote in quotes:
        text = quote.find("span", class_="text").text.strip()
        author = quote.find("small", class_="author").text.strip()
        tags = [tag.text.strip() for tag in quote.find_all("a", class_="tag")]

        quotes_data.append({"tags": tags, "author": author, "quote": text})

        if author not in unique_authors:
            author_url = main_url + quote.find("a")["href"]
            author_details = get_author_info(author_url)
            authors_data.append(author_details)
            unique_authors.add(author)

    page += 1


with open("quotes.json", "w", encoding="utf-8") as quotes_file:
    json.dump(quotes_data, quotes_file, indent=4)

with open("authors.json", "w", encoding="utf-8") as authors_file:
    json.dump(authors_data, authors_file, indent=4)


def import_data_to_mongo():
    try:
        client = MongoClient("mongodb+srv://realmalque:amlque123321@cluster0.fofyqea.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
        db = client["Parsing"]
        quotes_collection = db["Quotes"]
        authors_collection = db["Authors"]

        with open("quotes.json", "r", encoding="utf-8") as quotes_file:
            quotes_data = json.load(quotes_file)
            if quotes_data:
                quotes_collection.insert_many(quotes_data)

        with open("authors.json", "r", encoding="utf-8") as authors_file:
            authors_data = json.load(authors_file)
            if authors_data:
                authors_collection.insert_many(authors_data)

        print("Data successfully imported to MongoDB.")

    except errors.BulkWriteError as bwe:
        print(f"Bulk Write Error: {bwe.details}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # print(get_author_details("https://quotes.toscrape.com/author/Albert-Einstein/"))
    import_data_to_mongo()