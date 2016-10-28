import os

from flask import current_app, abort, request


def requires_authentication():
    if current_app.config['AUTH_REQUIRED']:
        incoming_token = get_token_from_headers(request.headers)
        if not incoming_token:
            abort(401, "Unauthorized; bearer token must be provided")
        if not token_is_valid(incoming_token):
            abort(403, "Forbidden; invalid bearer token provided {}".format(incoming_token))

def token_is_valid(incoming_token):
    return incoming_token == current_app.config['AUTH_TOKEN']

def get_token_from_headers(headers):
    auth_header = headers.get('Authorization', '')
    if auth_header[:7] != 'Bearer ':
        return None
    return auth_header[7:]
