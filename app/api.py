import requests
# from .apiKey import KEY


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


def api(bookId):
    url = f"https://www.googleapis.com/books/v1/volumes/{bookId}"
    response = requests.get(url).json()

    title = isField(response['volumeInfo'], 'title')
    author = isField(response['volumeInfo']['authors'], 0)
    image = isField(response['volumeInfo']['imageLinks'], 'thumbnail')
    description = isField(response['volumeInfo'], 'description')
    publishDate = isField(response['volumeInfo'], 'publishedDate')
    try:
        isbn = isField(response['volumeInfo']['industryIdentifier'][0]['identifer'])
    except KeyError:
        isbn = "Not Found"

    data = {'title': title,
            'author': author,
            'description': description,
            'image': image,
            'isbn': isbn,
            'publishDate': publishDate}
    return data
