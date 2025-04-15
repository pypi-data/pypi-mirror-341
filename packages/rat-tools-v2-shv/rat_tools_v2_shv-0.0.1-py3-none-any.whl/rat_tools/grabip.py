import requests


def getip():
    api = "https://api.ipify.org/?format=text"
    return requests.get(api).text
