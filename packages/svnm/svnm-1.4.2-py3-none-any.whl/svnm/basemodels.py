from tensorflow.keras.models import load_model
import numpy as np
import os
from svnm.preprocessing import load_and_preprocess_image
from svnm.config import modelinfo
from svnm.utils import download_model
from ultralytics import YOLO
import cv2
import tensorflow as tf
from svnm.layers import *
class ImageClassificationbaseModel:
    
    def __init__(self,modelname):
        """
        Initialize the model by downloading and loading the pre-trained model.
        """
        try:
            filepath = modelinfo[modelname]["filename"]
            repoid = modelinfo[modelname]["repoid"]
            modelpath = download_model(repoid, filepath)
            self.model = load_model(modelpath)
            self.metrics = modelinfo[modelname]["metrics"]
            self.classes = modelinfo[modelname]["classes"]
        except KeyError as e:
            raise KeyError(f"Missing key in modelinfo configuration: {e}")
        except Exception as e:
            raise RuntimeError(f"Error initializing the model: {e}")

    def predict(self, filepath,conf=0.8):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Image file not found: {filepath}")
        
        try:
            image =load_and_preprocess_image(filepath)
            image = tf.expand_dims(image, axis=0)
            results=self.model.predict(image)
            id = np.argmax(results[0])
            conf = results[0][id]
            label = self.classes.get(id, "Unknown")
            return label, conf
        except Exception as e:
            raise ValueError(f"Error during prediction: {e}")

    def predict_batch(self, filepaths):
        for filepath in filepaths:
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"Image file not found: {filepath}")

        try:
            images = [load_and_preprocess_image(fp) for fp in filepaths]
            images = np.stack(images)
            outputs = self.model.predict(images)

            predictions = []
            for output in outputs:
                id = np.argmax(output)
                conf = output[id]
                label = self.classes.get(id, "Unknown")
                predictions.append((label, conf))

            return predictions
        except Exception as e:
            raise ValueError(f"Error during batch prediction: {e}")
    def visualize_prediction(self, filepath):
        try:
            import matplotlib.pyplot as plt
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"Image file not found: {filepath}")

            label, conf = self.predict(filepath)
            image = tf.keras.preprocessing.image.load_img(filepath)
            plt.imshow(image)
            plt.title(f"Prediction: {label} ({conf:.2f})")
            plt.axis('off')
            plt.show()
        except Exception as e:
            raise RuntimeError(f"Error visualizing prediction: {e}")

class ImageDetectionyolobaseModel:
    def __init__(self, modelname, save=False, save_dir="predictions"):
        """
        Initialize the model by downloading and loading the pre-trained model.
        
        Args:
        - modelname: Name of the model.
        - save: Boolean flag indicating whether to save the predicted images.
        - save_dir: Directory where the predicted images will be saved.
        """
        try:
            filepath = modelinfo[modelname]["filename"]
            repoid = modelinfo[modelname]["repoid"]
            modelpath = download_model(repoid, filepath)
            self.model = YOLO(modelpath)
            self.metrics = modelinfo[modelname]["metrics"]
            self.classes=modelinfo[modelname]["classes"]
            self.save = save
            self.save_dir = save_dir
            if self.save and not os.path.exists(save_dir):
                os.makedirs(save_dir)
        except KeyError as e:
            raise KeyError(f"Missing key in modelinfo configuration: {e}")
        except Exception as e:
            raise RuntimeError(f"Error initializing the model: {e}")

    def _parse_predictions(self, results):
        # Function to parse YOLO model results into human-readable format
        predictions = []
        for result in results:
            boxes = result.boxes.xyxy  # Bounding boxes
            scores = result.boxes.conf  # Confidence scores
            classes = result.boxes.cls  # Class IDs

            output = [
                {
                    "label": self.classes.get(int(cls), "Unknown"),
                    "confidence": float(score),
                    "bbox": box.tolist()
                }
                for cls, score, box in zip(classes, scores, boxes)
            ]
            predictions.append(output)
        return predictions

    def _save_image(self, image, filepath, predictions):
        """
        Saves the image with predicted bounding boxes drawn.
        
        Args:
        - image: The image on which predictions are drawn.
        - filepath: The original image path (used to name the saved image).
        - predictions: The parsed prediction results.
        """
        for prediction in predictions:
            for obj in prediction:
                box = obj["bbox"]
                x1, y1, x2, y2 = map(int, box)
                label = obj["label"]
                confidence = obj["confidence"]
                
                # Draw bounding box and label
                color = (0, 255, 0)  # Green color for bounding box
                thickness = 2
                cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)
                cv2.putText(image, f"{label} {confidence:.2f}", 
                            (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 
                            0.8, color, 2)
        
        # Save the image with predictions
        filename = os.path.basename(filepath)
        save_path = os.path.join(self.save_dir, f"pred_{filename}")
        cv2.imwrite(save_path, image)

    def predict(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Image file not found: {filepath}")

        try:
            # Perform single image prediction using the file path
            result = self.model.predict(filepath)[0]  # Get the first result for a single image
            predictions = self._parse_predictions([result])  # Parse results
            
            if self.save:
                # Read the image to draw bounding boxes and save
                image = cv2.imread(filepath)
                self._save_image(image, filepath, predictions)
            
            return predictions

        except Exception as e:
            raise ValueError(f"Error during single prediction: {e}")

    def predict_batch(self, filepaths):
        # Ensure all file paths exist
        for filepath in filepaths:
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"Image file not found: {filepath}")

        try:
            # Perform batch prediction directly using the file paths
            results = self.model.predict(filepaths)  # Batch prediction
            predictions = self._parse_predictions(results)  # Parse results
            
            if self.save:
                # Save predicted images for the batch
                for filepath, result in zip(filepaths, predictions):
                    image = cv2.imread(filepath)
                    self._save_image(image, filepath, result)
            
            return predictions

        except Exception as e:
            raise ValueError(f"Error during batch prediction: {e}")
