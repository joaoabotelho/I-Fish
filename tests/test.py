class googleApiRequest:

    def __init__(self, client_access_token):
        self.client_access_token = client_access_token
        self.ai = apiai.ApiAI(self.client_access_token)
        self.session_id = randint(1, MAX_INT)

    def expectResponse(self, query):
        query = input('Input: ')
        request = self.ai.text_request()
        request.query = query
        request.session_id = self.session_id
        response = request.getresponse()
        parsed = json.loads(response.read().decode())
        return text_response

if __name__ == '__main__':
    while True:
        audio = speechRec.record()
        speechRec.analyze(audio)
