# 📹 Creating Demo Clip for README

## Method 1: Using OBS Studio (Recommended)

### Install OBS Studio
1. Download from: https://obsproject.com/
2. Install and launch OBS Studio

### Record Dashboard
1. Start your dashboard: `py -m streamlit run dashboard_working.py`
2. Open browser to http://localhost:8501
3. In OBS Studio:
   - Click "+" under Sources
   - Select "Window Capture"
   - Choose your browser window
   - Adjust frame to capture entire dashboard
   - Click "Start Recording"
4. Let it run for 30-60 seconds showing:
   - Live video feed
   - Counters updating
   - IOT parameters
   - AI agent analysis
5. Click "Stop Recording"
6. Video saved in: Videos folder (default)

### Optimize Video
```bash
# Compress video (optional)
ffmpeg -i recording.mp4 -vcodec h264 -acodec aac -b:v 2M demo.mp4
```

---

## Method 2: Windows Game Bar (Quick Method)

### For Windows 10/11:
1. Start dashboard: `py -m streamlit run dashboard_working.py`
2. Open browser to http://localhost:8501
3. Press `Win + G` to open Game Bar
4. Click "Capture" icon
5. Click "Start Recording" (or press `Win + Alt + R`)
6. Record for 30-60 seconds
7. Press `Win + Alt + R` to stop
8. Video saved in: `C:\Users\[YourName]\Videos\Captures`

---

## Method 3: Create Output Video from Python

### Run the video processing script:
```python
# This will create output_scenario1.mp4 in project root
python quick_test.py
```

Then use the generated video as demo!

---

## Adding Demo to GitHub README

### Step 1: Upload Video to GitHub
1. Go to your repo: https://github.com/Zesterdock/Deep-Learning-Assignment
2. Click "Issues" tab
3. Click "New Issue"
4. In the issue body, drag and drop your demo video
5. Wait for upload to complete
6. Copy the generated URL (will look like: `https://github.com/user-attachments/assets/...`)
7. You can close the issue without submitting

### Step 2: Update README
1. Open `README.md`
2. Find line ~13 with: `https://github.com/user-attachments/assets/your-demo-video-id-here`
3. Replace with your actual video URL
4. Commit and push:
```bash
git add README.md
git commit -m "docs: Add demo video to README"
git push origin main
```

---

## Alternative: Create GIF Demo

### Using FFmpeg
```bash
# Create GIF from video (first 10 seconds, 10 fps)
ffmpeg -i demo.mp4 -t 10 -vf "fps=10,scale=1280:-1:flags=lanczos" demo.gif

# Optimize GIF size
ffmpeg -i demo.mp4 -vf "fps=5,scale=800:-1:flags=lanczos" -t 15 demo_optimized.gif
```

### Upload GIF to README
```markdown
![Dashboard Demo](demo.gif)
```

---

## Recommended Demo Content

### Show these features in your demo:
1. ✅ **Dashboard Loading** (2-3 seconds)
   - Show main header and layout

2. ✅ **Live Video Feed** (10 seconds)
   - Camera 1 with active bag detection
   - Red detection boxes around bags
   - Line crossing visualization

3. ✅ **Counter Updates** (10 seconds)
   - Zoom in to show "Bags In" counting up
   - Show AI agent display updating

4. ✅ **IOT Parameters** (5 seconds)
   - Pan down to show all IOT values
   - Highlight colored status indicators

5. ✅ **AI Agent Analysis** (5 seconds)
   - Show live status with real-time counts
   - Demonstrate continuous updates

### Total Demo Length: 30-40 seconds (ideal)

---

## Quick Demo Script (Automated)

Create `create_demo.py`:
```python
import cv2
from bag_counter import process_video

# Process first 300 frames (~10 seconds at 30 fps)
out = cv2.VideoWriter('demo_clip.mp4', 
                      cv2.VideoWriter_fourcc(*'mp4v'), 
                      30, (1280, 720))

frame_count = 0
for frame, bags_in, bags_out in process_video("input/Problem Statement Scenario1.mp4"):
    if frame_count > 300:
        break
    
    # Resize to 720p
    frame = cv2.resize(frame, (1280, 720))
    out.write(frame)
    frame_count += 1
    
    if frame_count % 30 == 0:
        print(f"Processed {frame_count} frames...")

out.release()
print("✅ Demo clip created: demo_clip.mp4")
```

Run: `python create_demo.py`

---

## GitHub Video Requirements
- **Max size:** 10MB (for direct upload) or 100MB (via Git LFS)
- **Formats:** MP4, MOV, WebM recommended
- **Duration:** 30-60 seconds ideal for README
- **Resolution:** 1280x720 or 1920x1080

---

## Final Checklist
- [ ] Demo video shows live bag counting
- [ ] Counter values are clearly visible
- [ ] AI agent analysis is shown
- [ ] IOT parameters section visible
- [ ] Video is under 10MB
- [ ] Video uploaded to GitHub
- [ ] README updated with video URL
- [ ] Changes committed and pushed
