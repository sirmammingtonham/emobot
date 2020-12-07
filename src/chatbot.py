import json
import os

from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

class ChatBot:
    def __init__(self):
        assistant_authenticator = IAMAuthenticator(
            os.environ.get('ASSISTANT_APIKEY'))
        self.assistant = AssistantV2(
            version='2018-09-20',
            authenticator=assistant_authenticator)
        self.assistant.set_service_url(os.environ.get('ASSISTANT_URL'))
        self.assistant_id = os.environ.get('ASSISTANT_ID')
        self.session_id = self.assistant.create_session(
            assistant_id=self.assistant_id).get_result()['session_id']
    
    def __del__(self):
        self.assistant.delete_session(
            assistant_id=self.assistant_id, session_id=self.session_id)

    def processMessage(self, text, tone, emotion=None):
        input = {'text': text}

        context = {
            'global': {
                'tone': {
                    'type': tone.getTone(),
                    'score': tone.getScore()
                },
                'emotion': {
                    'type': 'test', # whatever we detect from emotion detection
                    'score': 0, # confidence score
                }
            }
        }

        response = self.assistant.message(assistant_id=self.assistant_id,
                                          session_id=self.session_id,
                                          input=input,
                                          context=context).get_result()

        print(json.dumps(response, indent=2))
        
        if response['output']['generic']:
            return response['output']['generic'][0]['text']
        else:
            return 'Watson couldn\'t understand'