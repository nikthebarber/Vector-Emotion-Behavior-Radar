import numpy as np
import tensorflow as tf
from tensorflow import keras
from reaction_detector import ReactionDetector

class EmotionEngine:
    def __init__(self, model_path, reaction_detector):
        self.model = keras.models.load_model(model_path)
        self.reaction_detector = reaction_detector
        
    def predict(self, image):
        reaction = self.reaction_detector.predict(image)
        if reaction != 'neutral':
            return 'angry'
        else:
            image = tf.image.resize(image, (48, 48))
            image = np.array(image)
            image = np.expand_dims(image, axis=0)
            result = self.model.predict(image)[0]
            emotion_dict = {
                0: 'angry',
                1: 'disgust',
                2: 'fear',
                3: 'happy',
                4: 'neutral',
                5: 'sad',
                6: 'surprise'
            }
            return emotion_dict[np.argmax(result)]
