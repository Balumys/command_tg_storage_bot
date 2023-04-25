import requests


def count_clicks(token, user_url):
    url_template = "https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary"
    url = url_template.format(user_url)
    authorization_params = {"Authorization": f"Bearer {token}"}
    payload = {"unit": "day",
               "units": "-1"}
    response = requests.get(url, params=payload, headers=authorization_params)
    response.raise_for_status()
    return response.json()["total_clicks"]


def shorten_link(token, user_url):
    url = "https://api-ssl.bitly.com/v4/bitlinks"
    authorization_params = {"Authorization": f"Bearer {token}"}
    payload = {"long_url": user_url}
    response = requests.post(url, json=payload, headers=authorization_params)
    response.raise_for_status()
    return response.json()["id"]
