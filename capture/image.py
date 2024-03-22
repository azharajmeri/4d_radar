import os
import time

from hikvisionapi import Client
from PIL import Image, ImageDraw, ImageFont

from radar.models import Display


def add_text(image_path, s_id, speed, lane):
    print("1")

    image = Image.open(image_path)
    print("2")

    # Define the text to be added
    text = f"id: {s_id}\nspeed: {speed}\nlane: {lane}"
    print("3")

    # Define font and size (increase the font size)
    font_size = 60
    font = ImageFont.truetype("arial.ttf", font_size)
    print("4")

    # Create a drawing context
    draw = ImageDraw.Draw(image)
    print("5")

    # Calculate text size
    text_width, text_height = draw.textsize(text, font=font)
    print("6")
    # Define the position to place the text (bottom left corner)
    margin = 10
    position = (margin, image.height - text_height - margin)
    print("7")
    # Add text to the image
    draw.text(position, text, fill="red", font=font)
    print("8")
    # Save the modified image with the same name
    filename, extension = os.path.splitext(image_path)
    print("9")
    new_image_path = filename + extension
    print("10")
    image.save(new_image_path)
    print("11")


def save_image(instance):
    print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
    display = Display.objects.get(lane_number=instance.lane_number)
    if display:
        cam = Client("http://"+display.camera_ip, display.camera_user, display.camera_pass)
        time.sleep(0.1)
        print("http://"+display.camera_ip, display.camera_user, display.camera_pass)
        response = cam.Streaming.channels[102].picture(method='get', type='opaque_data')
        with open(f'capture/images/{instance.id}.jpg', 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print("LLLLLLLLLLL")
        instance.image = f'{instance.id}.jpg'
        instance.save()
    print("KKKKKKKKKKKKKKKKKKKKKKKK")
    add_text(f'capture/images/{instance.id}.jpg', instance.id, instance.speed, instance.lane_number)
    print("////////////////////////////////////////////")