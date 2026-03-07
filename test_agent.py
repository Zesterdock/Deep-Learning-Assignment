import requests
import os

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "YOUR_GROQ_API_KEY_HERE")  # Replace with your key or set GROQ_API_KEY env variable

try:
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "user", "content": "Say 'Groq AI is working!' if you can read this."}
            ],
            "max_tokens": 50
        },
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        print("✅ SUCCESS! Groq API is working!")
        print(f"Response: {result['choices'][0]['message']['content']}")
    else:
        print(f"❌ Error: HTTP {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Connection error: {e}")
