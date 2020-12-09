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

    def processMessage(self, text, tone, emotion, session):
        if 'session_id' not in session:
            session['session_id'] = self.assistant.create_session(
                assistant_id=self.assistant_id).get_result()['session_id']

        session_id = session['session_id']

        input = {
            'message_type': 'text',
            'text': text,
            'options': {
                'return_context': True
            }
        }

        context = {
            'skills': {
                'main skill': {
                    'user_defined': {
                        'tone': {
                            'type': tone.getTone(),
                            'score': tone.getScore()
                        },
                        'emotion': {
                            # whatever we detect from emotion detection
                            'type': emotion[0],
                            'score': emotion[1],  # confidence score
                        }
                    }
                }
            }
        }

        response = self.assistant.message(assistant_id=self.assistant_id,
                                                    session_id=session_id,
                                                    input=input,
                                                    context=context).get_result()

        # print(json.dumps(response, indent=2))

        if response['output']['generic']:
            return response['output']['generic'][0]['text']
        else:
            return 'Watson couldn\'t understand'
