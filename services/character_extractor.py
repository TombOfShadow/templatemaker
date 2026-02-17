
from rembg import remove
from PIL import Image
import requests
from io import BytesIO

def extract_character(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    output = remove(img)
    return output
