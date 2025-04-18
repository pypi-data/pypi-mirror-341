import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img,img_to_array
import cv2
# Define a function for loading and preprocessing
def load_and_preprocess_image(path):
    image = load_img(path, target_size=(224, 224))
    image_array = img_to_array(image)
    return image_array

def load_and_preprocess_image_yolo(path):
    # Step 1: Load the image in BGR format
    image = cv2.imread(path)
    if image is None:
        raise FileNotFoundError(f"Image not found at path: {path}")
    # Step 2: Convert the image from BGR to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

