from google.cloud import logging
from google.cloud.logging_v2.handlers.handlers import CloudLoggingHandler, _format_and_parse_message, \
    _GAE_RESOURCE_TYPE, _GAE_TRACE_ID_LABEL
import urllib.parse
import requests


class OniCloudHandler(CloudLoggingHandler):
    def __init__(self,oni_services_token,telegram_onitificator_bot_token,chat_ids,project_name, *args, **kwargs):
        self.oni_services_token = oni_services_token
        self.telegram_onitificator_bot_token = telegram_onitificator_bot_token
        self.chat_ids = chat_ids
        self.project_name = project_name
        super().__init__(*args, **kwargs)

    def emit(self, record):
        """Actually log the specified logging record.

        Overrides the default emit behavior of ``StreamHandler``.

        See https://docs.python.org/2/library/logging.html#handler-objects

        Args:
            record (logging.LogRecord): The record to be logged.
        """
        import urllib
        # super().emit(record)
        data = {
            'oni_token': self.oni_services_token,
            'bot_token': self.telegram_onitificator_bot_token,
            'chat_id': self.chat_ids.get('dev'),
            'text': urllib.parse.quote(f'Um erro foi logado no {self.project_name}. \nErro: {record.msg}')
        }
        response = requests.post('https://onisass.onimusic.com.br/onitifications/notify-on-telegram', data=data)
