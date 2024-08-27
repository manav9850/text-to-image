import streamlit as st
import requests
import io
from PIL import Image

# Hugging Face API URL and token
API_URL = "https://api-inference.huggingface.co/models/davisbro/half_illustration"
headers = {"Authorization": "Bearer "}

# Function to query the Hugging Face API
def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Check for HTTP errors
        return response.content
    except requests.exceptions.HTTPError as err:
        st.error(f"HTTP error occurred: {err}")
    except requests.exceptions.RequestException as err:
        st.error(f"Error occurred: {err}")
    return None

# Streamlit app
st.title("Text to Image Generation")

st.write("Generate an image based on the provided text description.")

# Input field for the text description
input_text = st.text_input("Enter a description:", "Astronaut riding a horse")

# Button to generate the image
if st.button("Generate Image"):
    if input_text:
        with st.spinner("Generating image..."):
            # Query the model
            image_bytes = query({"inputs": input_text})
            
            if image_bytes:
                try:
                    # Convert bytes to PIL Image
                    image = Image.open(io.BytesIO(image_bytes))
                    st.image(image, caption=input_text)
                except Exception as e:
                    st.error(f"Error displaying image: {e}")
            else:
                st.error("No image was returned.")
    else:
        st.write("Please enter a description.")

st.markdown("Enter a text description above and click 'Generate Image' to see the generated image based on your description.")
