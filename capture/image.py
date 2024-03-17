from hikvisionapi import Client

cam = Client('http://192.168.40.218', 'admin', 'metro@123')


def save_image(transcation_id):
    response = cam.Streaming.channels[102].picture(method='get', type='opaque_data')
    with open(f'capture/images/{transcation_id}.jpg', 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
