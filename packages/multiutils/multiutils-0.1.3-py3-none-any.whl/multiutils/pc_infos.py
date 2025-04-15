import requests

def get_ip() -> str:
    return requests.get("https://api.ipify.org").text
