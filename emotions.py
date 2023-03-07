import anki_vector
from anki_vector import events, behavior, lights
import random
from datetime import datetime
import time

from emotion_engine import EmotionDetector, EmotionReaction
from config import VECTOR_NAME, VECTOR_BEHAVIOR_PATH, EYE_COLORS, DEFAULT_EYE_COLOR, \
    CUBE_LIGHT_COLORS, DEFAULT_CUBE_LIGHT_COLOR


def main():
    with anki_vector.Robot(name=VECTOR_NAME) as robot:
        robot.behavior.set_eye_color(DEFAULT_EYE_COLOR)
        robot.behavior.set_cube_lights(DEFAULT_CUBE_LIGHT_COLOR)
        robot.behavior.drive_off_charger()

        detector = EmotionDetector(robot)
        reaction = EmotionReaction(robot)

        def on_object_observed(event_type, event):
            emotion = detector.get_emotion(event.obj)
            print(f"Detected emotion: {emotion}")
            reaction.react(emotion)

        robot.events.subscribe(on_object_observed, events.Events.object_observed)

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
