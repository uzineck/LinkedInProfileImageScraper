import requests
import logging

logger = logging.getLogger(__name__)


class Utils:
    @staticmethod
    def save_image(image_name: str, image_url: str):
        image_name = image_name.replace(" ", "_")
        img_data = requests.get(image_url).content
        logger.info("Opened image url")
        with open(f'images/{image_name}.jpg', 'wb') as file:
            file.write(img_data)
            logger.info("Downloaded image")
