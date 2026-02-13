import requests
import json

class ScaleDownClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.scaledown.xyz/compress/raw/"

    def compress_paper(self, text):

        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "context": "Compress this scientific research paper while preserving technical details.",
            "prompt": text,
            "scaledown": {
                "rate": "auto"
            }
        }

        response = requests.post(
            self.base_url,
            headers=headers,
            data=json.dumps(payload),
            timeout=60
        )

        response.raise_for_status()

        result = response.json()

        if result.get("successful"):
            return result.get("compressed_prompt")

        return None
