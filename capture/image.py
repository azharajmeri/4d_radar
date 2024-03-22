import os

from hikvisionapi import Client
from PIL import Image, ImageDraw, ImageFont

from radar.models import Display


def add_text(image_path):

    image = Image.open(image_path)

    # Define the text to be added
    text = "id: 1\nspeed: 82\nlane: 0"

    # Define font and size (increase the font size)
    font_size = 60
    font = ImageFont.truetype("arial.ttf", font_size)

    # Create a drawing context
    draw = ImageDraw.Draw(image)

    # Calculate text size
    text_width, text_height = draw.textsize(text, font=font)

    # Define the position to place the text (bottom left corner)
    margin = 10
    position = (margin, image.height - text_height - margin)

    # Add text to the image
    draw.text(position, text, fill="red", font=font)

    # Save the modified image with the same name
    filename, extension = os.path.splitext(image_path)
    new_image_path = filename + extension
    image.save(new_image_path)


def save_image(instance):
    display = Display.objects.get(lane_number=instance.lane_number)
    if display:
        cam = Client(display.camera_ip, display.camera_user, display.camera_pass)
        response = cam.Streaming.channels[102].picture(method='get', type='opaque_data')
        with open(f'images/{instance.created_at}_{instance.id}.jpg', 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        instance.image = f'{instance.created_at}_{instance.id}.jpg'
        instance.save()

    add_text(f'images/{instance.created_at}_{instance.id}.jpg')
