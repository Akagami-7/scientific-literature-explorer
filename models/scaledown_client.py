def compress_paper(self, text):

    headers = {
        "x-api-key": self.api_key.strip(),
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
        json=payload,   # better than data=json.dumps()
        timeout=60
    )

    response.raise_for_status()

    result = response.json()

    # Proper parsing based on actual API structure
    if result.get("successful"):
        results_block = result.get("results", {})
        if results_block.get("success"):
            return results_block.get("compressed_prompt")

    return None
