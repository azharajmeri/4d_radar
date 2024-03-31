import os
import time
from datetime import datetime

from hikvisionapi import Client
from PIL import Image, ImageDraw, ImageFont

from radar.models import Display, Location


def delete_old_folders():
    location_obj = Location.objects.first()
    if location_obj:
        address = location_obj.address
    else:
        address = ""

    location_dir = f'capture/images/{address}'  # Path to the Location directory
    today = datetime.now()

    # Iterate over the directories in the Location directory
    for folder in os.listdir(location_dir):
        folder_path = os.path.join(location_dir, folder)
        if os.path.isdir(folder_path):
            # Extract the date from the folder name
            try:
                folder_date = datetime.strptime(folder, "%Y%m%d")
            except ValueError:
                # Skip if the folder name is not in the expected format
                continue

            # Calculate the age of the folder
            age = today - folder_date

            # Check if the folder is older than 5 days
            if age.days > 5:
                # Delete the folder and its contents
                try:
                    os.system(f"rm -rf {folder_path}")  # Remove folder and its contents (Unix-based systems)
                    # For Windows, you can use: os.system(f"rmdir /s /q {folder_path}")
                    print(f"Deleted folder: {folder_path}")
                except Exception as e:
                    print(f"Error deleting folder {folder_path}: {e}")


def create_folder_structure(instance):
    delete_old_folders()
    base_dir = 'capture/images'
    location_dir = os.path.join(base_dir, instance.address)
    today_date = datetime.now().strftime('%Y%m%d')
    date_dir = os.path.join(location_dir, today_date)

    # Creating base directory if it doesn't exist
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)

    # Creating location directory if it doesn't exist
    if not os.path.exists(location_dir):
        os.mkdir(location_dir)

    # Creating date directory if it doesn't exist
    if not os.path.exists(date_dir):
        os.mkdir(date_dir)

    # Creating lane directories
    for lane_id in range(1, 5):
        lane_dir = os.path.join(date_dir, f"Lane_{lane_id}")
        if not os.path.exists(lane_dir):
            os.mkdir(lane_dir)

    print("Folder structure created successfully.")


def add_text(image_path, s_id, speed, lane):

    image = Image.open(image_path)

    # Define the text to be added
    location_obj = Location.objects.first()
    if location_obj:
        address = location_obj.address
    else:
        address = ""
    text = f"id: {s_id}\nspeed: {speed}\nlane: {lane}\nlocation: {address}"

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
        cam = Client("http://"+display.camera_ip, display.camera_user, display.camera_pass)
        time.sleep(0.1)
        create_folder_structure(instance)
        today_date = datetime.now().strftime('%Y%m%d')
        response = cam.Streaming.channels[102].picture(method='get', type='opaque_data')
        image_path = f'capture/images/{instance.address}/{today_date}/{instance.lane_number}/{instance.transcation_id}.jpg'
        with open(image_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        instance.image = image_path
        instance.save()

        add_text(image_path, instance.id, instance.speed, instance.lane_number)
