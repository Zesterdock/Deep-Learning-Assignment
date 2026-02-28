import cv2
import os

videos = [
    "input/Problem Statement Scenario1.mp4",
    "input/Problem Statement Scenario2.mp4",
    "input/Problem Statement Scenario3.mp4"
]

output_folder = "dataset/images"
os.makedirs(output_folder, exist_ok=True)

frame_count = 0

for video in videos:
    cap = cv2.VideoCapture(video)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Save every 10th frame
        if frame_count % 10 == 0:
            cv2.imwrite(f"{output_folder}/frame_{frame_count}.jpg", frame)

        frame_count += 1

    cap.release()

print("Frame extraction complete!")