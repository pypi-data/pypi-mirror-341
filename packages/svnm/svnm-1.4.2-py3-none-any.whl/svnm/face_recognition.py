import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import os
import tempfile
import requests
from deepface import DeepFace
from sklearn.metrics.pairwise import cosine_similarity


class FaceRecognizer:
    def __init__(self, models=None):
        if models is None:
            models =  ["Facenet", "OpenFace"]
        self.models = models
        self.trained_df = None

    def detect_face(self, image_path, show=True):
        img = cv2.imread(image_path)
        if img is None:
            print(f"Could not load image: {image_path}")
            return None, None

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) == 0:
            print(f"No face detected in {image_path}")
            return None, img

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if show:
            plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            plt.axis("off")
            plt.title(f"Detected Face in {image_path}")
            plt.show()

        return faces, img

    def get_combined_embedding(self, image_path):
        embeddings = []

        for model in self.models:
            try:
                result = DeepFace.represent(img_path=image_path, model_name=model, enforce_detection=False)
                embedding = result[0]["embedding"]  # Get the embedding directly
                embeddings.append(embedding)
            except Exception as e:
                print(f"Error extracting from {model}: {e}")

        if len(embeddings) == 0:
            return None

        # Resize embeddings to the same length
        max_size = max(len(e) for e in embeddings)

        def resize_embedding(embedding, target_size):
            if len(embedding) < target_size:
                return np.pad(embedding, (0, target_size - len(embedding)), mode='constant')
            else:
                return embedding[:target_size]

        embeddings = np.array([resize_embedding(e, max_size) for e in embeddings])
        avg_embedding = np.mean(embeddings, axis=0)
        concat_embedding = np.concatenate(embeddings, axis=0)
        std_embedding = np.std(embeddings, axis=0)

        return {
            "avg": avg_embedding,
            "concat": concat_embedding,
            "std": std_embedding
        }

    def compare_embeddings(self, embedding1, embedding2):
        results = {}
        for method in ["avg", "concat", "std"]:
            if len(embedding1[method]) == len(embedding2[method]):
                similarity = cosine_similarity([embedding1[method]], [embedding2[method]])[0][0]
                results[method] = similarity
            else:
                results[method] = None
        return results

    def train(self, df, save=False, json_path="trained_data.json"):
        """
        df: DataFrame with 'path' and 'label' columns
        save: If True, saves result to JSON
        """
        data = []
        for _, row in df.iterrows():
            embedding_data = self.get_combined_embedding(row["path"])
            if embedding_data is not None:
                data.append({
                    "embedding": embedding_data["concat"].tolist(),  # store as list for JSON compatibility
                    "label": row["label"]
                })
            else:
                print(f"Skipping {row['path']} due to missing embedding.")

        self.trained_df = pd.DataFrame(data)

        if save:
            with open(json_path, "w") as f:
                json.dump(data, f, indent=2)
            print(f"Training data saved to {json_path}")
        print("Training Completed")

    def find_best_match(self, image, source_type=None):
        """
        Find the best matching label for the given image using the 'concat' embedding.

        Parameters:
            image (str): Image path or URL.
            source_type (str): 'url' or 'path'. If None, defaults to 'path'. 

        Returns:
            tuple: (predicted_label, similarity_score)
        """
        if self.trained_df is None:
            raise ValueError("No training data found. Please call `train()` first.")

        # Determine source type
        source_type = source_type or "path"

        if source_type == "url":
            # Download the image to a temporary file
            try:
                response = requests.get(image)
                response.raise_for_status()
            except Exception as e:
                raise ValueError(f"Error fetching image from URL: {e}")

            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                tmp_file.write(response.content)
                temp_image_path = tmp_file.name
            image_path_to_use = temp_image_path
        else:
            image_path_to_use = image

        # Get embedding
        test_embedding = self.get_combined_embedding(image_path=image_path_to_use)

        # Clean up temp file if used
        if source_type == "url" and os.path.exists(image_path_to_use):
            os.remove(image_path_to_use)

        if test_embedding is None or "concat" not in test_embedding:
            raise ValueError("Failed to obtain a valid 'concat' embedding.")

        test_vec = test_embedding["concat"].reshape(1, -1)
        db_embeddings = np.vstack(self.trained_df["embedding"].apply(np.array))
        similarities = cosine_similarity(db_embeddings, test_vec)

        index = np.argmax(similarities)
        label = self.trained_df["label"].iloc[index]
        score = similarities[index][0]

        return label, score
