def notify_on_discord(text):
    from discord import SyncWebhook
    webhook = SyncWebhook.from_url(
        'https://discordapp.com/api/webhooks/1101219902762778705/uFSi_pecwuJIbiKnS48ft-qmbZNHdjl3SLwPR7AqSQJojUetw6Nm8sygOTZOCR267Yxn')
    webhook.send(text)

notify_on_discord('teste')