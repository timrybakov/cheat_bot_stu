from io import BytesIO
import requests
from PIL import Image

from cheat_bot.di import di_container


class Conversion:
    url_info = f'https://api.telegram.org/bot{di_container.settings.auth_token}/getFile?file_id='
    url = f'https://api.telegram.org/file/bot{di_container.settings.auth_token}/'

    @classmethod
    def get_images_binary(cls, file_id: str) -> bytes:
        response = requests.get(cls.url_info + file_id)
        img_path = response.json().get('result').get('file_path')
        return requests.get(cls.url + img_path).content

    @classmethod
    def convert_bin_to_jpg(cls, file_binary: bytes) -> bytes:
        im = Image.open(BytesIO(file_binary))
        rgb_im = im.convert('RGB')
        img_byte_array = BytesIO()
        rgb_im.save(img_byte_array, format='JPEG')
        binary_data = img_byte_array.getvalue()
        return binary_data
