import requests
import json
import socket
import os

# Use environment variables for configuration
API_URL = "https://ccp.netcup.net/run/webservice/servers/endpoint.php?JSON"
CUSTOMER_NUMBER = os.getenv("CUSTOMER_NUMBER")
API_KEY = os.getenv("API_KEY")
API_PASSWORD = os.getenv("API_PASSWORD")
DOMAIN = os.getenv("DOMAIN")
RECORD_NAME = os.getenv("RECORD_NAME", "@")  # Default to root record

# Functions
def return_variables():
    return API_KEY

def get_public_ip():
    """Fetch the current public IP address."""
    response = requests.get("https://api.ipify.org?format=json")
    response.raise_for_status()
    return response.json()["ip"]

def api_request(payload):
    """Send a request to the Netcup API."""
    headers = {"Content-Type": "application/json"}
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

def login():
    """Log in to the Netcup API and retrieve a session ID."""
    payload = {
        "action": "login",
        "param": {
            "customernumber": CUSTOMER_NUMBER,
            "apikey": API_KEY,
            "apipassword": API_PASSWORD
        }
    }
    response = api_request(payload)
    if response["status"] != "success":
        raise Exception(f"Login failed: {response['longmessage']}")
    return response["responsedata"]["apisessionid"]

def get_dns_records(session_id):
    """Fetch DNS records for the domain."""
    payload = {
        "action": "infoDnsRecords",
        "param": {
            "customernumber": CUSTOMER_NUMBER,
            "apikey": API_KEY,
            "apisessionid": session_id,
            "domainname": DOMAIN
        }
    }
    response = api_request(payload)
    if response["status"] != "success":
        raise Exception(f"Failed to fetch DNS records: {response['longmessage']}")
    return response["responsedata"]["dnsrecords"]

def update_dns_record(session_id, record, new_ip):
    """Update a specific DNS record."""
    record["destination"] = new_ip
    payload = {
        "action": "updateDnsRecords",
        "param": {
            "customernumber": CUSTOMER_NUMBER,
            "apikey": API_KEY,
            "apisessionid": session_id,
            "domainname": DOMAIN,
            "dnsrecordset": {"dnsrecords": [record]}
        }
    }
    response = api_request(payload)
    if response["status"] != "success":
        raise Exception(f"Failed to update DNS record: {response['longmessage']}")
    print("DNS record updated successfully.")

def logout(session_id):
    """Log out from the Netcup API."""
    payload = {
        "action": "logout",
        "param": {
            "customernumber": CUSTOMER_NUMBER,
            "apikey": API_KEY,
            "apisessionid": session_id
        }
    }
    response = api_request(payload)
    if response["status"] != "success":
        print(f"Logout failed: {response['longmessage']}")
    else:
        print("Logged out successfully.")

# Main script
def main():
    try:
        current_ip = get_public_ip()
        print(f"Current public IP: {current_ip}")

        session_id = login()
        print("Logged in successfully.")

        dns_records = get_dns_records(session_id)
        print("Fetched DNS records.")

        for record in dns_records:
            if record["hostname"] == RECORD_NAME:
                if record["destination"] == current_ip:
                    print("DNS record is already up-to-date.")
                else:
                    print(f"Updating DNS record for {RECORD_NAME} to {current_ip}.")
                    update_dns_record(session_id, record, current_ip)
                break
        else:
            print(f"No DNS record found for {RECORD_NAME}.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if 'session_id' in locals():
            logout(session_id)

if __name__ == "__main__":
    main()
