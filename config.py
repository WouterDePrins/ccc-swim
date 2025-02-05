import os
from dotenv import load_dotenv
load_dotenv() 

CCC_BASE_URL = os.getenv("CCC_BASE_URL", "")
USERNAME = os.getenv("CCC_USERNAME", "")
PASSWORD = os.getenv("CCC_PASSWORD", "")
TOKEN_ENDPOINT = "/dna/system/api/v1/auth/token"
TOKEN_FILE = "ccc_token.json"
SCHEDULE_FILE = os.getenv("SCHEDULE_FILE", "")
