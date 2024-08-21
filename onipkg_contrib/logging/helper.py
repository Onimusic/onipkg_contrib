from logging.handlers import RotatingFileHandler
import urllib.parse
import requests

def notify_on_discord(text):
    from discord import SyncWebhook
    webhook = SyncWebhook.from_url(
        'https://discordapp.com/api/webhooks/1101219902762778705/uFSi_pecwuJIbiKnS48ft-qmbZNHdjl3SLwPR7AqSQJojUetw6Nm8sygOTZOCR267Yxn')
    webhook.send(text)

class RotatingAndTelegramHandler(RotatingFileHandler):
    """
        A handler that sends a telegram message after logging localy.

        Example args to use:
        {
            'level': 'DEBUG' if DEBUG else 'ERROR',
            'class': 'onipkg_contrib.logging.helper.RotatingAndTelegramHandler',
            'formatter': 'simple',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'oni_services_token': [ONISERVICES_TOKEN],
            'telegram_onitificator_bot_token': [TELEGRAM_BOT_TOKEN],
            'chat_ids': {'dev': [TELEGRAM_ONIDEV_NOTIFICATIONS_CHAT_ID]},
            'project_name': 'Project Name',
            'client': client
        }
    """
    def __init__(self, oni_services_token, telegram_onitificator_bot_token, chat_ids, project_name, *args, **kwargs):
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
        super().emit(record)
        data = {
            'oni_token': self.oni_services_token,
            'bot_token': self.telegram_onitificator_bot_token,
            'chat_id': self.chat_ids.get('dev'),
            'text': urllib.parse.quote(f'Um erro foi logado no {self.project_name}. \nErro: {record.getMessage()}')
        }
        requests.post('https://onisass.onimusic.com.br/onitifications/notify-on-telegram', data=data)
        try:
            response = notify_on_discord(f'Um erro foi logado no {self.project_name}. \nErro: {record.getMessage()}')
        except Exception as e:
            print(f'Error sending notification: {e}')
            pass

