import json

TOKEN = '123'

class LambdaAPIHandler:
    def __init__(self, event):
        self.event = event

    def parse_body(self):
        try:
            return json.loads(self.event.get('body', '{}')), None
        except json.JSONDecodeError:
            return None, {'message': 'Formato JSON inválido'}

    def check_auth(self, token):
        return token == TOKEN

    def get_response(self, status_code, body):
        return {
            'statusCode': status_code,
            'body': json.dumps(body),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

    def process_event(self):
        auth_header = self.event.get('headers', {}).get('Authorization')
        
        if auth_header:
            token = auth_header.split(' ')[-1]
        else:
            token = ''

        if not self.check_auth(token):
            return self.get_response(403, {'message': 'Não autorizado'})

        body, error = self.parse_body()
        if error:
            return self.get_response(400, error)

        # Para o exercício, apenas imprime o corpo da requisição
        print(body)
        return self.get_response(200, body)

def lambda_handler(event, context):
    handler = LambdaAPIHandler(event)
    return handler.process_event()
