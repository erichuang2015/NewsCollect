# -*- coding: utf-8 -*-
from flask import jsonify


def bad_request(msg):
    response = jsonify({'error': 'bad request', 'message': msg})
    response.status_code = 400
    return response

def forbidden(msg):
    response = jsonify({'error': 'forbidden', 'message': v})
    response.status_code = 403
    return response


def not_found(msg):
    response = jsonify({'error': 'not found', 'message': msg})
    response.status_code = 404
    return response


def message(msg):
    response = jsonify({'message': msg})
    response.status_code = 200
    return response
