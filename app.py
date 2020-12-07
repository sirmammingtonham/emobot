from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import ToneAnalyzerV3
from dotenv import load_dotenv, find_dotenv
import os
from flask import Flask, render_template, request
import base64
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


load_dotenv(find_dotenv('ibm-credentials.env'))

tone_analyzer_authenticator = IAMAuthenticator(
    os.environ.get('TONE_ANALYZER_APIKEY'))
tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    authenticator=tone_analyzer_authenticator)
tone_analyzer.set_service_url(os.environ.get('TONE_ANALYZER_URL'))


@app.route("/parse_text")
def get_bot_response():
    userText = request.args.get('msg')
    tone_response = tone_analyzer.tone(
        tone_input={'text': userText}, content_type='application/json').get_result()
    print(tone_response)
    if tone_response['document_tone']['tones']:
        tone = tone_response['document_tone']['tones'][0]['tone_name']
    else:
        tone = 'Neutral'
    return f"Detected tone: {tone}"


@app.route("/")
def home():
    return render_template("index.html")

# @app.route("/parse_text")
# def get_bot_response():
#     userText = request.args.get('msg')
#     return f"You typed: {userText}"


@app.route("/parse_image", methods=['GET'])
def parse_image():
    myfile = request.args.get('image').split(',')
    imgdata = base64.b64decode(myfile[1])
    with open('test.jpg', 'wb') as f:
        f.write(imgdata)
    return ''


if __name__ == "__main__":
    app.run(debug=True)
