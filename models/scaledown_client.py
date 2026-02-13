import requests
import json

class ScaleDownClient:
    def __init__(self, api_key):
        self.api_key = api_key.strip()
        self.base_url = "https://api.scaledown.xyz/compress/raw/"

    def compress_paper(self, text):
    
        headers = {
            "x-api-key": self.api_key.strip(),
            "Content-Type": "application/json"
        }
    
        payload = {
            "context": "You are a scientific summarization engine. Return only the compressed version of the input text.",
            "prompt": text,
            "scaledown": {
                "rate": "auto"
            }
        }
    
        response = requests.post(
            self.base_url,
            headers=headers,
            json=payload,   # better than data=json.dumps()
            timeout=60
        )
    
        response.raise_for_status()
    
        result = response.json()
    
        # Proper parsing based on actual API structure
        if result.get("successful"):
            results_block = result.get("results", {})
            if results_block.get("success"):
                compressed_text = results_block.get("compressed_prompt")

                if compressed_text and compressed_text.strip() != payload["context"]:
                    return compressed_text
    
        return None
