Glad you liked the setup! Here's a polished and super-readable version of your `README.md` section with clean formatting, ideal for both new users and experienced devs:

---

# 🔔 Push Dispatcher

**Push Dispatcher** is a simple and reusable service for sending push notifications using **Firebase Cloud Messaging (FCM)** in Django projects.

Send targeted messages to device tokens or broadcast to topics — with built-in support for Android and iOS.

---

## 🚀 Features

- 🔹 Send push notifications to **device tokens**
- 🔹 Broadcast messages to **topics**
- 🔹 **Subscribe/unsubscribe** devices from topics
- 🔹 Supports **APNs** (iOS) and message priority
- 🔹 Uses **Firebase service account** for secure messaging

---

## ⚙️ Quick Setup

### 1. Install Dependencies

```bash
pip install firebase-admin requests
```

---

### 2. Firebase Setup

- Go to the [Firebase Console](https://console.firebase.google.com)
- Create a project (if you haven’t already)
- Navigate to **Project Settings > Service Accounts**
- Click **"Generate new private key"**
- Save the downloaded `.json` file to your Django project

---

### 3. Add to `settings.py`

```python
# settings.py

INSTALLED_APPS = [
    ...
    "push_dispatcher",
]

FCM_PROJECT_ID = "your-firebase-project-id"
FIREBASE_SERVICE_ACCOUNT_KEY_PATH = "path/to/serviceAccountKey.json"
```

---

### 4. Send Notifications

```python
from push_dispatcher.notifications import PushNotificationDispatcher

dispatcher = PushNotificationDispatcher()

# Send to device tokens
dispatcher.send_to_tokens(
    tokens=["device_token_1", "device_token_2"],
    title="Hello",
    body="This is a test notification",
    custom_key="value"  # Optional additional data
)

# Send to a topic
dispatcher.send_to_topic(
    topic="news-updates",
    title="Breaking News",
    body="Check out the latest story!"
)
```

---

Let me know if you want to add **error handling**, **response examples**, or **Django integration tips** too!
