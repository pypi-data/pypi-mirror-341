import json
import requests
from django.conf import settings
from firebase_admin import messaging
from .firebase_utils import get_firebase_access_token


class FirebasePushService:
    FCM_URL_TEMPLATE = "https://fcm.googleapis.com/v1/projects/{project_id}/messages:send"

    def __init__(self, access_token=None):
        self.access_token = access_token or get_firebase_access_token()
        self.project_id = settings.FCM_PROJECT_ID
        self.fcm_url = self.FCM_URL_TEMPLATE.format(project_id=self.project_id)

    def _build_headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def _apns_payload(self, title, body, badge=1):
        return {
            "payload": {
                "aps": {
                    "alert": {"title": title, "body": body},
                    "sound": "default",
                    "badge": badge,
                    "content-available": 1,
                }
            },
            "headers": {
                "apns-priority": "10",
                "apns-push-type": "alert",
            },
        }

    def _build_message(self, token_or_topic, is_topic=False, title="", body="", banner_url=None, **kwargs):
        target_key = "topic" if is_topic else "token"
        return {
            "message": {
                target_key: token_or_topic,
                "data": {
                    "title": title,
                    "body": body,
                    "banner_url": banner_url or "",
                    "priority": "high",
                    **{k: str(v) for k, v in kwargs.items()},
                },
                "apns": self._apns_payload(title, body, kwargs.get("badge", 1)),
            }
        }

    def send_to_tokens(self, tokens, title, body, banner_url=None, **kwargs):
        if not self.access_token:
            return []

        headers = self._build_headers()
        responses = []

        for token in tokens:
            message = self._build_message(token, title=title, body=body, banner_url=banner_url, **kwargs)
            try:
                response = requests.post(self.fcm_url, headers=headers, data=json.dumps(message))
                responses.append(response.json())
            except Exception as e:
                responses.append({"error": str(e)})

        return responses

    def send_to_topic(self, topic, title, body, banner_url=None, **kwargs):
        if not self.access_token:
            return []

        headers = self._build_headers()
        message = self._build_message(topic, is_topic=True, title=title, body=body, banner_url=banner_url, **kwargs)

        try:
            response = requests.post(self.fcm_url, headers=headers, data=json.dumps(message))
            return [response.json()]
        except Exception as e:
            return [{"error": str(e)}]

    def subscribe_to_topic(self, registration_ids, topic, old_registration_ids=None):
        if not isinstance(registration_ids, list):
            return {"error": "registration_ids must be a list"}

        result = {"subscribed": 0, "unsubscribed": 0, "errors": []}

        def batch_process(ids, action):
            while ids:
                batch = ids[:1000]
                ids[:] = ids[1000:]
                try:
                    response = action(batch, topic)
                    return response.success_count
                except Exception as e:
                    result["errors"].append(str(e))
                    return 0

        if old_registration_ids:
            result["unsubscribed"] += batch_process(old_registration_ids, messaging.unsubscribe_from_topic)

        result["subscribed"] += batch_process(registration_ids, messaging.subscribe_to_topic)

        return result
