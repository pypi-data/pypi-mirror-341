import os
import tensorflow as tf
from .model import galaxy_morph, preprocess_image
from . import bpt  # Import the BPT module

__version__ = "0.0.7"  # Updated version to 0.0.7

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow warnings
tf.get_logger().setLevel('ERROR')  # Suppress other TensorFlow logs

# Get the absolute model path inside the package
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.keras")
MODEL_PATH2 = os.path.join(os.path.dirname(__file__), "model2.keras")  # For second model

# Load the models globally
if os.path.exists(MODEL_PATH) and os.path.exists(MODEL_PATH2):
    model1 = tf.keras.models.load_model(MODEL_PATH)
    model2 = tf.keras.models.load_model(MODEL_PATH2)
else:
    raise FileNotFoundError(f"One or more model files not found at {MODEL_PATH} or {MODEL_PATH2}")

# Expose key functions, models, and modules
__all__ = ["galaxy_morph", "preprocess_image", "model1", "model2", "bpt"]
