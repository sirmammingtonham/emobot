from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, request
import base64
import logging

from src.tone_analyzer import ToneAnalyzer
from src.face_recognition import FacialRecognition
from src.chatbot import ChatBot

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask('Emotionally Intelligent Chatbot')
app.config['TEMPLATES_AUTO_RELOAD'] = True

load_dotenv(find_dotenv('ibm-credentials.env'))
tone_analyzer = ToneAnalyzer() 
face_recognition = FacialRecognition()
chatbot = ChatBot()

@app.route("/")
def home():
    return render_template("index.html")


# @app.route("/parse_text")
# def get_bot_response():
#     userText = request.args.get('msg')
#     tone = tone_analyzer.analyze(userText)
#     return f"Detected tone: {tone.getTone()}"

@app.route("/parse_text")
def test():
    userText = request.args.get('msg')
    tone = tone_analyzer.analyze(userText)
    response = chatbot.processMessage(userText, tone)

    return f"Detected tone: {tone.getTone()}&nbsp; <br> &nbsp; Watson says: {response}"


@app.route("/parse_image", methods=['GET'])
def parse_image():
    myfile = request.args.get('image').split(',')
    imgdata = base64.b64decode(myfile[1])
    face = face_recognition.run_detection_bytes(imgdata)

    # with open('test.jpg', 'wb') as f:
    #     f.write(imgdata)
    return 'face detected!' if face is not None else 'no face detected'


if __name__ == "__main__":
    app.run(debug=True)
