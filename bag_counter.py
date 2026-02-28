import cv2
from ultralytics import YOLO

# Loading the trained custom model
model = YOLO("runs/detect/train/weights/best.pt")


def process_video(input_path, output_path):

    counted_ids = set()
    previous_positions = {}
    total_count = 0
    line_x = None
    out = None

    results = model.track(
        source=input_path,
        persist=True,
        tracker="bytetrack.yaml",
        stream=True,
        conf=0.5
    )

    for result in results:

        frame = result.orig_img
        height, width = frame.shape[:2]

        # Place vertical line
        if line_x is None:
            line_x = int(width * 0.6)

        boxes = result.boxes

        # Draw counting line
        cv2.line(frame, (line_x, 0), (line_x, height), (0, 0, 255), 3)

        if boxes.id is not None:

            for box, track_id in zip(boxes.xyxy, boxes.id):

                x1, y1, x2, y2 = map(int, box)
                track_id = int(track_id)

                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2

                
                if track_id in previous_positions:
                    prev_x = previous_positions[track_id]

                    if prev_x > line_x and cx <= line_x:
                        if track_id not in counted_ids:
                            counted_ids.add(track_id)
                            total_count += 1
                            print(f"Counted ID: {track_id}")

                previous_positions[track_id] = cx

                
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"ID {track_id}",
                            (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6, (0, 255, 0), 2)

                cv2.circle(frame, (cx, cy), 4, (255, 0, 0), -1)

        
        cv2.putText(frame, f"Total Bags: {total_count}",
                    (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3)

        
        if out is None:
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            out = cv2.VideoWriter(output_path, fourcc, 25, (width, height))

        out.write(frame)

    if out is not None:
        out.release()

    print(f"Final Count for {input_path}: {total_count}")


# Process all scenarios
process_video("input/Problem Statement Scenario1.mp4", "outputs/output_scenario1.mp4")
process_video("input/Problem Statement Scenario2.mp4", "outputs/output_scenario2.mp4")
process_video("input/Problem Statement Scenario3.mp4", "outputs/output_scenario3.mp4")