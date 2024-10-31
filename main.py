import os

import logging
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

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


def get_random_firefox_agent() -> str:
    user_agent = UserAgent(browsers="firefox", os="windows", platforms="pc")
    return user_agent.random


if __name__ == "__main__":
    ua = get_random_firefox_agent()
    options = Options()
    options.add_argument(f'--user-agent={ua}')
    driver = Firefox(options=options)
    image_name, image_link = get_linkedin_profile_image(web_driver=driver)
    Utils.save_image(image_name=image_name, image_url=image_link)
