import os
from ultralytics import YOLO
import cv2

video_path = "E:\\Arquivos\\ai-want-coffee\\data\\sample_videos\\cozinha01.mp4"

file_name_without_extension = os.path.splitext(os.path.basename(video_path))[0]
output_dir = "E:\\Arquivos\\ai-want-coffee\\data\\results"

video_path_out = os.path.join(output_dir, f"{file_name_without_extension}.mp4")

cap = cv2.VideoCapture(video_path)

ret, frame = cap.read()    
H, W, _ = frame.shape
out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'MP4V'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))

model = YOLO('yolov8n.pt')

threshold = 0.5

while ret:

    results = model(frame)[0]

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

    out.write(frame)
    ret, frame = cap.read()

cap.release()
out.release()
cv2.destroyAllWindows()