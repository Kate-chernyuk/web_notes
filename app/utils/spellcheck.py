import requests


def check_spelling(text):
    url = "https://speller.yandex.net/services/spellservice.json/checkText"
    params = {
        "text": text,
        "lang": "ru",
        "format": "json"
    }

    response = requests.post(url, json=params)
    response.raise_for_status()

    return response.json()
