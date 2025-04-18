import hashlib
import hmac
import base64
from yayawallet_python_sdk.functions.get_api_secret import get_api_secret

def generate_signature(timestamp, method, endpoint, body, api_key):
    prehash_string = timestamp + method + endpoint + body
    api_secret = get_api_secret(api_key)
    
    if api_secret is None:
        raise ValueError("API secret not found in database")
        
    hashed_key = hmac.new(bytes(api_secret, 'UTF-8'), msg=bytes(prehash_string, 'UTF-8'), digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(hashed_key).decode()
    return signature