import os

import logging
from selenium import webdriver
from selenium.webdriver import Firefox

from linkedin import LinkedIn
from utils import Utils

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] - [%(levelname)s] -  %(name)s.%(funcName)s(%(lineno)d) - "%(message)s"',
                    filename='logs/out.log',
                    filemode='a',)


def get_linkedin_profile_image(web_driver: webdriver.Firefox):
    linkedin = LinkedIn(driver=web_driver)

    linkedin.login(email=os.getenv('LINKEDIN_EMAIL'), password=os.getenv('LINKEDIN_PASSWORD'))

    username = linkedin.get_username()
    profile_img_link = linkedin.get_profile_image()

    return username, profile_img_link


if __name__ == "__main__":
    driver = Firefox()
    image_name, image_link = get_linkedin_profile_image(web_driver=driver)
    Utils.save_image(image_name=image_name, image_url=image_link)
