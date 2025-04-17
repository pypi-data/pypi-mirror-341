import requests

API_KEY = "18ed5e66a7msh9f4b2dcea69f606p1dc970jsnd09db62aaec1"

def download_media(url):
    endpoint = "https://zm-api.p.rapidapi.com/v1/social/autolink"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "zm-api.p.rapidapi.com",
        "content-type": "application/json"
    }
    params = {"url": url}
    response = requests.get(endpoint, headers=headers, params=params)
    return response.json()
