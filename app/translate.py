import json
import requests
import uuid
from flask_babel import _
from flask import current_app


def translate(text, source_language, dest_language):
    if 'MS_TRANSLATOR_KEY' not in current_app.config or \
            not current_app.config['MS_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured.')
    auth = {
        'Ocp-Apim-Subscription-Key': current_app.config['MS_TRANSLATOR_KEY']
    }
    body = [{'text': text}]
    headers = {
        'Ocp-Apim-Subscription-Key': current_app.config['MS_TRANSLATOR_KEY'],
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    r = requests.post(
        f'https://api.cognitive.microsofttranslator.com/translate?api-version='
        f'3.0&from={source_language}&to={dest_language}',
        json=body,
        headers=headers)
    if r.status_code != 200:
        return _('Error: the translation service failed.')
    response = json.loads(r.content.decode('utf-8-sig'))
    return response[0]['translations'][0]['text']
