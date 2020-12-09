import os
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, jsonify, request, session
import base64

from src.tone_analyzer import ToneAnalyzer
from src.emotion_detection import EmotionDetector
from src.chatbot import ChatBot

app = Flask('Emotionally Intelligent Chatbot')
app.secret_key = os.urandom(24)
app.config['TEMPLATES_AUTO_RELOAD'] = True

load_dotenv(find_dotenv('ibm-credentials.env'))
tone_analyzer = ToneAnalyzer()
emotion_detector = EmotionDetector()
chatbot = ChatBot()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/parse_text")
def test():
    userText = request.args.get('msg')

    if 'emotion' not in session:
        session['emotion'] = 'Neutral'
    current_emotion = session['emotion']

    tone = tone_analyzer.analyze(userText)
    response = chatbot.processMessage(userText, tone, current_emotion, session)

    return jsonify(response=response, tone=tone.getTone(), emotion=current_emotion[0])


@app.route("/parse_image", methods=['POST'])
def parse_image():
    try:
        imgdata = base64.b64decode(request.data.split(b',')[1])
        current_emotion = emotion_detector.run_detection_bytes(imgdata)
        session['emotion'] = current_emotion
        return f'successfully updated emotion to {current_emotion[0]}'

    except Exception as e:
        print(e)
        return f'error! {e}'


if __name__ == "__main__":
    app.run()
