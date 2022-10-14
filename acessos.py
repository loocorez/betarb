import requests, json

def get_url(url: str, headers:json) -> json:
    return (requests.get(url=url, headers=headers).json())

def post_url(url: str, headers:json, data: json):
    response = requests.post(url=url, json=data, headers=headers)
    return response.json()
