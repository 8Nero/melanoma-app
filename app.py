import os
import io
import torch
from urllib.request import urlopen
from PIL import Image
from torch import argmax
from torchvision import models
import torchvision.transforms as transforms
from flask import Flask, request, render_template

# Load a pre-trainied DenseNet model from torchvision.models
model = models.densenet121(weights=models.DenseNet121_Weights.DEFAULT)
model.eval()

# Load the class labels from a file
class_labels_url = (
    "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
)
class_labels = urlopen(class_labels_url).read().decode("utf-8").split("\n")

# Define the transofrmation of the input image
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def predict(model, transform, image, class_labels):
  # Transform the image and convert it to a tensor
  image_tensor = transform(image).unsqueeze(0)

  # Pass the image through the model
  with torch.no_grad():
      output = model(image_tensor)

  # Select the class with the highest probability
  class_id = argmax(output).item()
  class_name = class_labels[class_id]
  return class_name


app = Flask(__name__)

@app.route("/")
def home():
  return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict_api():
  # Fetch the image from the request and convert it
  image_file = request.files["file"]
  image_bytes = image_file.read()
  image = Image.open(io.BytesIO(image_bytes))

  # Predict the class from the image
  class_name = predict(model, transform, image, class_labels)

  # Write result as JSON
  return class_name


# Run the app
if __name__ == "__main__":
  app.run(debug=False, threaded=True, port=os.getenv("PORT", 5000))