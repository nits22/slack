import slack
import os
from pathlib import Path
from dotenv import load_dotenv
import certifi

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
token=os.environ['SLACK_TOKEN']
client = slack.WebClient(token=token)
print(token)
print(certifi.where())

client.chat_postMessage(channel='#test', text="Hello world")