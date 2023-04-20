import logging

from flask import Flask
from slack_helper import bot


app = Flask(__name__)
app.register_blueprint(bot.slack_events)

# logging.basicConfig(level=logging.INFO, format='Method Name --> %(funcName)s  %(asctime)s   %(message)s\n')
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    #print(app.url_map)
    app.run(host='0.0.0.0', port=5002, debug=True)
