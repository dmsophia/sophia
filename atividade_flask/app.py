from flask import Flask, jsonify, request
from marshmallow import Schema, fields, ValidationError
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import os
import datetime

app = Flask(__name__)

SECRET_KEY = os.environ.get('SECRET_KEY', 'afonsinho')

class MessageSchema(Schema):
    text = fields.Str(required=True, validate=lambda s: s.strip() != '')

message_schema = MessageSchema()

class JWTAuthenticator:
    @staticmethod
    def verify_token(token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return payload
        except ExpiredSignatureError:
            raise ValueError("Token expired")
        except InvalidTokenError:
            raise ValueError("Invalid token")

class MessageHandler:
    def create(self, data):
        if data is None:
            return {"message": "Validation error", "errors": "No data provided"}, 400
        try:
            result = message_schema.load(data)
            return {"message": "Message received", "data": result}, 201
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, 400

@app.route('/messages', methods=['POST'])
def create_message():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Token is missing!"}), 401

    try:
        token = token.split(" ")[1] if 'Bearer ' in token else token
        JWTAuthenticator.verify_token(token)
        message_handler = MessageHandler()
        response, status = message_handler.create(request.json)
        return jsonify(response), status
    except ValueError as e:
        return jsonify({"message": str(e)}), 401

if __name__ == '__main__':
    app.run(debug=True)
