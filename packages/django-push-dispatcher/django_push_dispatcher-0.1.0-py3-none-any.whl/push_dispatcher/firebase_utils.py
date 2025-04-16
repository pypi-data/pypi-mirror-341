import google.auth
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from django.conf import settings

SERVICE_ACCOUNT_FILE = settings.FIREBASE_KEY_PATH
SCOPES = ["https://www.googleapis.com/auth/firebase.messaging"]

def get_firebase_access_token(service_account_file=SERVICE_ACCOUNT_FILE, scopes=SCOPES):
    """
    Retrieve and refresh Firebase access token from a service account file.
    :param service_account_file: Path to the Firebase service account key JSON file
    :param scopes: The scopes required to access Firebase APIs
    :return: Access token
    """
    try:
        credentials = service_account.Credentials.from_service_account_file(
            service_account_file, scopes=scopes
        )
        credentials.refresh(Request())
        return credentials.token
    except Exception as e:
        print(f"Error retrieving access token: {e}")
        return None
