import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get endpoint and key from environment variables
endpoint = os.environ.get('CONTENT_UNDERSTANDING_ENDPOINT')
key = os.environ.get('CONTENT_UNDERSTANDING_KEY')

analyzer_name = 'travel-insurance-analyzer'
document_url = 'https://github.com/microsoftlearning/mslearn-ai-document-intelligence/raw/main/Labfiles/05-content-understanding/forms/rest-form.pdf'

cu_version = '2024-12-01-preview'

# Validate environment variables are set
if not endpoint or not key:
    raise ValueError("CONTENT_UNDERSTANDING_ENDPOINT and CONTENT_UNDERSTANDING_KEY must be set in the .env file")

body = {
    "url": document_url
}

headers = {
    "Ocp-Apim-Subscription-Key": key,
    "Content-Type": "application/json"
}

url = endpoint + f'contentunderstanding/analyzers/{analyzer_name}:analyze?api-version={cu_version}'

print ('Analyzing document...')
response = requests.post(url, headers=headers, data=json.dumps(body))

print(response.status_code)
response_json = response.json()

# Extract the "id" value from the response
id_value = response_json.get("id")

# Perform a GET request t get the results
print ('Getting results...')
result_url = f'{endpoint}contentunderstanding/analyzers/{analyzer_name}/results/{id_value}?api-version={cu_version}'
result_response = requests.get(result_url, headers=headers)
print(result_response.status_code)

status = result_response.json().get("status")
while status == "Running":
    print('...')
    result_response = requests.get(result_url, headers=headers)
    status = result_response.json().get("status")

if status == "Succeeded":
    print("Analysis succeeded.")
    results = result_response.json()
    # Print formatted JSON with indentation
    print(json.dumps(results, indent=2))

