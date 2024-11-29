import streamlit as st
import pytesseract
from PIL import Image, ImageDraw, ImageFont
import torch
from torchvision import models, transforms
import torch.nn as nn

# Specify the tesseract executable path if Tesseract is not in the PATH
# Adjust the path to where Tesseract is installed on your machine
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # For Windows users
# For Linux or macOS, you can skip this line if tesseract is in the PATH
# pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'  # For macOS and Linux users (if needed)

# Load your trained model (ResNet-101)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = models.resnet101(pretrained=False)
num_classes = 46  # Set to the number of classes in your dataset
model.fc = nn.Linear(model.fc.in_features, num_classes)

# Load the model weights
model.load_state_dict(torch.load('C:/Users/achar/OneDrive/Desktop/Hackathon/scan/devanagari_model.pth', map_location=device))
model = model.to(device)
model.eval()

# Define the image transformation pipeline
data_transforms = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Set up the Streamlit interface
st.title("Devanagari Handwritten Text Recognition")
st.write("Upload an image containing Devanagari text, and the system will extract and classify the text.")

# Image upload
uploaded_image = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_image is not None:
    # Open the image using PIL
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Step 1: Extract text using Tesseract OCR
    try:
        text = pytesseract.image_to_string(image, config='--psm 6', lang='nep')
        st.write("Extracted Text using Tesseract OCR:")
        st.write(text.strip())
    except pytesseract.TesseractError as e:
        st.error(f"Error in Tesseract OCR: {str(e)}")

    # Step 2: Use Tesseract to detect character bounding boxes
    boxes = pytesseract.image_to_boxes(image, config='--psm 6', lang='nep')

    # Step 3: Prepare for character segmentation and classification
    # Draw the bounding boxes on the image for visualization (optional)
    draw = ImageDraw.Draw(image)

    # Load a font that supports Devanagari characters (ensure the path is correct)
    try:
        # Replace this with the correct path to the NotoSansDevanagari font
        font = ImageFont.truetype("path_to_your_font_folder/NotoSansDevanagari-Regular.ttf", 32)
    except IOError:
        font = None  # Default font if the custom one isn't found

    for box in boxes.splitlines():
        b = box.split()
        char = b[0]
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        draw.rectangle([x, y, w, h], outline="red")

        # Draw the character using the custom font, if available
        if font:
            draw.text((x, y), char, font=font, fill="red")
        else:
            draw.text((x, y), char, fill="red")  # Fallback to default font

    # Display the image with bounding boxes (optional)
    st.image(image, caption="Image with Character Boundaries", use_column_width=True)

    # Step 4: Segment the image and classify each character using your ResNet model
    class_names = ["Class1", "Class2", "Class3", "Class4", "Class5", "Class6", "Class7", "Class8", "Class9", "Class10", 
                   "Class11", "Class12", "Class13", "Class14", "Class15", "Class16", "Class17", "Class18", "Class19", "Class20", 
                   "Class21", "Class22", "Class23", "Class24", "Class25", "Class26", "Class27", "Class28", "Class29", "Class30", 
                   "Class31", "Class32", "Class33", "Class34", "Class35", "Class36", "Class37", "Class38", "Class39", "Class40", 
                   "Class41", "Class42", "Class43", "Class44", "Class45", "Class46"]  # Replace with actual class names

    # Predict each character
    predicted_text = []
    for box in boxes.splitlines():
        b = box.split()
        char = b[0]
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        char_image = image.crop((x, y, w, h))  # Crop the image for the character
        
        # Transform the cropped image for ResNet input
        input_image = data_transforms(char_image).unsqueeze(0).to(device)
        
        # Predict the character class using the trained ResNet model
        with torch.no_grad():
            outputs = model(input_image)
            _, preds = torch.max(outputs, 1)
        
        predicted_class = preds.item()
        predicted_label = class_names[predicted_class]
        predicted_text.append(predicted_label)
    
    # Combine the predicted characters into a single string
    st.write("Predicted Text from Segmented Characters:")
    st.write("".join(predicted_text))
