# from deepface import DeepFace
# import os

# EMPLOYEE_IMAGE_DIR = "data_pipeline/employee_images"

# def detect_emotion(image_path):
#     """
#     Detects emotion from an employee's face using DeepFace.
#     """
#     try:
#         analysis = DeepFace.analyze(image_path, actions=['emotion'])
#         return analysis[0]['dominant_emotion']
#     except Exception as e:
#         print(f"Error in emotion detection: {e}")
#         return "Unknown"

# def analyze_employee_images(employee_id):
#     """
#     Detects emotions for all available images of an employee.
#     """
#     emp_folder = os.path.join(EMPLOYEE_IMAGE_DIR, employee_id)

#     if not os.path.exists(emp_folder) or not os.path.isdir(emp_folder):
#         return {"error": f"No images found for employee {employee_id}"}

#     images = [os.path.join(emp_folder, img) for img in os.listdir(emp_folder) if img.endswith(('.png', '.jpg', '.jpeg'))]

#     if not images:
#         return {"error": f"No valid image files found for {employee_id}"}

#     emotions = {}
#     for img_path in images:
#         img_name = os.path.basename(img_path)
#         emotions[img_name] = detect_emotion(img_path)

#     return emotions

import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image as keras_image
# from tensorflow.keras.utils import load_img, img_to_array
import os

# Load the fine-tuned model
MODEL_PATH = "/Users/kdn_aigayatrikadam/Documents/Projects/Project-4/ESG Wellbeing Agent/backend/model/microexpression_model_finetuned_4.keras"
model = tf.keras.models.load_model(MODEL_PATH)
print("loaded face emotions model sucessfully✅")

# Class names (from your training dataset)
class_names = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']  # Example, replace with your actual list

EMPLOYEE_IMAGE_DIR = "data_pipeline/employee_images"

def preprocess_image(img_path):
    """
    Preprocess image to match EfficientNet input requirements.
    """
    img = keras_image.load_img(img_path, target_size=(224, 224))
    img_array = keras_image.img_to_array(img)
    img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)
    return np.expand_dims(img_array, axis=0)  # Model expects batch dimension

def detect_emotion(img_path,model=model):
    """
    Detects emotion using the fine-tuned EfficientNet model.
    """
    try:
        img_preprocessed = preprocess_image(img_path)
        predictions = model.predict(img_preprocessed)
        predicted_class = class_names[np.argmax(predictions)]
        return predicted_class
    except Exception as e:
        print(f"Error in emotion detection: {e}")
        return "Unknown"

def analyze_employee_images(employee_id):
    """
    Detects emotions for all available images of an employee.
    """
    emp_folder = os.path.join(EMPLOYEE_IMAGE_DIR, employee_id)

    if not os.path.exists(emp_folder) or not os.path.isdir(emp_folder):
        return {"error": f"No images found for employee {employee_id}"}

    images = [os.path.join(emp_folder, img) for img in os.listdir(emp_folder) if img.endswith(('.png', '.jpg', '.jpeg'))]

    if not images:
        return {"error": f"No valid image files found for {employee_id}"}

    emotions = {}
    for img_path in images:
        img_name = os.path.basename(img_path)
        emotions[img_name] = detect_emotion(img_path,model)

    return emotions
