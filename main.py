from flask import Flask, request, jsonify
from dotenv import load_dotenv
import time
import json
from handler.message_handler import *

load_dotenv()
app = Flask(__name__)

# In-memory chat buffer per user (use Redis or DB in prod)
chat_buffers = {}
last_message_time = {}
BUFFER_TIMEOUT = 180  # 3 minutes


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    # Ensure data is not None
    if data is None:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    # Decrypt if encrypted
    if isinstance(data, dict) and "encrypt" in data:
        try:
            data = decrypt_lark_message(data["encrypt"])
        except Exception as e:
            return jsonify({"error": f"Failed to decrypt message: {str(e)}"}), 400

    # Lark challenge verification
    if isinstance(data, dict) and data.get("type") == "url_verification":
        return jsonify({"challenge": data.get("challenge")})

    # Lark event handling
    print(data)
    event = data.get("event", {}) if isinstance(data, dict) else {}
    message = event.get("message", {}) if isinstance(event, dict) else {}
    chat_id = message.get("chat_id", {}) if isinstance(message, dict) else None
    content_json = message.get("content", {}) if isinstance(message, dict) else None
    user_id = event.get("sender", {}).get("sender_id", {}).get("open_id")

    if not user_id or not content_json:
        return jsonify({"error": "No Content or No User Id"}), 400

    now = time.time()
    # Reset buffer if 3 minutes is out!
    if (
        user_id in last_message_time
        and now - last_message_time[user_id] > BUFFER_TIMEOUT
    ):
        chat_buffers[user_id] = []

    last_convo = json.loads(content_json).get("text", "")
    convo_dict = {chat_id: last_convo}
    # Handle idempotency. Lark sends the same event more than once
    print(chat_buffers)
    if user_id in chat_buffers and convo_dict in chat_buffers[user_id]:
        return "OK"

    chat_buffers.setdefault(user_id, []).append(convo_dict)
    last_message_time[user_id] = now
    # Extract all values from each dictionary
    # chat_buffers structure >> user_id: [{chat_id: "hey"}]
    convo_list = [value for d in chat_buffers[user_id] for value in d.values()]
    full_convo = "\n".join(convo_list)

    if detect_jd_intent(full_convo):
        job_info = extract_job_info(full_convo)
        jd_text = generate_job_description(job_info)
        send_lark_card(jd_text, chat_id)
        return jsonify({"status": "JD sent"})
    else:
        return jsonify({"status": "buffered"})


@app.route("/")
def index():
    return "Lark bot is running!"


if __name__ == "__main__":
    app.run(port=3000)
