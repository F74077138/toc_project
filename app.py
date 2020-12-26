import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["user", "greeting", "options", "list", "genre", "new", "cartoon", "showgenre", "cancel", "about"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "greeting",
            "conditions": "is_going_to_greeting",
        },
        {
            "trigger": "advance",
            "source": "greeting",
            "dest": "greeting",
            "conditions": "is_going_to_greeting",
        },
        {
            "trigger": "advance",
            "source": "greeting",
            "dest": "options",
            "conditions": "is_going_to_options",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "options",
            "conditions": "is_going_to_options",
        },
        {
            "trigger": "advance",
            "source": "options",
            "dest": "options",
            "conditions": "is_going_to_options",
        },
        {
            "trigger": "advance",
            "source": "options",
            "dest": "new",
            "conditions": "is_going_to_new",
        },
        {
            "trigger": "advance",
            "source": "options",
            "dest": "list",
            "conditions": "is_going_to_list",
        },
        {
            "trigger": "advance",
            "source": "options",
            "dest": "genre",
            "conditions": "is_going_to_genre",
        },
        {
            "trigger": "advance",
            "source": "options",
            "dest": "about",
            "conditions": "is_going_to_about",
        },
        {
            "trigger": "advance",
            "source": "list",
            "dest": "cancel",
            "conditions": "is_going_to_cancel",
        },
        {
            "trigger": "advance",
            "source": "new",
            "dest": "options",
            "conditions": "is_going_to_options",
        },
        {
            "trigger": "advance",
            "source": "new",
            "dest": "cancel",
            "conditions": "is_going_to_cancel",
        },
        {
            "trigger": "advance",
            "source": "list",
            "dest": "cartoon",
            "conditions": "is_going_to_cartoon",
        },
        {
            "trigger": "advance",
            "source": "cartoon",
            "dest": "list",
            "conditions": "is_going_to_list",
        },
        {
            "trigger": "advance",
            "source": "cartoon",
            "dest": "cancel",
            "conditions": "is_going_to_cancel",
        },
        {
            "trigger": "advance",
            "source": "genre",
            "dest": "cancel",
            "conditions": "is_going_to_cancel",
        },
        {
            "trigger": "advance",
            "source": "genre",
            "dest": "showgenre",
            "conditions": "is_going_to_showgenre",
        },
        {
            "trigger": "advance",
            "source": "showgenre",
            "dest": "cancel",
            "conditions": "is_going_to_cancel",
        },
        {
            "trigger": "advance",
            "source": "showgenre",
            "dest": "genre",
            "conditions": "is_going_to_genre",
        },
        {"trigger": "go_back", "source": ["cartoon"], "dest": "list"},
        {"trigger": "go_back", "source": ["showgenre"], "dest": "genre"},
        {"trigger": "go_back", "source": ["cancel", "about"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "Not Entering any State")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
