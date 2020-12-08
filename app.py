from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, jsonify, request
import base64
import logging

from src.tone_analyzer import ToneAnalyzer
from src.emotion_detection import EmotionDetector
from src.chatbot import ChatBot

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask('Emotionally Intelligent Chatbot')
app.config['TEMPLATES_AUTO_RELOAD'] = True

load_dotenv(find_dotenv('ibm-credentials.env'))
tone_analyzer = ToneAnalyzer() 
emotion_detector = EmotionDetector()
chatbot = ChatBot()

# since we only detect emotion every 3 seconds we need to track it
# current_emotion = ('Neutral', 0.0)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/parse_text")
def test():
    userText = request.args.get('msg')
    current_emotion = request.args.get('current_emotion')
    tone = tone_analyzer.analyze(userText)
    response = chatbot.processMessage(userText, tone, (current_emotion, 1.0))

    return jsonify(response=response, tone=tone.getTone(), emotion=current_emotion)

    # return f"Detected tone: {tone.getTone()}&nbsp; <br> &nbsp; Watson says: {response}"


@app.route("/parse_image", methods=['GET'])
def parse_image():
    try:
        myfile = request.args.get('image').split(',')
        imgdata = base64.b64decode(myfile[1])
        current_emotion = emotion_detector.run_detection_bytes(imgdata)
        return current_emotion[0]

    except Exception as e:
        print(e)
        return 'Neutral'
    


if __name__ == "__main__":
    app.run(debug=True)
