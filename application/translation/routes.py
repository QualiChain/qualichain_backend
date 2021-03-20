# =================================
#   Translation API
# =================================
import logging
import sys

from flask import request, jsonify
from flask_restful import Resource, Api
from application.database import db
from application.models import TranslationUsage
from application.translation import translation_blueprint
from datetime import date
from google.cloud import translate_v2 as translate
import os

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

api = Api(translation_blueprint)

TRANSLATED_CHARS_LIMIT = 15000

# environment variable for Google translation credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:\Users\vkarakolis.EPU\Downloads\qualichain-translation-26d081738c31.json"


class TranslationObject(Resource):
    def post(self):
        try:
            data = dict(request.get_json())
            text = data['text']
            length = len(text)

            today_characters = TranslationUsage.query.filter_by(day=date.today())
            today_use = today_characters.first()
            if today_use is None:
                usage = 0
            else:
                usage = today_use.usage

            if usage+length > TRANSLATED_CHARS_LIMIT:
                return 'Exceeded the translation rate limits, try again tomorrow', 429

            if today_use is not None:
                today_characters.update({"usage": today_use.usage + length})
                db.session.commit()
            else:
                translation_obj = TranslationUsage(day=date.today(), usage=length)
                db.session.add(translation_obj)
                db.session.commit()

            translate_client = translate.Client()
            target = 'en'

            output = translate_client.translate(text, target_language=target)
            print(output)
            return output

        except Exception as ex:
            log.error(ex)
            return ex, 400


# Translation Route
api.add_resource(TranslationObject, '/translate')

