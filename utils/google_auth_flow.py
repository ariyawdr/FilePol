import os
import pickle
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from ..config.settings import settings
from .logger import logger

SCOPES = ["https://www.googleapis.com/auth/drive.file"]

class GoogleAuthFlow:
    def __init__(self):
        self.client_config = {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "project_id": "پل-bot", # This can be a placeholder
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
            }
        }

    def get_authorization_url(self, state: str) -> tuple[str, Flow]:
        flow = Flow.from_client_config(
            self.client_config,
            scopes=SCOPES,
            state=state
        )
        flow.redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
        authorization_url, state = flow.authorization_url(access_type="offline", include_granted_scopes="true")
        return authorization_url, flow

    def exchange_code_for_token(self, code: str, flow: Flow) -> str:
        try:
            flow.fetch_token(code=code)
            credentials = flow.credentials
            return credentials.refresh_token
        except Exception as e:
            logger.error(f"Error exchanging code for token: {e}", exc_info=True)
            raise

    def get_credentials(self, refresh_token: str) -> Credentials:
        creds = Credentials(
            token=None,  # Access token will be refreshed
            refresh_token=refresh_token,
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            token_uri="https://oauth2.googleapis.com/token",
            scopes=SCOPES
        )
        if not creds.valid:
            if creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    logger.error(f"Error refreshing access token: {e}", exc_info=True)
                    raise
            else:
                raise Exception("Invalid or expired credentials without refresh token.")
        return creds

google_auth_flow = GoogleAuthFlow()

