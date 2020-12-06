import json
import os
from dotenv import load_dotenv, find_dotenv
import uuid

from ibm_watson import AssistantV2
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

import tone_detection

# load the .env file containing your environment variables for the required
# services (conversation and tone)
load_dotenv(find_dotenv('ibm-credentials.env'))


assistant_authenticator = IAMAuthenticator(os.environ.get('ASSISTANT_APIKEY'))
assistant = AssistantV2(
    version='2018-09-20',
    authenticator=assistant_authenticator)
assistant.set_service_url(os.environ.get('ASSISTANT_URL'))
assistant_id = os.environ.get('ASSISTANT_ID')


tone_analyzer_authenticator = IAMAuthenticator(
    os.environ.get('TONE_ANALYZER_APIKEY'))
tone_analyzer = ToneAnalyzerV3(
    version='2016-05-19',
    authenticator=tone_analyzer_authenticator)
tone_analyzer.set_service_url(os.environ.get('TONE_ANALYZER_URL'))

# This example stores tone for each user utterance in conversation context.
# Change this to false, if you do not want to maintain history
global_maintainToneHistoryInContext = True

# Payload for the Watson Conversation Service
# user input text required - replace "I am happy" with user input text.
global_payload = {
    'input': {
        'text': "I am happy"
    }
}


def invokeToneConversation(payload, maintainToneHistoryInContext):
    """
     invokeToneConversation calls the Tone Analyzer service to get the
     tone information for the user's input text (input['text'] in the payload
     json object), adds/updates the user's tone in the payload's context,
     and sends the payload to the
     conversation service to get a response which is printed to screen.
     :param payload: a json object containing the basic information needed to
     converse with the Conversation Service's message endpoint.
     :param maintainHistoryInContext:
     Note: as indicated below, the console.log statements can be replaced
     with application-specific code to process the err or data object
     returned by the Conversation Service.
    """
    session_id = assistant.create_session(assistant_id=assistant_id).get_result()['session_id']

    tone = tone_analyzer.tone(
        tone_input=payload['input'], content_type='application/json').get_result()
    conversation_payload = tone_detection.\
        updateUserTone(payload, tone, maintainToneHistoryInContext)
    
    response = assistant.message(assistant_id=assistant_id, 
                                 session_id=session_id,
                                 input=conversation_payload['input'],
                                 context=conversation_payload['context']).get_result()

    assistant.delete_session(assistant_id=assistant_id, session_id=session_id)
        
    print(json.dumps(response, indent=2))


if __name__ == "__main__":
    # synchronous call to conversation with tone included in the context
    invokeToneConversation(global_payload, global_maintainToneHistoryInContext)
