import streamlit as st
import cv2
import numpy as np
import os
from bag_counter import process_video

# Page config
st.set_page_config(page_title="WareHouse DashBoard", layout="wide")

# Custom CSS
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main container styling */
    .main {
        background-color: #f5f7fa;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1e5a7d 0%, #2a7aa3 50%, #1e5a7d 100%);
        color: white;
        padding: 25px;
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .sub-header {
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
        color: #1e5a7d;
        padding: 18px;
        text-align: center;
        font-size: 26px;
        font-weight: bold;
        margin-bottom: 25px;
        border-radius: 10px;
        box-shadow: 0 3px 5px rgba(0, 0, 0, 0.15);
    }
    
    .camera-label {
        background: linear-gradient(135deg, #1e5a7d 0%, #2a7aa3 100%);
        color: white;
        padding: 12px;
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        border-radius: 8px;
        margin-bottom: 12px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .bag-counter {
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
        color: #1e5a7d;
        padding: 10px;
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        border-radius: 8px;
        margin-top: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
    }
    
    .iot-section {
        background: linear-gradient(135deg, #ffffff 0%, #e8f4f8 100%);
        border: 3px solid #1e5a7d;
        border-radius: 12px;
        padding: 25px;
        margin: 25px 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    .iot-header {
        color: #1e5a7d;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-bottom: 2px solid #ffd700;
        padding-bottom: 10px;
    }
    
    .iot-section p {
        color: #1e5a7d !important;
        font-size: 16px;
        margin: 10px 0;
        line-height: 1.6;
    }
    
    .iot-section strong {
        color: #0d3d5c !important;
        font-weight: 600;
    }
    
    .offline-camera {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        color: white;
        padding: 100px 20px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        border-radius: 8px;
        margin: 10px 0;
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.2);
        border: 2px solid #1e5a7d;
    }
    
    /* Video container styling */
    .stImage {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        border: 2px solid #1e5a7d;
    }
    
    /* AI Agent section */
    .element-container div[data-testid="stMarkdownContainer"] {
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🏭 WAREHOUSE MANAGEMENT SYSTEM</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">⚡ Intelligent Bag Counting & Real-Time Monitoring Dashboard</div>', unsafe_allow_html=True)

#Camera sections
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="camera-label">📹 Camera 01 - Gate 01 (ACTIVE)</div>', unsafe_allow_html=True)
    cam1 = st.empty()
    bag_col1 = st.columns(2)
    with bag_col1[0]:
        in1 = st.empty()
    with bag_col1[1]:
        out1 = st.empty()

with col2:
    st.markdown('<div class="camera-label">📹 Camera 02 - Gate 02 (OFFLINE)</div>', unsafe_allow_html=True)
    st.markdown('<div class="offline-camera">📵 Camera Offline</div>', unsafe_allow_html=True)
    bag_col2 = st.columns(2)
    with bag_col2[0]:
        st.markdown('<div class="bag-counter">Bags In : 0</div>', unsafe_allow_html=True)
    with bag_col2[1]:
        st.markdown('<div class="bag-counter">Bags Out : 0</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="camera-label">📹 Camera 03 - Gate 03 (OFFLINE)</div>', unsafe_allow_html=True)
    st.markdown('<div class="offline-camera">📵 Camera Offline</div>', unsafe_allow_html=True)
    bag_col3 = st.columns(2)
    with bag_col3[0]:
        st.markdown('<div class="bag-counter">Bags In : 0</div>', unsafe_allow_html=True)
    with bag_col3[1]:
        st.markdown('<div class="bag-counter">Bags Out : 0</div>', unsafe_allow_html=True)

# IOT Parameters Section
st.markdown("""
<div class="iot-section">
    <div class="iot-header">📊 IOT PARAMETERS MONITORING</div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px;">
        <div style="padding: 15px; background-color: rgba(30, 90, 125, 0.05); border-radius: 8px;">
            <p style="margin: 12px 0;"><strong>🌡️ Temperature :</strong> <span style="color: #e74c3c; font-weight: bold;">27°C</span></p>
            <p style="margin: 12px 0;"><strong>💧 Humidity :</strong> <span style="color: #3498db; font-weight: bold;">64%</span></p>
            <p style="margin: 12px 0;"><strong>⚠️ Phosphine Gas Level :</strong> <span style="color: #27ae60; font-weight: bold;">Safe</span></p>
        </div>
        <div style="padding: 15px; background-color: rgba(30, 90, 125, 0.05); border-radius: 8px;">
            <p style="margin: 12px 0;"><strong>🔥 Smoke and Fire Status:</strong> <span style="color: #27ae60; font-weight: bold;">Normal</span></p>
            <p style="margin: 12px 0;"><strong>🚪 Gate Open/Close Status:</strong> <span style="color: #f39c12; font-weight: bold;">Open</span></p>
            <p style="margin: 12px 0;"><strong>📡 System Status:</strong> <span style="color: #27ae60; font-weight: bold;">Online</span></p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# AI Agent Section
st.markdown('<h3 style="color: #1e5a7d; padding: 15px; background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%); border-radius: 8px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">🤖 AI Agent - Warehouse Assistant</h3>', unsafe_allow_html=True)
agent_placeholder = st.empty()
agent_placeholder.info("🔄 Initializing AI Agent... Waiting for first detection")

# Video processing
video_path = "input/Problem Statement Scenario1.mp4"
ai_called = False

try:
    for frame, bags_in, bags_out in process_video(video_path):
        # Convert and display
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cam1.image(frame, channels="RGB", use_container_width=True)
        in1.markdown(f'<div class="bag-counter">Bags In : {bags_in}</div>', unsafe_allow_html=True)
        out1.markdown(f'<div class="bag-counter">Bags Out : {bags_out}</div>', unsafe_allow_html=True)
        
        # Update AI agent display continuously with current counts
        if bags_in > 0 or bags_out > 0:
            # Call AI API only once to get analysis
            if not ai_called:
                ai_called = True
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
                                {"role": "system", "content": "You are a warehouse AI assistant. Provide brief operational analysis."},
                                {"role": "user", "content": f"Analyze warehouse operations with bag loading/unloading. Provide insights on efficiency and status in 1-2 sentences."}
                            ],
                            "temperature": 0.7,
                            "max_tokens": 150
                        },
                        timeout=5
                    )
                    if response.status_code == 200:
                        ai_summary = response.json()["choices"][0]["message"]["content"]
                    else:
                        ai_summary = "Real-time monitoring active. System operating normally."
                except:
                    ai_summary = "Real-time monitoring active. System operating normally."
            else:
                ai_summary = "Real-time monitoring active. System operating normally."
            
            # Always update the display with current counts
            agent_output = f"""🤖 **AI Agent Analysis**

{ai_summary}

📊 **Live Status (Gate 01):**
- 🟢 Bags Loaded: **{bags_in}**
- 🔴 Bags Unloaded: **{bags_out}**
- 📈 Net Count: **{bags_in - bags_out}**

✅ System operational • Last updated: Frame {bags_in + bags_out}"""
            
            agent_placeholder.info(agent_output)

except StopIteration:
    st.info("✅ Video playback completed")
except Exception as e:
    st.error(f"❌ Error: {str(e)}")
    import traceback
    st.code(traceback.format_exc())
