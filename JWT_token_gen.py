import json
import jwt
import datetime
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, json
from flask import render_template
from cryptography.hazmat.primitives import serialization as crypto_serialization
import base64
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index2.html')


@app.route('/generate_token', methods=['POST'])
def generate_token():

    data = request.form

    required_fields = ['carrier_code', 'iss', 'sub', 'exp', 'iat', 'private_key', 'algorithm']

    missing_fields = [field for field in required_fields if not data.get(field)]

    if missing_fields:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400
        # return json.dumps({'error': f'Missing fields: {", ".join(missing_fields)}'}), 405
    else:
        carrier_code = request.form['carrier_code']
        algorithm = request.form['algorithm']
        iss = request.form['iss']
        sub = request.form['sub']
        exp = request.form['exp']
        iat = request.form['iat']
        private_key = request.form['private_key']
    # if carrier_code and iss and sub and exp and iat and private_key and algorithm:
    # if missing_fields:
        payload = {
            "sub": sub,
            "iss": iss,
            "exp": exp,
            "iat": iat
        }
        coded_string = private_key
        private_key = base64.b64decode(coded_string)
        if algorithm == 'RS256':
            encoded = jwt.encode(payload, private_key, algorithm=algorithm)
            token = "JWT " + encoded
            print(token)
            # return json.dumps({'validated': token}), 201
            return jsonify({'validated': token}), 201
        else:
            return jsonify({'error': f'The specified algorithm is an asymmetric key or x509 certificate and should not be used as an HMAC secret.'}), 405
    # return json.dumps({'Validation : missing paramaters': True}), 403
    # return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400


def validate(iss, sub):
    return True


if __name__ == "__main__":
    app.run(debug=True)



