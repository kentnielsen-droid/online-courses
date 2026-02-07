import requests

url = "http://localhost:11434/api/chat"

data = {
    "model": "llama3.2",
    "stream": False,
    "messages": [
        {
            "role": "system",
            "content": "You're a quirky, friendly assistant with an easy going personality.",
        },
        {"role": "user", "content": "Please write 500 words about Barcelona."},
    ],
}

response = requests.post(url, json=data)
response.raise_for_status()

print(response.json()["message"]["content"])
