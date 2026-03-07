"""
Create a demo video clip showing the bag counting system in action
This will process the first 300 frames (~10 seconds) and save as demo_clip.mp4
"""

import cv2
from bag_counter import process_video
from tqdm import tqdm

print("🎬 Creating demo clip from Scenario 1...")
print("This will take a few minutes...\n")

# Output video settings
output_path = "demo_clip.mp4"
fps = 30
width = 1280
height = 720
max_frames = 300  # 10 seconds at 30 fps

# Initialize video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

try:
    frame_count = 0
    
    print(f"Processing {max_frames} frames...")
    for frame, bags_in, bags_out in tqdm(process_video("input/Problem Statement Scenario1.mp4"), 
                                          total=max_frames, 
                                          desc="Creating demo"):
        if frame_count >= max_frames:
            break
        
        # Resize to 720p
        frame_resized = cv2.resize(frame, (width, height))
        
        # Write frame
        out.write(frame_resized)
        frame_count += 1
        
        # Status update
        if frame_count % 50 == 0:
            print(f"  Progress: {frame_count}/{max_frames} frames | Bags In: {bags_in} | Bags Out: {bags_out}")
    
    print(f"\n✅ Demo clip created successfully!")
    print(f"   Output: {output_path}")
    print(f"   Duration: {frame_count/fps:.1f} seconds")
    print(f"   Resolution: {width}x{height}")
    print(f"   Size: {cv2.os.path.getsize(output_path) / (1024*1024):.2f} MB")
    
except Exception as e:
    print(f"❌ Error creating demo: {e}")
    import traceback
    traceback.print_exc()
    
finally:
    out.release()
    cv2.destroyAllWindows()

print("\n📋 Next steps:")
print("1. Upload demo_clip.mp4 to GitHub (via Issues > New Issue > drag & drop)")
print("2. Copy the generated URL")
print("3. Update README.md line ~13 with the video URL")
print("4. Commit and push: git add README.md && git commit -m 'docs: Add demo video' && git push")
print("\nSee DEMO_INSTRUCTIONS.md for detailed guide!")
