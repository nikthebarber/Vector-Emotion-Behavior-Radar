import anki_vector
import cv2
import numpy as np
import random
import time

# Configuration
VECTOR_NAME = "Vector"
CURSE_WORDS_ENABLED = True
CURSE_WORDS = {
    "angry": ["Fuck!", "Shit!", "Asshole!", "Motherfucker!"],
    "happy": ["Yeah baby!", "Awesome!", "Sweet!", "Amazing!"],
    "sad": ["Sucks!", "Damn it!", "Shit!", "WTF!"],
    "surprised": ["Holy shit!", "What the hell!", "OMG!", "No way!"]
}
REACTIONS = {
    "angry": [
        "You're making me angry, %s!",
        "I'm getting pissed off, %s!",
        "Why are you being such a jerk, %s?",
        "Stop pissing me off, %s!"
    ],
    "happy": [
        "You're making me happy, %s!",
        "I'm feeling good, %s!",
        "Why are you so awesome, %s?",
        "Keep up the good work, %s!"
    ],
    "sad": [
        "You're making me sad, %s!",
        "I'm feeling down, %s!",
        "Why are you being mean, %s?",
        "Stop making me feel bad, %s!"
    ],
    "surprised": [
        "You're surprising me, %s!",
        "I'm shocked, %s!",
        "Why didn't I see that coming, %s?",
        "Keep surprising me, %s!"
    ]
}
EMOTIONS = ["angry", "happy", "sad", "surprised"]
EMOTION_COLORS = {
    "angry": (255, 0, 0),    # red
    "happy": (0, 255, 0),    # green
    "sad": (0, 0, 255),      # blue
    "surprised": (255, 255, 0)   # yellow
}
EMOTION_THRESHOLDS = {
    "angry": 0.5,
    "happy": 0.5,
    "sad": 0.5,
    "surprised": 0.5
}
ANIMATION_DURATION = 1.0   # seconds

# Initialize Vector
with anki_vector.Robot(VECTOR_NAME) as robot:
    robot.behavior.set_head_angle(anki_vector.util.degrees(45.0))
    robot.behavior.set_lift_height(0.0)
    robot.behavior.set_eye_color((0, 0, 0))

    # Initialize face detection
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    video_capture = cv2.VideoCapture(0)

    # Main loop
    while True:
        # Capture frame from camera
        ret, frame = video_capture.read()

        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # Check if a face is detected
        if len(faces) > 0:
            # Get the largest face
            (x, y, w, h) = max(faces, key=lambda face: face[2] * face[3])

            #
