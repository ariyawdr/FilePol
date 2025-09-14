import requests
from ..config.settings import settings
from ..utils.logger import logger

class ShortioService:
    def __init__(self):
        self.api_key = settings.SHORTIO_API_KEY
        self.base_url = "https://api.short.io/links"

    def shorten_link(self, original_url: str, domain: str) -> str | None:
        if not self.api_key:
            logger.error("Short.io API key is not set.")
            return None

        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "originalURL": original_url,
            "domain": domain
        }

        try:
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            short_url = data.get("shortURL")
            if short_url:
                logger.info(f"Successfully shortened {original_url} to {short_url}")
                return short_url
            else:
                logger.error(f"Short.io API did not return a shortURL for {original_url}. Response: {data}")
                return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Error shortening link {original_url} with Short.io: {e}", exc_info=True)
            return None

shortio_service = ShortioService()

