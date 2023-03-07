import requests
import json
import random

from config import API_KEY, API_URL, DEFAULT_EMOTION


class EmotionDetector:
    """
    A class that detects emotion using the Microsoft Azure Emotion API
    """

    def __init__(self):
        self.headers = {'Content-Type': 'application/octet-stream',
                        'Ocp-Apim-Subscription-Key': API_KEY}

    def detect_emotion(self, image=None):
        """
        A method that detects emotion using a given image or the default image
        """
        if image is None:
            image = open("default_image.jpg", "rb").read()

        response = requests.post(API_URL, headers=self.headers, data=image)
        data = json.loads(response.text)

        if data:
            try:
                scores = data[0]["faceAttributes"]["emotion"]
                emotion = max(scores, key=scores.get)
                return emotion
            except:
                pass

        return DEFAULT_EMOTION


class EmotionReaction:
    """
    A class that defines the emotion reactions of Vector
    """

    def __init__(self, robot):
        self.robot = robot

    def say(self, text, duration_scalar=1.0):
        """
        A method that makes Vector say a given text with optional duration scalar
        """
        duration_ms = int(duration_scalar * 200.0 * len(text))
        self.robot.behavior.say_text(text, duration_scalar=duration_scalar)
        return duration_ms

    def play_animation(self, anim_name, *, loops=1, use_lift_safe=True, ignore_lift_track=False):
        """
        A method that makes Vector play a given animation
        """
        anim = self.robot.anim.load_animation(anim_name)
        return self.robot.anim.play_animation(
            anim, loops=loops, use_lift_safe=use_lift_safe, ignore_lift_track=
