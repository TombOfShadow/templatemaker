
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import requests
from io import BytesIO
from services.character_extractor import extract_character

WIDTH = 1280
HEIGHT = 720

def gradient_overlay(width, height):
    base = Image.new('RGBA', (width, height), (0,0,0,0))
    draw = ImageDraw.Draw(base)
    for i in range(height):
        alpha = int(180 * (i / height))
        draw.line((0, i, width, i), fill=(0, 0, 0, alpha))
    return base

def glass_panel(image, box):
    panel = Image.new("RGBA", (box[2]-box[0], box[3]-box[1]), (255,255,255,60))
    blurred = image.crop(box).filter(ImageFilter.GaussianBlur(15))
    panel = Image.alpha_composite(blurred.convert("RGBA"), panel)
    image.paste(panel, box)

def generate_image(data):

    response = requests.get(data["poster"])
    bg = Image.open(BytesIO(response.content)).resize((WIDTH, HEIGHT)).convert("RGBA")

    bg = Image.alpha_composite(bg, gradient_overlay(WIDTH, HEIGHT))

    draw = ImageDraw.Draw(bg)

    font_big = ImageFont.load_default()
    font_small = ImageFont.load_default()

    # Title
    draw.text((100, 80), data["title"].upper(), font=font_big, fill="white")

    # Glass info panel
    info_box = (80, 160, 700, 380)
    glass_panel(bg, info_box)

    y = 180
    draw.text((100, y), f"RATING • {data['rating']}", font=font_small, fill="white")
    y += 40
    draw.text((100, y), f"STATUS • {data.get('status','N/A')}", font=font_small, fill="white")

    # Genres
    y = 250
    for genre in data["genres"][:5]:
        draw.text((100, y), genre.upper(), font=font_small, fill="white")
        y += 30

    # Character Cutout
    character = extract_character(data["poster"])
    character = character.resize((500, 650))
    bg.paste(character, (750, 40), character)

    # Branding
    draw.text((950, 40), data.get("logo", "ANIME STARDUST"), font=font_small, fill=(180,100,255))
    draw.text((900, 660), data.get("signature", "Sanctuary Stardust"), font=font_small, fill=(255,215,0))

    path = f"{data['title'].replace(' ','_')}.png"
    bg.save(path)

    return path
