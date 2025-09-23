from email.mime import message
from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from llm_interface import ChatBackend
import os
import secrets
import markdown as md
from flask import Flask, send_from_directory

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
app.config['SESSION_TYPE'] = 'filesystem'

chatbot_backend = ChatBackend()

@app.route('/settings.json')
def settings_json():
    return send_from_directory('static', 'settings.json')
@app.route('/about.md')
def about_md():
    return send_from_directory('static', 'about.md')

def convert_history(raw_history):
    pairs = []
    curr_user = None
    for msg in raw_history:
        if msg["role"] == "user":
            curr_user = msg["content"]
        elif msg["role"] == "assistant" and curr_user is not None:
            pairs.append((curr_user, msg["content"]))
            curr_user = None
    return pairs

def render_messages_as_markdown(pairs):
    return [
        (md.markdown(pair[0], extensions=["tables", "fenced_code"], output_format="html5"),
         md.markdown(pair[1], extensions=["tables", "fenced_code"], output_format="html5"))
        for pair in pairs
    ]

@app.route("/", methods=["GET"])
def index():
    initial_history = chatbot_backend.get_history()
    history = convert_history(initial_history)
    # md_pairs = render_messages_as_markdown(history)
    return render_template("chat.html", history=history)

# def stream(input_text):
#     response = ""
#     for chunk in model.stream(input_text):
#         prev_len = len(response)
#         response += chunk.content
#         delta = response[prev_len:]
#         if delta:
#             yield delta

@app.route("/chat_stream", methods=['GET', 'POST'])
def chat_stream():
    if request.method == "POST":
        data = request.get_json()
        message = data.get("message", "")
        model_name = data.get("model")  # <-- get model sent by frontend
        print(f"model: {model_name}")
        return Response(chatbot_backend.predict(message, model_name=model_name), mimetype="text/event-stream")
    else:
        return Response(None, mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9060, debug=True)