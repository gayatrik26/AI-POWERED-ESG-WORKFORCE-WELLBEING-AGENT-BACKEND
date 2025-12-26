import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

import librosa

# Load your saved model
model = load_model("/Users/kdn_aigayatrikadam/Documents/Projects/Project-4/ESG Wellbeing Agent/backend/model/audio_emotion_model_acc_60.h5")
# model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),loss='categorical_crossentropy',metrics=['accuracy'])
print("✅ Model loaded successfully!")

# Same emotion label mapping used during training
emotions = {0: 'angry', 1: 'sad', 2: 'happy', 3: 'fear', 4: 'disgust', 5: 'surprised', 6: 'neutral'}

def extract_features(file_path, target_duration=4, sr=16000, max_pad_len=200):
    """
    Extract features (MFCC, Chroma, Mel Spectrogram) from an audio file.
    - Trims audio longer than `target_duration` seconds.
    - Pads audio shorter than `target_duration` seconds.
    - Standardizes all extracted features to a fixed length.
    """
    try:
        audio, sample_rate = librosa.load(file_path, sr=sr)

        # Ensure audio length is within range (1-3 sec)
        audio_duration = librosa.get_duration(y=audio, sr=sample_rate)
        
        if audio_duration < 1.0:
            print(f"Skipping {file_path} (too short: {audio_duration:.2f} sec)")
            return None

        # Trim or pad audio to exactly `target_duration`
        target_samples = sr * target_duration  # Number of samples in 3 sec
        if len(audio) > target_samples:
            audio = audio[:target_samples]  # Trim
        else:
            audio = np.pad(audio, (0, max(0, target_samples - len(audio))), mode='constant')  # Pad

        # Extract features
        mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
        chroma = librosa.feature.chroma_stft(y=audio, sr=sample_rate)
        mel = librosa.feature.melspectrogram(y=audio, sr=sample_rate)

        # Ensure all features have a fixed size
        def fix_shape(feature):
            return np.pad(feature, ((0, 0), (0, max(0, max_pad_len - feature.shape[1]))), mode='constant')[:, :max_pad_len]

        mfccs, chroma, mel = map(fix_shape, [mfccs, chroma, mel])

        # Stack features
        feature_stack = np.vstack([mfccs, chroma, mel])

        return feature_stack

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None



def predict_emotion_from_audio(audio_path, model=model):
    # Extract features
    feature = extract_features(audio_path)
    
    if feature is None:
        print("⚠️ Feature extraction failed.")
        return None

    # Reshape feature (match model input)
    feature = np.expand_dims(feature, axis=0)  # (1, height, width)
    feature = feature[..., np.newaxis]  # Add channel dim -> (1, height, width, 1)

    # Predict
    prediction = model.predict(feature)
    predicted_index = np.argmax(prediction)
    predicted_emotion = emotions[predicted_index]

    print(f"🎙️ Predicted Emotion for {audio_path}: {predicted_emotion} ({np.round(prediction[0][predicted_index]*100, 2)}%)")
    return predicted_emotion
