import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import cv2
import numpy as np
import mediapipe as mp

# Initialize MediaPipe Hand model
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Create a larger blank canvas to draw on (720p resolution)
canvas = np.zeros((720, 1280, 3), dtype=np.uint8)

# Start webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Cannot access camera")
    exit()

# MediaPipe Hands setup
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
prev_x, prev_y = None, None
smoothing_factor = 0.2

# Smoothed fingertip position
smoothed_x, smoothed_y = None, None

# Drawing state
drawing_enabled = False
eraser_mode = False
line_thickness = 20
drawing_color = (255, 255, 255)

print("[INFO] Use your index finger to draw.")
print("[INFO] Press 'a' to pause/resume drawing.")
print("[INFO] Press 'e' to toggle eraser mode.")
print("[INFO] Press 'c' to clear, 's' to save canvas, 'q' to quit.")
print("[INFO] Press '1', '2', '3', '4' to change color (White, Red, Blue, Green).")
print("[INFO] Press '+' or '-' to adjust line thickness.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to grab frame")
        break

    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (1280, 720))
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            index_finger = hand_landmarks.landmark[8]
            h, w, _ = frame.shape
            x, y = int(index_finger.x * w), int(index_finger.y * h)

            if smoothed_x is None or smoothed_y is None:
                smoothed_x, smoothed_y = x, y
            else:
                smoothed_x = int(smoothed_x * (1 - smoothing_factor) + x * smoothing_factor)
                smoothed_y = int(smoothed_y * (1 - smoothing_factor) + y * smoothing_factor)

            if drawing_enabled and prev_x is not None and prev_y is not None:
                if eraser_mode:
                    cv2.line(canvas, (prev_x, prev_y), (smoothed_x, smoothed_y), (0, 0, 0), line_thickness)
                else:
                    cv2.line(canvas, (prev_x, prev_y), (smoothed_x, smoothed_y), drawing_color, line_thickness)

            prev_x, prev_y = smoothed_x, smoothed_y
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    else:
        prev_x, prev_y = None, None

    overlay = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)
    cv2.putText(overlay, f"Drawing: {'ON' if drawing_enabled else 'OFF'}", (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if drawing_enabled else (0, 0, 255), 2)
    cv2.putText(overlay, f"Eraser: {'ON' if eraser_mode else 'OFF'}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if eraser_mode else (0, 0, 255), 2)
    cv2.putText(overlay, f"Thickness: {line_thickness}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow("Teaching Board", overlay)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('a'):
        drawing_enabled = not drawing_enabled
        print(f"[INFO] Drawing {'enabled' if drawing_enabled else 'paused'}.")
    elif key == ord('e'):
        eraser_mode = not eraser_mode
        print(f"[INFO] Eraser {'enabled' if eraser_mode else 'disabled'}.")
    elif key == ord('c'):
        canvas[:] = 0
        print("[INFO] Canvas cleared.")
    elif key == ord('s'):
        cv2.imwrite("teaching_canvas.png", canvas)
        print("[INFO] Canvas saved as 'teaching_canvas.png'.")
    elif key == ord('1'):
        drawing_color = (255, 255, 255)
        print("[INFO] Drawing color set to White.")
    elif key == ord('2'):
        drawing_color = (0, 0, 255)
        print("[INFO] Drawing color set to Red.")
    elif key == ord('3'):
        drawing_color = (255, 0, 0)
        print("[INFO] Drawing color set to Blue.")
    elif key == ord('4'):
        drawing_color = (0, 255, 0)
        print("[INFO] Drawing color set to Green.")
    elif key == ord('+'):
        line_thickness = min(line_thickness + 1, 50)
        print(f"[INFO] Line thickness increased to {line_thickness}.")
    elif key == ord('-'):
        line_thickness = max(line_thickness - 1, 1)
        print(f"[INFO] Line thickness decreased to {line_thickness}.")
    elif key == ord('q'):
        print("[INFO] Exiting...")
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
