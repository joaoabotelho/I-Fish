from random import randint
import os.path
import json
import sys

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

class googleApiRequest:

    def __init__(self, client_access_token):
        self.client_access_token = client_access_token
        self.ai = apiai.ApiAI(self.client_access_token)
        self.session_id = randint(1, MAX_INT)

    def expectResponse(self, query):
        request = self.ai.text_request()
        request.query = query
        request.session_id = self.session_id
        response = request.getresponse()
        parsed = json.loads(response.read().decode())
        print(json.dumps(parsed, indent=4))
        text_response = parsed['result']['fulfillment']['speech']
        score = parsed['result']['score']
        if score == 0.0:
            text_response = 'I didn\'t understand'
        print('Response: ', text_response)
        return text_response
