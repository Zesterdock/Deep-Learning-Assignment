import streamlit as st
import cv2
import numpy as np
import os
from bag_counter import process_video

st.set_page_config(layout="wide", page_title="Warehouse Management System")

# Custom CSS to match the reference dashboard design
st.markdown("""
<style>
    .main-header {
        background-color: #1e5a7d;
        color: #ffd700;
        padding: 20px;
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .sub-header {
        background-color: #1e5a7d;
        color: #ffd700;
        padding: 15px;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    .iot-section {
        background-color: #1e6b8f;
        color: white;
        padding: 25px;
        border-radius: 8px;
        margin-top: 20px;
    }
    .iot-header {
        color: #ffd700;
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 15px;
    }
    .gate-label {
        background-color: #1e5a7d;
        color: white;
        padding: 8px;
        text-align: center;
        font-weight: bold;
        border-radius: 4px;
        margin: 5px 0;
    }
    .bag-counter {
        background-color: #1e5a7d;
        color: white;
        padding: 10px;
        text-align: center;
        font-size: 14px;
        border-radius: 4px;
        margin: 2px;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<div class="main-header">Warehouse Management System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Bag Counting Management System</div>', unsafe_allow_html=True)

# AI Agent Status (at top)
agent_placeholder = st.empty()
agent_placeholder.info("🤖 AI Agent analyzing warehouse operations...")

# Create 3 camera panels
col1, col2, col3 = st.columns(3)

# Camera 1 placeholders
with col1:
    cam1 = st.empty()
    st.markdown('<div class="gate-label">Gate Number : 01</div>', unsafe_allow_html=True)
    bag_col1_1, bag_col1_2 = st.columns(2)
    with bag_col1_1:
        in1 = st.empty()
    with bag_col1_2:
        out1 = st.empty()

# Camera 2 placeholders
with col2:
    cam2 = st.empty()
    st.markdown('<div class="gate-label">Gate Number : 02</div>', unsafe_allow_html=True)
    bag_col2_1, bag_col2_2 = st.columns(2)
    with bag_col2_1:
        in2 = st.empty()
    with bag_col2_2:
        out2 = st.empty()

# Camera 3 placeholders
with col3:
    cam3 = st.empty()
    st.markdown('<div class="gate-label">Gate Number : 03</div>', unsafe_allow_html=True)
    bag_col3_1, bag_col3_2 = st.columns(2)
    with bag_col3_1:
        in3 = st.empty()
    with bag_col3_2:
        out3 = st.empty()

# Display video feed (Camera 1)
video_path = "input/Problem Statement Scenario1.mp4"
first_frame = True
agent_called = False

# Initialize placeholder cameras (Camera 2 & 3) once
placeholder_img = np.full((480, 640, 3), [30, 90, 125], dtype=np.uint8)
cv2.putText(placeholder_img, "Camera Offline", (180, 240), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

cam2.image(placeholder_img, channels="RGB", width="stretch")
in2.markdown('<div class="bag-counter">Bags In : 0</div>', unsafe_allow_html=True)
out2.markdown('<div class="bag-counter">Bags Out : 0</div>', unsafe_allow_html=True)

cam3.image(placeholder_img, channels="RGB", width="stretch")
in3.markdown('<div class="bag-counter">Bags In : 0</div>', unsafe_allow_html=True)
out3.markdown('<div class="bag-counter">Bags Out : 0</div>', unsafe_allow_html=True)

# IOT Parameters Section with styled background (before video loop so it's always visible)
st.markdown("""
<div class="iot-section">
    <div class="iot-header">IOT Parameters Monitoring</div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
        <div>
            <p><strong>Temperature :</strong> 27°C</p>
            <p><strong>Humidity :</strong> 64%</p>
            <p><strong>Phosphine Gas Level :</strong> Safe</p>
        </div>
        <div>
            <p><strong>Smoke and Fire Status:</strong> Normal</p>
            <p><strong>Gate Open/Close Status:</strong> Open</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

for frame, bags_in, bags_out in process_video(video_path):

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    cam1.image(frame, channels="RGB", width="stretch")

    in1.markdown(f'<div class="bag-counter">Bags In : {bags_in}</div>', unsafe_allow_html=True)
    out1.markdown(f'<div class="bag-counter">Bags Out : {bags_out}</div>', unsafe_allow_html=True)
    
    # Call AI agent after first detection
    if first_frame and (bags_in > 0 or bags_out > 0) and not agent_called:
        agent_called = True
        try:
            from agent_controller import run_agent
            agent_output = f"""📊 **Warehouse Summary**

Bags Loaded: {bags_in}
Bags Unloaded: {bags_out}

✅ Real-time monitoring active."""
            
            # Try to get AI insights
            try:
                import requests
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {os.environ.get('GROQ_API_KEY', '')}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama-3.3-70b-versatile",
                        "messages": [
                            {"role": "system", "content": "You are a warehouse AI assistant. Provide brief operational summaries."},
                            {"role": "user", "content": f"Warehouse report: {bags_in} bags loaded, {bags_out} bags unloaded. Give a 1-sentence summary."}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 100
                    },
                    timeout=5
                )
                if response.status_code == 200:
                    ai_summary = response.json()["choices"][0]["message"]["content"]
                    agent_output = f"""🤖 **AI Agent Analysis**

{ai_summary}

📊 **Current Status:**
- Bags Loaded: {bags_in}
- Bags Unloaded: {bags_out}"""
            except:
                pass  # Use fallback summary
            
            agent_placeholder.info(agent_output)
        except Exception as e:
            agent_placeholder.warning(f"⚠️ AI Agent offline  • Monitoring continues")
        
        first_frame = False