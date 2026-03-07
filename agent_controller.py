import requests
from bag_counter import process_video
import logging
import os

# ========================================
# SETUP: Get your FREE Groq API key at:
# https://console.groq.com/keys
# ========================================
GROQ_API_KEY = os.environ.get('GROQ_API_KEY', 'YOUR_GROQ_API_KEY_HERE')  # Get from environment variable

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def run_agent(video_path):
    try:
        # Run the bag counter model
        generator = process_video(video_path)
        frame, bags_in, bags_out = next(generator)

        # If API key not set, return basic summary
        if GROQ_API_KEY == "YOUR_GROQ_API_KEY_HERE":
            return f"""📊 **Warehouse Summary**

Bags Loaded: {bags_in}
Bags Unloaded: {bags_out}

⚠️ To enable AI insights:
1. Visit: https://console.groq.com/keys
2. Sign up (free)
3. Create an API key
4. Paste it in agent_controller.py (line 9)"""

        # Prepare the prompt
        prompt = f"""Warehouse monitoring report.

Bags Loaded: {bags_in}
Bags Unloaded: {bags_out}

Provide a short operational summary for warehouse managers."""

        # Call Groq API
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "llama-3.3-70b-versatile",  # Fast and capable
            "messages": [
                {"role": "system", "content": "You are a warehouse management AI assistant. Provide concise, professional summaries."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 200
        }

        response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
    
    except requests.exceptions.RequestException as e:
        # Return error-safe fallback message
        logging.error(f"Agent API error: {e}")
        try:
            generator = process_video(video_path)
            frame, bags_in, bags_out = next(generator)
            return f"""📊 **Warehouse Summary**

Bags Loaded: {bags_in}
Bags Unloaded: {bags_out}

⚠️ AI agent connection failed. Check your API key and internet connection."""
        except:
            return "⚠️ Unable to process video. Please check the video path."
    
    except Exception as e:
        logging.error(f"Agent error: {e}")
        return f"⚠️ Error: {str(e)}"