import time
import json
import requests
import logging
import os
from config import CCC_BASE_URL, TOKEN_ENDPOINT, USERNAME, PASSWORD, TOKEN_FILE

logger = logging.getLogger("CCC")

def authenticate():
    url = f"{CCC_BASE_URL}{TOKEN_ENDPOINT}"
    headers = {"Content-Type": "application/json"}
    try:
        logger.info("Authenticating with Catalyst Center...")
        response = requests.post(url, auth=(USERNAME, PASSWORD), headers=headers, verify=False)
        response.raise_for_status()
        token_data = {
            "access_token": response.json()["Token"],
            "expires_at": time.time() + 3600
        }
        save_token(token_data)
        logger.info("Authentication successful. Token saved.")
        return token_data["access_token"]
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during authentication: {e}")
        return None

def save_token(token_data):
    try:
        with open(TOKEN_FILE, "w") as f:
            json.dump(token_data, f)
        logger.debug("Token data saved to file.")
    except IOError as e:
        logger.error(f"Error saving token to file: {e}")

def load_token():
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, "r") as f:
                token_data = json.load(f)
            if token_data["expires_at"] > time.time():
                logger.debug("Valid token loaded from file.")
                return token_data["access_token"]
            else:
                logger.info("Token expired.")
        except (IOError, json.JSONDecodeError) as e:
            logger.error(f"Error loading token from file: {e}")
    else:
        logger.info("Token file not found.")
    return None

def get_access_token():
    token = load_token()
    if token:
        logger.info("Using cached token")
        return token
    else:
        logger.info("Cached token invalid or not found. Authenticating...")
        return authenticate()