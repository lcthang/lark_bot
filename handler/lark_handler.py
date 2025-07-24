from dataclasses import dataclass
import json
import requests
import os
import base64
import hashlib
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

LARK_URL = "https://open.larksuite.com/open-apis"
# Lark App credentials
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
VERIFICATION_TOKEN = os.getenv("VERIFICATION_TOKEN")
ENCRYPT_KEY = os.getenv("ENCRYPT_KEY")


# --- Step 4: Generate Lark Message Card ---
def send_lark_card(jd_text, chat_id):
    card = create_lark_card(jd_text)
    # Send a reply to the user in Lark
    url = "%s/im/v1/messages?receive_id_type=chat_id" % LARK_URL
    headers = {
        "Authorization": "Bearer %s" % get_tenant_access_token(),
        "Content-Type": "application/json; charset=utf-8",
    }
    content = json.dumps(card)
    body = {"msg_type": "interactive", "content": content, "receive_id": chat_id}
    requests.post(url, headers=headers, json=body)


def create_lark_card(jd_text):
    return {
        "config": {"wide_screen_mode": True},
        "elements": [
            {
                "tag": "markdown",
                "content": jd_text,  # Lark card content limit
            },
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {"tag": "plain_text", "content": "Copy JD"},
                        "type": "primary",
                        "value": {"copy_text": jd_text},
                    }
                ],
            },
        ],
    }


def get_company_name():
    url = f"{LARK_URL}/tenant/v2/tenant/query"
    headers = {
        "Authorization": f"Bearer {get_tenant_access_token()}",
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # The company name is usually in data['data']['tenant']['name']
        return data.get("data", {}).get("tenant", {}).get("name")
    else:
        print("Failed to get company name:", response.text)
        return None


def get_tenant_access_token():
    url = "%s/auth/v3/tenant_access_token/internal" % LARK_URL
    body = {"app_id": APP_ID, "app_secret": APP_SECRET}
    resp = requests.post(url, json=body)
    return resp.json().get("tenant_access_token")


def decrypt_lark_message(encrypted: str) -> dict:
    # Step 1: Decode the base64 input
    encrypted_bytes = base64.b64decode(encrypted)
    # Step 2: Derive a 32-byte AES key from the ENCRYPT_KEY using SHA-256
    if ENCRYPT_KEY is None:
        raise ValueError("ENCRYPT_KEY is not set")
    key_bytes = hashlib.sha256(str(ENCRYPT_KEY).encode()).digest()
    # Step 3: Extract IV (first 16 bytes) and ciphertext (rest)
    iv = encrypted_bytes[:16]
    ciphertext = encrypted_bytes[16:]
    # Step 4: Decrypt using AES-256-CBC
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    decrypted_padded = cipher.decrypt(ciphertext)
    # Step 5: Unpad using PKCS7
    decrypted_bytes = unpad(decrypted_padded, AES.block_size)
    # Step 6: Parse as JSON
    return json.loads(decrypted_bytes.decode("utf-8"))


def send_lark_reply(event, text):
    # Send a reply to the user in Lark
    message_id = event["message"]["message_id"]
    url = "%s/im/v1/messages/%s/reply" % (LARK_URL, message_id)
    headers = {
        "Authorization": "Bearer %s" % get_tenant_access_token(),
        "Content-Type": "application/json",
    }
    content = json.dumps({"text": text})
    body = {"msg_type": "text", "content": content}
    requests.post(url, headers=headers, json=body)
