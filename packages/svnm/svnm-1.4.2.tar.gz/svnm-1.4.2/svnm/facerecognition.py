import os
import cv2
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from svnm.facedetection import FaceDetection
from keras_facenet import FaceNet

class FaceRecognition:
    def __init__(self):
        self.facedetector = FaceDetection()  # Face detection model
        self.embeddingmodel = FaceNet()  # Face embedding model
        self.data = {"embeddings": [], "labels": []}  # Store training data embeddings and labels

    def train(self, trainset):
        """
        Train the model using the given training dataset.

        Args:
            trainset (list): List of training image data with attributes `imagepath` and `label`.
        """
        for index, rawimagedata in enumerate(trainset):
            if not os.path.exists(rawimagedata["imagepath"]):
                print(f"The image path {rawimagedata['imagepath']} does not exist.")
                continue  # Skip if image file doesn't exist

            # Detect faces in the image
            result = self.facedetector.predict(rawimagedata["imagepath"])
            faces = []
            if len(result)==0:
                print("no face found")
                continue
            # Extract face regions from the image
            for imagedata in result[0]:
                x1, y1, x2, y2 = map(int, imagedata['bbox'])
                image = cv2.imread(rawimagedata["imagepath"])
                if image is None:
                    print(f"Failed to load image: {rawimagedata['imagepath']}")
                    continue
                face = image[y1:y2, x1:x2]
                if face.dtype != np.uint8:
                    face = np.clip(face, 0, 255).astype(np.uint8)
                face=cv2.resize(face,(160,160))
                faces.append(face)

            if not faces:  # Skip if no faces are detected
                print(f"No faces detected in image: {rawimagedata['imagepath']}")
                continue

            # Compute embeddings for the detected faces
            embeddings = self.embeddingmodel.embeddings(faces)

            # Append embeddings and labels to the training data
            self.data["embeddings"].extend(embeddings)
            self.data["labels"].extend([rawimagedata["label"]] * len(embeddings))
            print("Training completed")

    def predict(self, image_path):
        """
        Predict the identity of a face in the given image.

        Args:
            image_path (str): Path to the image.

        Returns:
            list: A list of dictionaries containing predicted labels and confidence scores
                  for each detected face.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image path {image_path} does not exist.")

        # Detect faces in the image
        result = self.facedetector.predict(image_path)
        if not result:
            return [{"label": "No face detected", "conf": 0.0}]
        
        predictions = []
        for imagedata in result[0]:
            x1, y1, x2, y2 = map(int, imagedata['bbox'])
            image = cv2.imread(image_path)
            if image is None:
                print(f"Failed to load image: {image_path}")
                continue
            face = image[y1:y2, x1:x2]
            if face.dtype != np.uint8:
                face = np.clip(face, 0, 255).astype(np.uint8)
            face=cv2.resize(face,(160,160))
            # Compute embedding for the detected face
            face_embedding = self.embeddingmodel.embeddings([face])[0]

            # Calculate cosine similarity with training embeddings
            similarities = cosine_similarity([face_embedding], self.data["embeddings"])[0]

            # Find the best match
            best_match_idx = np.argmax(similarities)
            best_match_score = similarities[best_match_idx]

            # Threshold for face recognition
            threshold = 0.5  # Adjust based on application needs
            label = "Unknown"
            if best_match_score > threshold:
                label = self.data["labels"][best_match_idx]

            predictions.append({"label": label, "conf": best_match_score})

        return predictions

# Example Usage:
# face_recognition = FaceRecognition()
# face_recognition.train(train_dataset)  # Provide a dataset with image paths and labels
# prediction = face_recognition.predict("path_to_test_image.jpg")
# print(f"Predicted Label: {prediction}")
