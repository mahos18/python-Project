import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)  # Detect only one hand
mp_draw = mp.solutions.drawing_utils

# Open webcam
cap = cv2.VideoCapture(0)

# Finger tips landmarks as per MediaPipe
finger_tips_ids = [4, 8, 12, 16, 20]

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)  # Flip the frame horizontally
    h, w, c = frame.shape

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)

    count = 0

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            landmarks = hand_landmarks.landmark

            # Thumb
            if landmarks[finger_tips_ids[0]].x < landmarks[finger_tips_ids[0] - 1].x:
                count += 1

            # Fingers (except thumb)
            for id in range(1, 5):
                if landmarks[finger_tips_ids[id]].y < landmarks[finger_tips_ids[id] - 2].y:
                    count += 1

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display the number of fingers
    cv2.putText(frame, f'Fingers: {count}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX,
                2, (255, 0, 0), 3)

    cv2.imshow("Finger Counter", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' key to exit
        break

cap.release()
cv2.destroyAllWindows()
