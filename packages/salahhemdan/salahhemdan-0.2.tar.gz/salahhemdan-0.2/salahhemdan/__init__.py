import requests

# مفتاح ثابت داخل المكتبة
API_KEY = "18ed5e66a7msh9f4b2dcea69f606p1dc970jsnd09db62aaec1"

def download_media(url: str):
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "zm-api.p.rapidapi.com"
    }
    params = {"url": url}
    api_url = "https://zm-api.p.rapidapi.com/instagram"

    response = requests.get(api_url, headers=headers, params=params)
    response.raise_for_status()

    return response.json()