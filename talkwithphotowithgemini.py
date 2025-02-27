from google import genai
from google.genai.types import (
    Part,
)

import base64
import os

# Import the project ID, location and Model ID from the environment variables 
PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("LOCATION")
MODEL_ID = os.getenv("MODEL_ID")

# Create a client with the Vertex AI backend
client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)

def encode_image_to_base64(image_path):
    """
    Encode an image to a base64 string.

    Args:
        image_path (str): Path to the image file.

    Returns:
        str: Base64 encoded string of the image.
    """
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        print(f"Error: The file {image_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while encoding the image: {e}")
        return None

def get_gemini_response(base64_image):
    """
    Get a response from the Gemini model using AzureChatOpenAI.

    Args:
        messages (list): Message payload for AzureChatOpenAI.

    Returns:
        dict: Response from the Gemini model.
    """

    try:
        prompt = """
                You are an expert in Analyzing Images.
                Please extract all information from the provided image.

                Response Format: Simple Text, no markdown; no bullet points.
                
            """

        response = client.models.generate_content(
                model=MODEL_ID,
                contents=[
                    Part.from_bytes(
                        data=image_base64, mime_type="image/jpeg"
                    ),
                    f"{prompt}",
                ],
            )
        return response.text
    except Exception as e:
        print(f"An error occurred while getting the GPT-4o response: {e}")
        return None

def main():
    image_path = "download.jpg"
    base64_image = encode_image_to_base64(image_path)
    if base64_image:
        response = get_gemini_response(base64_image)
        if response:
            print("Response received:", response)
        else:
            print("Failed to get a response from Gemini.")
    else:
        print("Failed to encode the image.")

if __name__ == "__main__":
    main()
