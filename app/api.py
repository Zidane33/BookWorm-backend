import requests


def isField(endpoint, field):
    try:
        data = endpoint[field]
        return data
    except KeyError:
        return 'Not Found'


def search(query):
    url = f'https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=40'
    response = requests.get(url).json()
    return response


def searchCite(query):
    url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{query}'
    response = requests.get(url).json()
    return response


def api(bookId):
    url = f"https://www.googleapis.com/books/v1/volumes/{bookId}"
    response = requests.get(url).json()

    title = isField(response['volumeInfo'], 'title')
    author = isField(response['volumeInfo']['authors'], 0)
    image = isField(response['volumeInfo']['imageLinks'], 'thumbnail')
    description = isField(response['volumeInfo'], 'description')
    publishDate = isField(response['volumeInfo'], 'publishedDate')
    publisher = isField(response['volumeInfo'], 'publisher')
    try:
        isbn = response['volumeInfo']['industryIdentifiers'][0]['identifier']
    except KeyError:
        isbn = "Not Found"

    data = {'title': title,
            'author': author,
            'description': description,
            'image': image,
            'isbn': isbn,
            'publishDate': publishDate,
            'publisher': publisher}
    return data
