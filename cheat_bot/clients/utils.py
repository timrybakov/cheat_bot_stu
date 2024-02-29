from io import BytesIO

import requests

from PIL import Image

from cheat_bot.config.config import settings

URI_INFO = f'https://api.telegram.org/bot{settings.AUTH_TOKEN}/getFile?file_id='
URI = f'https://api.telegram.org/file/bot{settings.AUTH_TOKEN}/'


class AccessHelper:

    @staticmethod
    def get_images_binary(file_id: str) -> bytes:
        response = requests.get(URI_INFO + file_id)
        img_path = response.json().get('result').get('file_path')
        return requests.get(URI + img_path).content

    @staticmethod
    def convert_bin_to_jpg(file_binary: bytes) -> bytes:
        im = Image.open(BytesIO(file_binary))
        rgb_im = im.convert('RGB')
        img_byte_array = BytesIO()
        rgb_im.save(img_byte_array, format='JPEG')
        binary_data = img_byte_array.getvalue()
        return binary_data
