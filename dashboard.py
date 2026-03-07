import streamlit as st
import cv2
import numpy as np
import os
from bag_counter import process_video

st.set_page_config(layout="wide", page_title="Warehouse Management System")

# Custom CSS to match the reference dashboard design with improved UI
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
    
    .gate-label {
        background: linear-gradient(135deg, #1e5a7d 0%, #2a7aa3 100%);
        color: white;
        padding: 12px;
        text-align: center;
        font-weight: bold;
        font-size: 18px;
        border-radius: 8px;
        margin: 8px 0;
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
    
    /* Video container styling */
    .stImage {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        border: 2px solid #1e5a7d;
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
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<div class="main-header">🏭 WAREHOUSE MANAGEMENT SYSTEM</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">⚡ Intelligent Bag Counting & Real-Time Monitoring Dashboard</div>', unsafe_allow_html=True)

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

# Display all 3 video feeds simultaneously
video_paths = [
    "input/Problem Statement Scenario1.mp4",
    "input/Problem Statement Scenario2.mp4",
    "input/Problem Statement Scenario3.mp4"
]

first_frame = True
agent_called = False

# IOT Parameters Section with styled background (before video loop so it's always visible)
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

# Create generators for all 3 videos
try:
    video_generators = [process_video(path) for path in video_paths]
except Exception as e:
    st.error(f"Failed to initialize video processors: {e}")
    st.stop()

# Process all videos frame by frame
try:
    while True:
        # Get frame from each video
        try:
            frame1, bags_in1, bags_out1 = next(video_generators[0])
            frame2, bags_in2, bags_out2 = next(video_generators[1])
            frame3, bags_in3, bags_out3 = next(video_generators[2])
        except StopIteration:
            st.info("✅ All video playback completed")
            st.stop()
        
        # Convert and display Camera 1
        frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        cam1.image(frame1, channels="RGB", width="stretch")
        in1.markdown(f'<div class="bag-counter">Bags In : {bags_in1}</div>', unsafe_allow_html=True)
        out1.markdown(f'<div class="bag-counter">Bags Out : {bags_out1}</div>', unsafe_allow_html=True)
        
        # Convert and display Camera 2
        frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
        cam2.image(frame2, channels="RGB", width="stretch")
        in2.markdown(f'<div class="bag-counter">Bags In : {bags_in2}</div>', unsafe_allow_html=True)
        out2.markdown(f'<div class="bag-counter">Bags Out : {bags_out2}</div>', unsafe_allow_html=True)
        
        # Convert and display Camera 3
        frame3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2RGB)
        cam3.image(frame3, channels="RGB", width="stretch")
        in3.markdown(f'<div class="bag-counter">Bags In : {bags_in3}</div>', unsafe_allow_html=True)
        out3.markdown(f'<div class="bag-counter">Bags Out : {bags_out3}</div>', unsafe_allow_html=True)
        
        # Update AI agent continuously with live counts
        total_bags_in = bags_in1 + bags_in2 + bags_in3
        total_bags_out = bags_out1 + bags_out2 + bags_out3
        
        if total_bags_in > 0 or total_bags_out > 0:
            # Call AI API only once for analysis
            if not agent_called:
                agent_called = True
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
                                {"role": "user", "content": f"Analyze multi-gate warehouse operations with bag loading/unloading across 3 gates. Provide efficiency insights in 1-2 sentences."}
                            ],
                            "temperature": 0.7,
                            "max_tokens": 150
                        },
                        timeout=5
                    )
                    if response.status_code == 200:
                        ai_summary = response.json()["choices"][0]["message"]["content"]
                    else:
                        ai_summary = "Multi-gate warehouse monitoring active. All systems operational."
                except:
                    ai_summary = "Multi-gate warehouse monitoring active. All systems operational."
            else:
                ai_summary = "Multi-gate warehouse monitoring active. All systems operational."
            
            # Always update display with current counts
            agent_output = f"""🤖 **AI Agent Analysis**

{ai_summary}

📊 **Live Status (All Gates):**
- 🟢 Total Loaded: **{total_bags_in}** bags
- 🔴 Total Unloaded: **{total_bags_out}** bags
- 📈 Net Count: **{total_bags_in - total_bags_out}** bags

**Per Gate Breakdown:**
• Gate 01: {bags_in1} in / {bags_out1} out
• Gate 02: {bags_in2} in / {bags_out2} out  
• Gate 03: {bags_in3} in / {bags_out3} out

✅ Real-time monitoring active"""
            
            agent_placeholder.info(agent_output)
            first_frame = False

except StopIteration:
    st.info("✅ All video playback completed")
except Exception as e:
    st.error(f"❌ Error: {str(e)}")