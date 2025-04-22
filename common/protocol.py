# common/protocol.py

import json

def encode_message(type_, data=None):
    return json.dumps({"type": type_, "data": data}).encode('utf-8')

def decode_message(raw_message):
    try:
        message = json.loads(raw_message.decode('utf-8'))
        return message.get("type"), message.get("data")
    except json.JSONDecodeError:
        return None, None

# Message types
MSG_READY = "READY"
MSG_URL = "URL"
MSG_RESULT = "RESULT"
MSG_NO_MORE_WORK = "NO_MORE_WORK"
