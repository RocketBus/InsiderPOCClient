import requests
import base64

workspace_id = 'ZEU740S3GCT03DH6RQ2EU96I'
api_secret = 'E37E38881AA44365B3ED106F'

api_key = f'{workspace_id}_{api_secret}'
print(api_key)

string_to_encode = f'{api_key}:'
encoded_bytes = base64.b64encode(string_to_encode.encode('utf-8'))
base64_string = encoded_bytes.decode('utf-8')
print(f"Base64 encoded: {base64_string}")

auth = 'Basic ' + base64_string

headers = {
    'Content-Type': 'application/json',
    'Authorization': auth
}

data = {
    "email": "maria@examplepet.com",
    "first_name": "Maria",
    "last_name": "Silva",
    "u_mb": "+5511983659987",
    "moe_ip_city": "São Paulo/SP",
    "moe_ip_country": "Brazil",
    "moe_sub_w": True
}

url = f'https://api-01.moengage.com/v1/customer/ZEU740S3GCT03DH6RQ2EU96I'

try:
    response = requests.post(url, json=data, headers=headers)

    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Body: {response.text}")

    # Check if request was successful
    if response.status_code == 200:
        print("✅ Customer attributes updated successfully!")
    else:
        print(f"❌ Request failed with status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Request failed with error: {e}")