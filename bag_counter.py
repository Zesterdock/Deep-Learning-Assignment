import cv2
from ultralytics import YOLO

model = YOLO("runs/detect/train/weights/best.pt")

def process_video(input_path):

    counted_ids_in = set()
    counted_ids_out = set()
    previous_positions = {}

    bags_in = 0
    bags_out = 0
    line_x = None

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

        if line_x is None:
            line_x = int(width * 0.5)

        boxes = result.boxes

        cv2.line(frame, (line_x, 0), (line_x, height), (0,0,255), 3)

        if boxes.id is not None:

            for box, track_id in zip(boxes.xyxy, boxes.id):

                x1, y1, x2, y2 = map(int, box)
                track_id = int(track_id)

                cx = (x1+x2)//2

                if track_id in previous_positions:

                    prev_x = previous_positions[track_id]

                    # RIGHT → LEFT  (Loading)
                    if prev_x > line_x and cx <= line_x:
                        if track_id not in counted_ids_in:
                            bags_in += 1
                            counted_ids_in.add(track_id)

                    # LEFT → RIGHT (Unloading)
                    elif prev_x < line_x and cx >= line_x:
                        if track_id not in counted_ids_out:
                            bags_out += 1
                            counted_ids_out.add(track_id)

                previous_positions[track_id] = cx

                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)

        cv2.putText(frame,f"Bags In: {bags_in}",(20,50),
                    cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

        cv2.putText(frame,f"Bags Out: {bags_out}",(20,90),
                    cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)

        yield frame,bags_in,bags_out