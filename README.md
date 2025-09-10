# Red-light--Green-light-game
This game is based on famous Netflix series 'Squid Game' , which is created through python and it's library.

🟢🔴 Red Light – Green Light Game

A computer vision-based Red Light – Green Light game inspired by Squid Game.
The game uses Python, OpenCV, and Mediapipe to track player motion through a webcam feed.
Players must freeze during Red Light and move only during Green Light to win.

🚀 Features
🎥 Webcam Integration – real-time video capture.
🧍 Pose Detection – uses Mediapipe for full-body tracking.
🟩 Green Light Mode – player can move forward.
🟥 Red Light Mode – player must stay still; motion leads to elimination.
🔊 Sound Effects – background music, doll voice, and gunshot sounds.
🕹️ Game Status Display – "YOU WON" if you reach the finish line, "ELIMINATED" if you move during red light.
⏱️ Timer Support – optional countdown timer for the match.
🎨 UI Elements – top section shows webcam with detection, bottom shows doll images changing with red/green light.


🛠️ Tech Stack
Programming Language: Python 3.x
Libraries:
OpenCV – for video processing
Mediapipe – for pose detection
Pygame – for sound effects
Numpy – for computations


▶️ How to Run
1) Clone the repository
2) Install dependencies (from requirements.txt)
   pip install -r requirements.txt
3) Run the game


🖥️ Gameplay Instructions

1)Stand in front of your webcam.
2) When the doll says “Green Light” 🟢 – you may move forward.
3) When it says “Red Light” 🔴 – freeze completely!
4) If motion is detected during Red Light, you’ll hear a gunshot 🔫 and see ELIMINATED.
5) Reach the finish line before the timer runs out to see YOU WON 🎉.
