import requests

url = "https://paybox.com.co/settlement_accounts"

payload={}
files={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload, files=files)

print(response.text)
