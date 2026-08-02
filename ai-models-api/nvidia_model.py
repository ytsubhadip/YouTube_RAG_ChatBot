import json
import requests
import os
from dotenv import load_dotenv
load_dotenv()

invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
stream = False

headers = {
  # use single quotes inside getenv to avoid f-string quote issues
  "Authorization": f"Bearer nvapi-{os.getenv('model_api')}",
    "Accept": "text/event-stream" if stream else "application/json",
}

payload = {
  "messages": [
    {
      "role": "user",
      "content": "is nvidia api key is free to use iunlimitate"
    }
  ],
  "model": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning",
  "max_tokens": 65536,
  "reasoning_budget": 16384,
  "stream": stream,
  "temperature": 0.6,
  "top_p": 0.95
}

response = requests.post(invoke_url, headers=headers, json=payload, stream=stream)

res = response.json()
message = res["choices"][0]["message"]["content"]
print(message)