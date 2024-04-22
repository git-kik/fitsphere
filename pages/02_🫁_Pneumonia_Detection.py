import os
from datetime import datetime
import sqlite3
import config as cfg
import streamlit as st
import torch
import torch.nn as nn
import torchvision
from config import doctor_search
from PIL import Image
from torchvision import transforms

# Connect to SQLite database
conn = sqlite3.connect('predictions.db')
c = conn.cursor()

# Create predictions table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS predictions
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              image_path TEXT,
              prediction INTEGER,
              confidence REAL)''')
conn.commit()

def preprocess_image(image):
    transform = transforms.Compose(
        [
            transforms.Resize(256),
            transforms.Grayscale(num_output_channels=1),
            transforms.ToTensor(),
        ]
    )
    image = Image.open(image)
    image = transform(image).float()
    return image

# Function to save uploaded image and return its filename
def save_uploaded_image(uploaded_image):
    # Create a directory to save uploaded images if it doesn't exist
    if not os.path.exists("uploaded_images"):
        os.makedirs("uploaded_images")

    # Generate a unique filename based on the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"uploaded_images/{timestamp}.png"

    # Save the uploaded image to the specified filename
    with open(filename, "wb") as f:
        f.write(uploaded_image.read())

    return filename

# Function to save prediction and confidence to the database
def save_prediction_to_database(image_filename, prediction, confidence):
    c.execute("INSERT INTO predictions (image_path, prediction, confidence) VALUES (?, ?, ?)", (image_filename, prediction.item(), confidence.item()))
    conn.commit()

class PneumoniaModel(nn.Module):
    def __init__(self):
        super().__init__()

        self.network = torchvision.models.resnet50(pretrained=False)
        self.network.conv1 = nn.Conv2d(
            1, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False
        )
        for param in self.network.fc.parameters():
            param.require_grad = False

        num_features = (
            self.network.fc.in_features
        )  # get number of features of last layer
        # -----------------------------------
        self.network.fc = nn.Sequential(
            nn.Linear(num_features, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 3),
        )

    def forward(self, x):
        return self.network(x)


def predict(image):
    with torch.no_grad():

        image = preprocess_image(image)
        image = image.unsqueeze(0)
        output = model(image)
        softmax = nn.Softmax(dim=1)
        output = softmax(output)
        pred = torch.argmax(output)
        print(output)
        confidence = torch.max(output).numpy()
        print(confidence * 100)
    return pred, confidence


def app():
    st.set_page_config(
        page_title="FitSphere - Pneumonia Detection",
        page_icon="🏥",
    )
    st.markdown(
        f"<h1 style='text-align: center; color: black;'>Pneumonia Detection</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h4 style='text-align: center; color: black;'>Upload a lung X-Ray image to know if the patient has bacterial or viral pneumonia</h4>",
        unsafe_allow_html=True,
    )
    st.markdown("#")
    uploaded_image = st.file_uploader("Upload an image to predict")

    if uploaded_image:
        st.image(uploaded_image)

        pred_button = st.button("Predict")
        if pred_button:
            # Save uploaded image
            image_filename = save_uploaded_image(uploaded_image)
            
            prediction, confidence = predict(uploaded_image)
            
            # Save prediction and confidence to database
            save_prediction_to_database(image_filename, prediction, confidence)
            
            print(prediction)
            if prediction == 0:
                st.subheader("The patient is not suffering from Pneumonia 😄🎉🎉")
                st.subheader(f"Confidence of model: {confidence*100:.2f}%")
                st.balloons()
            elif prediction == 1:
                st.subheader("The patient is suffering from Bacterial Pneumonia 😔")
                st.subheader(f"Confidence of model: {confidence*100:.2f}%")

            elif prediction == 2:
                st.subheader("The patient is suffering from Viral Pneumonia 😔")
                st.subheader(f"Confidence of model: {confidence*100:.2f}%")

            if prediction != 0:
                st.markdown("---")
                st.error(
                    "If you are a patient, consult with one of the following doctors immediately"
                )
                st.subheader("Specialists 👨‍⚕")
                st.write(
                    "Click on the specialist's name to find out the nearest specialist to you ..."
                )
                for s in ["Primary Care Doctor", "Lung Specialist"]:
                    doctor = f"- [{s}]({doctor_search(s)})"
                    st.markdown(doctor, unsafe_allow_html=True)
                st.markdown("---")


if __name__ == "__main__":
    model = PneumoniaModel()
    model.load_state_dict(torch.load(cfg.PNEUMONIA_MODEL, map_location="cpu"))
    model.eval()

    app()
