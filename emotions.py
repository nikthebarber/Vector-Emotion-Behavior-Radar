import anki_vector
from anki_vector import events, behavior, lights
from anki_vector.util import degrees, distance_mm, speed_mmps
import random
from datetime import datetime
import time

from reaction_detector import EmotionDetector, EmotionReaction
from config import VECTOR_NAME, VECTOR_BEHAVIOR_PATH, EYE_COLORS, DEFAULT_EYE_COLOR, CUBE_LIGHT_COLORS, \
    DEFAULT_CUBE_LIGHT_COLOR


def main():
    # Connect to Vector robot
    with anki_vector.Robot(name=VECTOR_NAME) as robot:
        robot.behavior.drive_off_charger()
        robot.behavior.set_head_angle(degrees(0))

        # Instantiate emotion detector and reaction
        detector = EmotionDetector(robot)
        reaction = EmotionReaction(robot)

        # Set default eye and cube light colors
        robot.behavior.set_eye_color(DEFAULT_EYE_COLOR)
        robot.behavior.set_cube_lights(DEFAULT_CUBE_LIGHT_COLOR)

        # Wait for robot to detect a face and emotion
        while True:
            robot.behavior.say_text("Hi, I'm Vector. Let's talk about your emotions.")
            event = robot.world.wait_for_events(events.FaceObservedEvent)

            if isinstance(event, events.FaceObservedEvent):
                if event.face and event.face.expression:
                    robot.behavior.say_text("I see that you are feeling " + event.face.expression.name)

                    # Determine emotion and react accordingly
                    emotion = detector.get_emotion(event.face.expression.name)
                    reaction.react(emotion)

if __name__ == "__main__":
    main()
