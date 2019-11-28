import requests


KEY = 'Cc5azpsc8j0fATmIxBfhDw'


def api():
    response = requests.get("https://www.goodreads.com/book/review_counts.json",
                            params={"key": KEY, "isbns": "9781632168146"}).json()
    data = response['books'][0]['ratings_count']
    return str(data)
