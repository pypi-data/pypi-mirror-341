import json
import requests
from django.conf import settings
from firebase_admin import messaging
from .firebase_utils import get_firebase_access_token


class PushNotificationDispatcher:
    FCM_URL = "https://fcm.googleapis.com/v1/projects/{project_id}/messages:send"

    def __init__(self, access_token=None):
        self.access_token = access_token or get_firebase_access_token()
        self.project_id = settings.FCM_PROJECT_ID

    def _build_headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def _build_apns_payload(self, title, body, badge=1):
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

    def send_to_tokens(self, tokens, title, body, banner_url=None, **kwargs):
        """
        Send push notification to a list of device tokens.
        """
        if not self.access_token:
            return []

        responses = []
        headers = self._build_headers()
        url = self.FCM_URL.format(project_id=self.project_id)

        for token in tokens:
            message = {
                "message": {
                    "token": token,
                    "data": {
                        "title": title,
                        "body": body,
                        "banner_url": banner_url or "",
                        "priority": "high",
                        **{k: str(v) for k, v in kwargs.items()},
                    },
                    "apns": self._build_apns_payload(title, body, kwargs.get("badge", 1)),
                }
            }

            try:
                response = requests.post(url, headers=headers, data=json.dumps(message))
                responses.append(response.json())
            except Exception as e:
                responses.append({"error": str(e)})

        return responses

    def send_to_topic(self, topic, title, body, banner_url=None, **kwargs):
        """
        Send push notification to a topic.
        """
        if not self.access_token:
            return []

        headers = self._build_headers()
        url = self.FCM_URL.format(project_id=self.project_id)

        message = {
            "message": {
                "topic": topic,
                "data": {
                    "title": title,
                    "body": body,
                    "banner_url": banner_url or "",
                    "priority": "high",
                    **{k: str(v) for k, v in kwargs.items()},
                },
                "apns": self._build_apns_payload(title, body, kwargs.get("badge", 1)),
            }
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(message))
            return [response.json()]
        except Exception as e:
            return [{"error": str(e)}]

    def subscribe_to_topic(self, registration_ids, topic, old_registration_ids=None):
        """
        Subscribe and optionally unsubscribe devices from a topic.
        """
        if not isinstance(registration_ids, list):
            return {"error": "registration_ids must be a list"}

        result = {"subscribed": 0, "unsubscribed": 0, "errors": []}

        # Unsubscribe old tokens
        if old_registration_ids:
            while old_registration_ids:
                batch = old_registration_ids[:1000]
                old_registration_ids = old_registration_ids[1000:]
                try:
                    response = messaging.unsubscribe_from_topic(batch, topic)
                    result["unsubscribed"] += response.success_count
                except Exception as e:
                    result["errors"].append(str(e))

        # Subscribe new tokens
        while registration_ids:
            batch = registration_ids[:1000]
            registration_ids = registration_ids[1000:]
            try:
                response = messaging.subscribe_to_topic(batch, topic)
                result["subscribed"] += response.success_count
            except Exception as e:
                result["errors"].append(str(e))

        return result
