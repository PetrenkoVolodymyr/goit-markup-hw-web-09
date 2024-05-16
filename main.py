import json
import requests
from bs4 import BeautifulSoup


url = 'https://quotes.toscrape.com/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

quotes =[]
authors=[]
parts = soup.find_all('div', class_='quote')

for part in parts:
    quote={}
    quote_text= part.find('span', class_='text').text.strip(u'\u201c\u201d')  
    author= part.find('small', class_='author').text
    tags=[]
    all_tags= part.find_all('a', class_='tag')
    for tag in all_tags:
        tags.append(tag.text)
    quote.update({"tags":tags, "author":author,"quote": quote_text})
    quotes.append(quote)


    details_link= part.find('a')["href"]
    details_link=url+details_link
    response_authors = requests.get(details_link)
    soup_authors = BeautifulSoup(response_authors.text, 'lxml')

    about={}
    name = soup_authors.find('h3').text
    born = soup_authors.find('span', class_='author-born-date').text
    location = soup_authors.find('span', class_='author-born-location').text
    description = soup_authors.find('div', class_='author-description').text.strip()

    repeated = "false"
    for el in authors:
        if el["fullname"] == name:
            repeated ="true"
            break
    if repeated != "true":
        about.update({"fullname":name, "born_date":born,"born_location": location,"description":description})
        authors.append(about)
    try:
        authors[0]
    except:
        about.update({"fullname":name, "born_date":born,"born_location": location,"description":description})
        authors.append(about)

    has = soup.find('li', class_='next') is not None
    print(has)


with open("authors.json", "w",encoding='utf-8') as f:
    json.dump(authors, f, indent=2)

with open("qoutes.json", "w",encoding='utf-8') as f:
    json.dump(quotes, f, indent=2)
