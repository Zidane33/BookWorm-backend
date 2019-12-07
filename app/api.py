import requests
from .apiKey import KEY


def search(query):
    url = f'https://www.googleapis.com/books/v1/volumes?q={query}'
    response = requests.get(url).json()
    result = []
    for book in response['items']:
        result.append(book['volumeInfo']['title'])
    return result


def api(bookId):
    bookId = 'tcSMCwAAQBAJ?'
    url = f"https://www.googleapis.com/books/v1/volumes/{bookId}key={KEY}"
    response = requests.get(url).json()
    data = {'title': response['volumeInfo']['title'],
            'author': response['volumeInfo']['authors'][0],
            'categories': response['volumeInfo']['categories'][0],
            'description': response['volumeInfo']['description'],
            'image': response['volumeInfo']['imageLinks']['medium'],
            'isbn': response['volumeInfo']['industryIdentifiers'][0]['identifier'],
            'publishDate': response['volumeInfo']['publishedDate']}
    return data
    # return response
