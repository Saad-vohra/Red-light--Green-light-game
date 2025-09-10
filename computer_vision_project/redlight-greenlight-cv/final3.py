import cv2
import mediapipe as mp
import time
import pygame
import numpy as np

# Initialize Pygame mixer
pygame.mixer.init()

# Load sound effects 
gunshot = pygame.mixer.Sound("redlight-greenlight-cv\gunshot.wav.mp3")
green_light_music = pygame.mixer.Sound("redlight-greenlight-cv\Mingle Game Squid Game Ringtone Download - MobCup.Com.Co.mp3")
green_light_music.set_volume(0.4)


# Load and resize doll images
doll_front = cv2.imread("redlight-greenlight-cv\doll_front.png")
doll_back = cv2.imread("C:\\Users\\saado\\OneDrive\\Pictures\\Screenshots\\Screenshot 2025-04-18 223446.png")
doll_front = cv2.resize(doll_front, (300, 200))
doll_back = cv2.resize(doll_back, (300, 200))

# Mediapipe Pose Setup
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

# Webcam setup
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Game state variables
prev_landmarks = None
motion_detected = False
light = "green"
last_switch = time.time()
game_over = False
start_time = time.time()
game_duration = 180  # seconds
player_progress = 0  # 0=start, 500=win

def check_motion(landmarks, prev_landmarks, threshold=15):
    if not prev_landmarks:
        return False
    for i, lm in enumerate(landmarks):
        x_diff = abs(lm.x - prev_landmarks[i].x)
        y_diff = abs(lm.y - prev_landmarks[i].y)
        if x_diff > threshold / 100 or y_diff > threshold / 100:
            return True
    return False

def show_result(text, color):
    result_frame = np.zeros((720, 1280, 3), dtype=np.uint8)
    cv2.putText(result_frame, text, (350, 360), cv2.FONT_HERSHEY_SIMPLEX, 3, color, 8)
    cv2.imshow("Red-Green Game", result_frame)
    cv2.waitKey(3000)
    cap.release()
    cv2.destroyAllWindows()
    exit()

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(frame_rgb)

    # Light switching logic every 3 seconds
    if time.time() - last_switch > 3:
        light = "red" if light == "green" else "green"
        last_switch = time.time()
        if light == "green":
            green_light_music.play(-1)
        else:
            green_light_music.stop()

    # Pose detection and motion check
    if result.pose_landmarks:
        mp_draw.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        motion_detected = check_motion(result.pose_landmarks.landmark, prev_landmarks)
        prev_landmarks = result.pose_landmarks.landmark
    else:
        motion_detected = False

    # Top camera view resized
    top_frame = cv2.resize(frame, (1280, 400))

    # Show timer
    elapsed = time.time() - start_time
    remaining = max(0, int(game_duration - elapsed))
    cv2.putText(top_frame, f"Time Left: {remaining}s", (1000, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)

    # Show light status
    if light == "green":
        cv2.putText(top_frame, "Green Light", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 5)
    else:
        cv2.putText(top_frame, "Red Light", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)

    # Eliminate if motion during red light
    if motion_detected and light == "red" and not game_over:
        gunshot.play()
        game_over = True
        result_frame = np.zeros((720, 1280, 3), dtype=np.uint8)
        cv2.putText(result_frame, "ELIMINATED", (350, 360), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 8)
        cv2.imshow("Red-Green Game", result_frame)
        cv2.waitKey(3000)
        cap.release()
        cv2.destroyAllWindows()
        break

    # Move dot forward only if player moves during green light
    if light == "green" and motion_detected and not game_over:
        player_progress += 10
        if player_progress >= 500:
            player_progress = 500

    # Bottom area (progress and doll)
    bottom_area = np.zeros((250, 1280, 3), dtype=np.uint8)

    # Draw full progress line
    start_point = (100, 200)
    end_point = (600, 200)
    cv2.line(bottom_area, start_point, end_point, (255, 255, 255), 4)

    # Draw moving dot
    dot_x = 100 + player_progress
    cv2.circle(bottom_area, (dot_x, 200), 15, (0, 255, 255), -1)

    # Draw doll image
    doll_img = doll_back if light == "green" else doll_front
    bottom_area[20:220, 980:1280] = doll_img

    # Combine top and bottom
    combined = cv2.vconcat([top_frame, bottom_area])

    # Progress bar (bottom-wide)
    progress_bar_width = int((elapsed / game_duration) * 1200)
    cv2.rectangle(combined, (40, 660), (1240, 675), (100, 100, 100), -1)
    cv2.rectangle(combined, (40, 660), (40 + progress_bar_width, 675), (0, 255, 0), -1)

    # Show the full game window
    cv2.imshow("Red-Green Game", combined)

    # Win condition
    if player_progress >= 500 and not game_over:
        show_result("YOU WON", (0, 255, 0))

    # Time's up condition
    if elapsed >= game_duration and not game_over:
        show_result("TIME'S UP", (0, 0, 255))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
