import logging
import string

import slack
import os
from dotenv import load_dotenv
from pathlib import Path

from flask import Blueprint, Response, request
from slackeventsapi import SlackEventAdapter
from slack_helper.Welcome_message_blueprint_py import WelcomeMessage

message_counts = {}
BAD_WORDS = ['hmm', 'no', 'tim']

env_path = Path('.') / '__init__.py'
load_dotenv(dotenv_path=env_path)

slack_events = Blueprint('slack_events', __name__)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']

slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], '/slack/events', slack_events)
#client.chat_postMessage(channel='#test', text='Hello')

# @slack_event_adapter.on("message")
# def handle_message(event_data):
#     message = event_data["event"]
#     if message.get("subtype") is None and "hi" in message.get('text'):
#         logging.info(f"{message}")
#         channel = message["channel"]
#         message = "Hi <@%s>! :tada:" % message["user"]
#         client.chat_postMessage(channel=channel, text=message)
#


@slack_event_adapter.on('message')
def message(payload):
    logging.info(f"{payload}")
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    if user_id != None and BOT_ID != user_id:
        if user_id in message_counts:
            message_counts[user_id] += 1
        else:
            message_counts[user_id] = 1

        if text.lower() == 'start':
            WelcomeMessage.send_welcome_message(f'@{user_id}', user_id)

        if check_if_bad_words(text):
            ts = event.get('ts')
            client.chat_postMessage(
            channel=channel_id, thread_ts=ts, text="THAT IS A BAD WORD!")
        else:
            channel = event["channel"]
            message = "Hello <@%s>!" % event["user"]
            client.chat_postMessage(channel=channel, text=message)


@slack_events.route('/message-count', methods=['POST'])
def message_count():
    data = request.form
    channel_id = data.get('channel_id')
    user_id = data.get('user_id')
    message_count = message_counts.get(user_id, 0)
    client.chat_postMessage(channel=channel_id, text=f"Count: {message_count}")
    return Response(), 200

@slack_event_adapter.on("reaction_added")
def reaction(payload):
    event = payload.get('event', {})
    channel_id = event.get('item', {}).get('channel')
    user_id = event.get('user')
    WelcomeMessage.listen_reaction(channel_id, user_id)
    return Response, 200

@slack_event_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))



def check_if_bad_words(message):
    msg = message.lower()
    msg = msg.translate(str.maketrans('', '', string.punctuation))
    return any(word in msg for word in BAD_WORDS)