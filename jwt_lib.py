import jwt
import time
from typing import Dict
import os
import dotenv
import db

dotenv.load_dotenv()

JWT_SECRET = os.getenv("AUTHORIZATION_KEY_SECRET")
JWT_ALGORITHM = 'HS256'
SERIAL_KEY_SECRET = os.getenv("SERIAL_KEY_SECRET")

def generatetoken(username):
    return signJWT(username)
    
def verify_jwt(user,jwtoken: str) -> bool:
    try:
        payload = decodeJWT(jwtoken)
        if payload["expires"] <= time.time():
            db.set_token_exp(user,jwtoken)
    except:
        payload = None
    if payload:
        return True
    return False

def token_response(token: str):
    return {
        "access_token": token
    }
    
def signJWT(user: str) -> Dict[str, str]:
    payload = {
        "user": user,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}