import requests
import logging
from auth import get_access_token
from config import CCC_BASE_URL

logger = logging.getLogger("CCC")

def api_request(url, method="GET", params=None, data=None):
    token = get_access_token()
    full_url = CCC_BASE_URL + url
    if not token:
        logger.critical("No valid token found. Cannot make API request.")
        return None
    
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": token
    }

    methods = {
        "GET": requests.get,
        "POST": requests.post,
    }

    if method not in methods:
        logger.error(f"Invalid HTTP method: {method}")
        return None

    try:
        logger.info(f"Making {method} request to {full_url} with params {params} and data {data}")
        response = methods[method](full_url, headers=headers, params=params, json=data, verify=False)
        response.raise_for_status()
        logger.info(f"Successful {method} API call with status code {response.status_code}")
        return response.json().get("response", []) 
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        return None