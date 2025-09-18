from dotenv import load_dotenv
import sys
import os

load_dotenv()

# Get config from .env file
API_ID = os.getenv("API_ID") or 'your_api_id'       
try:
    API_ID = int(API_ID)

except ValueError:
    print("Khata: Dar file config.py shoma API_ID sahih ra vared nakr did chon adad nist")
    sys.exit(1)

API_HASH = os.getenv("API_HASH") or 'your_api_hash'  

SESSION_NAME = os.getenv("API_HASH") or 'check_session'  

checked_username = "@Sobhan_SRZA"