import json
import requests
from django.conf import settings
from .firebase_utils import get_firebase_access_token

class PushNotification:
    FCM_URL = "https://fcm.googleapis.com/v1/projects/{project_id}/messages:send"

    def __init__(self, *users):
        self.fcm_devices = GCMDevice.objects.filter(user__in=users).distinct() or None
        self.apn_devices = APNSDevice.objects.filter(user__in=users).distinct()

    def fcm_send_message(self, queryset, title, body, banner_url=None, **kwargs):
        """
        Send a push notification to a list of devices via FCM.
        """
        responses = []
        access_token = get_firebase_access_token()  # Retrieve Firebase access token

        if not access_token:
            print("Error retrieving access token. Cannot send FCM message.")
            return responses

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }

        project_id = settings.FCM_PROJECT_ID

        if isinstance(queryset, list):
            registration_ids = queryset
        else:
            registration_ids = list(
                queryset.filter(
                    active=True, cloud_message_type="FCM"
                ).values_list("registration_id", flat=True)
            )

        if registration_ids:
            try:
                for token in registration_ids:
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
                            "apns": {
                                "payload": {
                                    "aps": {
                                        "alert": {
                                            "title": title,
                                            "body": body,
                                        },
                                        "sound": "default",
                                        "badge": kwargs.get("badge", 1),
                                        "content-available": 1,
                                    }
                                },
                                "headers": {
                                    "apns-priority": "10",
                                    "apns-push-type": "alert",
                                }
                            }
                        }
                    }

                    url = self.FCM_URL.format(project_id=project_id)
                    try:
                        response = requests.post(url, headers=headers, data=json.dumps(message))

                        if response.status_code == 200:
                            print(f"Successfully sent message to registration ID {token}")
                        else:
                            print(f"Error sending message: {response.content}")
                        responses.append(response.json())
                    except Exception as e:
                        print(f"Error sending message: {e}")
                        raise e

            except Exception as e:
                print(f"Error in processing registration IDs: {e}")

        return responses

    def fcm_send_to_topic(self, topic, title, body, banner_url=None, **kwargs):
        """
        Send a push notification to a specific topic using FCM.
        """
        responses = []
        access_token = get_firebase_access_token()  # Retrieve Firebase access token

        if not access_token:
            print("Error retrieving access token. Cannot send FCM message.")
            return responses

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }

        project_id = settings.FCM_PROJECT_ID

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
                "apns": {
                    "payload": {
                        "aps": {
                            "alert": {
                                "title": title,
                                "body": body,
                            },
                            "sound": "default",
                            "badge": kwargs.get("badge", 1),
                            "content-available": 1,
                        }
                    },
                    "headers": {
                        "apns-priority": "10",
                        "apns-push-type": "alert",
                    }
                }
            }
        }

        url = self.FCM_URL.format(project_id=project_id)
        try:
            response = requests.post(url, headers=headers, data=json.dumps(message))

            if response.status_code == 200:
                print(f"Successfully sent message to topic {topic}")
            else:
                print(f"Error sending message to topic {topic}: {response.content}")
            responses.append(response.json())
        except Exception as e:
            print(f"Error sending message: {e}")
            raise e

        return responses
