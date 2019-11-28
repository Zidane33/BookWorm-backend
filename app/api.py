import requests
from .apiKey import KEY


def api():
    bookId = 'tcSMCwAAQBAJ?'
    url = "https://www.googleapis.com/books/v1/volumes/" + bookId + "key=" + KEY
    response = requests.get(url).json()
    return response['volumeInfo']['title']
