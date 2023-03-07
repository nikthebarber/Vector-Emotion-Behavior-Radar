import anki_vector
from anki_vector import events, behavior, lights
import time
from datetime import datetime

from emotions import EmotionDetector, EmotionReaction
from config import VECTOR_NAME, VECTOR_BEHAVIOR_PATH


def main():
    # Connect to Vector
    with anki_vector.Robot(VECTOR_NAME, behavior_control_level=None) as robot:
        print(f"Connected to {robot.serial}")

        # Initialize emotion detector and reaction
        detector = EmotionDetector()
        reaction = EmotionReaction(robot)

        # Wait for Vector to finish connecting
        robot.behavior.set_eye_color(lights.blue_light)
        robot.behavior.say_text("Hello, I'm awake now", duration_scalar=0.5)
        robot.behavior.drive_off_charger()

        # Set Vector's initial state
        reaction.react("happy")

        # Add event listener for cube placement
        robot.events.subscribe(on_cube_placed_on_ground, events.Events.object_observed)

        # Drive around and detect emotions
        while True:
            # Detect emotion
            emotion = detector.detect_emotion()

            # React to emotion
            reaction.react(emotion)

            # Delay for a short period to prevent spamming API
            time.sleep(0.1)


def on_cube_placed_on_ground(robot, event_type, event):
    """
    A function that is called when Vector observes a cube being placed on the ground
    """
    robot.behavior.say_text("I see a cube!", duration_scalar=0.5)
    robot.behavior.set_cube_lights(lights.white_light)
    robot.behavior.drive_to_object(event.obj, distance_from_object=distance_mm(80.0))


if __name__ == "__main__":
    main()
