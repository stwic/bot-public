import config
from slack_sdk.webhook import WebhookClient

def trigger_slack_bot(text):
    webhook = WebhookClient(config.slack_webhook_url)
    response = webhook.send(text=text)
    assert response.status_code == 200
    assert response.body == "ok"