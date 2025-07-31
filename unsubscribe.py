import requests

url = 'https://contact.useinsider.com/email/v1/unsubscribe'
api_key='asjdaskdj'
headers = {
    'X-PARTNER-NAME': 'clickbusbr',  
    'X-REQUEST-TOKEN': api_key,  
    'Content-Type': 'application/json'
}

data = {
    "email": "sample@useinsider.com"
}

response = requests.post(url, json=data, headers=headers)

print(response.status_code)
print(response.text)

