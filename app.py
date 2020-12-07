from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, request
import base64
import logging

from src.tone_analyzer import *

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


load_dotenv(find_dotenv('ibm-credentials.env'))
tone_analyzer = tone_analyzer.ToneAnalyzer()  # type: ignore


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/parse_text")
def get_bot_response():
    userText = request.args.get('msg')
    tone = tone_analyzer.analyze(userText)
    return f"Detected tone: {tone.getTone()}"


@app.route("/parse_image", methods=['GET'])
def parse_image():
    myfile = request.args.get('image').split(',')
    imgdata = base64.b64decode(myfile[1])
    with open('test.jpg', 'wb') as f:
        f.write(imgdata)
    return ''


if __name__ == "__main__":
    app.run(debug=True)
