import json

### simple class for housing the tone response 
# (so we don't have to decode a json each time)
# we can add more functionality to this later depending
# on what we end up using the tones for

class Tone:
    def __init__(self, text, response):
        self.text = text
        self.response = response

        self.document_tones = [
            tone for tone in response['document_tone']['tones']]
        
        if 'sentences_tone' in response:
            self.sentence_tones = {data['text']: data['tones']
                                for data in response['sentences_tone']}
        else:
            self.sentence_tones = None

    def __str__(self):
        return json.dumps(self.response, indent=2)
    
    def getAverageToneScore(self):
        return sum([tone['score'] for tone in self.document_tones]) / len(self.document_tones)
    

