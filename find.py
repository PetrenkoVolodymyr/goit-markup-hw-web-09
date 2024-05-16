import re

from typing import Any
from redis_lru import RedisLRU

from models import Author, Quote

def find_by_tag(tag: str) -> list[str | None]:
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result

def find_by_author(author: str) -> list[list[Any]]:
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result


if __name__ == '__main__':
   
    while True:
        request = input('Please input "name: "+ full/part of name OR "tag" + full/ part of tag -> ')

        text = request.split()[0]
        pattern = r"\w+"
        match = re.search(pattern, text)
        command = match.group()

        try: 
            text = request.split()[1]
            words_list = text.split(",")
        except:
            pass

        match command:
            case "name":
                print(find_by_author(words_list[0]))
            case "tag":
                print(find_by_tag(words_list[0]))
            case "tags":
                result = []
                for word in words_list:
                    result.append(find_by_tag(word)[0])
                print(result)
            case "exit":
                break
            case _:
                print("Unknown command")

