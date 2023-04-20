import os
import slack


client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']
welcome_messages = {}

class WelcomeMessage:

    START_TEXT = {
        'type': 'section',
        'text': {
            'type': 'mrkdwn',
            'text': (
                'Welcome to this awesome channel! \n\n'
                '*Get started by completing the tasks!*'
            )
        }
    }

    DIVIDER = {'type': 'divider'}

    def __init__(self, channel):
        self.channel = channel
        self.icon_emoji = ':robot_face:'
        self.timestamp = ''
        self.completed = False

    def get_message(self):
        return {
            'ts': self.timestamp,
            'channel': self.channel,
            # 'username': 'Welcome Robot!',
            # 'icon_emoji': self.icon_emoji,
            'blocks': [
                self.START_TEXT,
                self.DIVIDER,
                self._get_reaction_task()
            ]
        }

    def _get_reaction_task(self):
        checkmark = ':white_check_mark:'
        if not self.completed:
            checkmark = ':white_large_square:'

        text = f'{checkmark} *React to this message!*'
        return {'type': 'section', 'text': {'type': 'mrkdwn', 'text': text}}


    def send_welcome_message(channel, user):
        if channel not in welcome_messages:
            welcome_messages[channel] = {}
        if user in welcome_messages[channel]:
            return

        welcome = WelcomeMessage(channel)
        message = welcome.get_message()
        response = client.chat_postMessage(**message)
        welcome.timestamp = response['ts']
        welcome_messages[channel][user] = welcome

    def listen_reaction(channel,user):
        if f'@{user}' not in welcome_messages:
            return
        welcome = welcome_messages[f'@{user}'][user]
        welcome.completed = True
        welcome.channel = channel
        message = welcome.get_message()
        updated_message = client.chat_update(**message)
        welcome.timestamp = updated_message['ts']