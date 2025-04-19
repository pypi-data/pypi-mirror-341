import time
from sys import exit as bye
from sys import argv
import json
import requests

# Endpoints definition
API_SERVER = "https://apix.cisco.com/api/services"
SUMMARY_ENDPOINT = "/assets-and-entitlement/v1/licenses/summary"
ENTITLEMENTS_ENDPOINT = "/assets-and-entitlement/v1/licenses/entitlements"
STATUS_ENDPOINT = "/assets-and-entitlement/v1/request/status"
REPORT_ENDPOINT = "/assets-and-entitlement/v1/request/report"
AUTH_ENDPOINT = "https://id.cisco.com/oauth2/default/v1/token"

# Function to get token
def get_token(client, secret):
    token_data = {
        "grant_type": "client_credentials",
        "client_id": client,
        "client_secret": secret
    }
    token_resp = requests.post(AUTH_ENDPOINT, data=token_data, timeout=30)
    if token_resp.status_code == 200:
        token_id = token_resp.json().get("access_token")
        print("Token generated successfully.")
        return token_id
    else:
        print("Credentials not accepted.")
        return None

# Function to submit summary request
def submit_sum_req(tokn, smartaccount):
    req_headers = {
        "Authorization": f"Bearer {tokn}",
        "Content-Type": "application/json"
    }
    req_data = json.dumps({
        "smartAccount": f"{smartaccount}"
    })
    req_resp = requests.post(f"{API_SERVER}{SUMMARY_ENDPOINT}", headers=req_headers, data=req_data, timeout=30)
    if req_resp.status_code == 202:
        req_id = req_resp.json().get("requestId")
        req_message = req_resp.json().get("message")
        print(f"Message: {req_message}")
        print(f"Request ID: {req_id}")
        return req_id
    else:
        print("Failed to retrieve summary", req_resp.status_code)
        return None

# Function to submit entitlements request
def submit_ent_req(tokn, smartaccount):
    req_headers = {
        "Authorization": f"Bearer {tokn}",
        "Content-Type": "application/json"
    }
    req_data = json.dumps({
        "smartAccount": f"{smartaccount}",
        "request": "Full"
    })
    req_resp = requests.post(f"{API_SERVER}{ENTITLEMENTS_ENDPOINT}", headers=req_headers, data=req_data, timeout=30)
    if req_resp.status_code == 202:
        req_id = req_resp.json().get("requestId")
        req_message = req_resp.json().get("message")
        print(f"Message: {req_message}")
        print(f"Request ID: {req_id}")
        return req_id
    else:
        print("Failed to retrieve entitlements", req_resp.status_code)
        return None

# Function to get file URL
def get_file_url(tokn, request_id):
    req_headers = {
        "Authorization": f"Bearer {tokn}",
        "Content-Type": "application/json"
    }
    req_data = json.dumps({
        "requestId": request_id,
        "responseType": 1
    })
    print("Getting file URL...")
    req_resp = requests.post(f"{API_SERVER}{REPORT_ENDPOINT}", headers=req_headers, data=req_data, timeout=30)
    if req_resp.status_code == 200:
        file_url = req_resp.json().get("preSignedURL")[0]
        print(f"The file is ready. Please use the following URL to download the file:\n{file_url}")
        print("Exiting now...")
        return file_url
    else:
        print("Failed to retrieve file", req_resp.status_code)
        return None

# Function to check request status and get file URL
def check_req_status(tokn, request_id):
    req_data = json.dumps({
        "requestId": request_id
    })
    req_headers = {
        "Authorization": f"Bearer {tokn}",
        "Content-Type": "application/json"
    }
    time.sleep(5)
    while True:
        req_resp = requests.post(f"{API_SERVER}{STATUS_ENDPOINT}", headers=req_headers, data=req_data, timeout=30)
        if req_resp.status_code == 200:
            status_code = req_resp.json().get('requests')[0]['requestStatus']
            status_message = req_resp.json().get("message")
            print(f"Message: {status_message}")
            print(f"Request Status: {status_code}")
            if status_code == "COMPLETED":
                time.sleep(3)
                url_resp = get_file_url(tokn, request_id)
                return url_resp
            print("Request not completed yet. Retrying in 30 seconds...")
            time.sleep(30)
        else:
            print("Failed to retrieve request status")
            bye()

if __name__ == "__main__":
    if len(argv) != 4:
        print("Usage: python script.py <client id> <client secret> <sa id>")
        exit(1)

    c_id = argv[1]
    c_secret = argv[2]
    sa_id = argv[3]

    choice = input("Enter '1' to download Summary file or '2' to download Entitlement file: ")

    token = get_token(c_id, c_secret)

    if choice == '1':
        request_id = submit_sum_req(token, sa_id)
    elif choice == '2':
        request_id = submit_ent_req(token, sa_id)
    else:
        print("Invalid choice. Exiting.")
        exit(1)

    check_req_status(token, request_id)
