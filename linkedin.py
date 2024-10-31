import getpass
import logging
from dataclasses import dataclass
import time
from enum import StrEnum

from selenium.common import TimeoutException, WebDriverException
from selenium.common.exceptions import NoSuchWindowException

from constants import CLASS, CSS, XPATH
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from exceptions import CaptchaException, LoginException

logger = logging.getLogger(__name__)


@dataclass
class LinkedIn:
    driver: Firefox

    def __wait_until_element_located(self, timeout: int, by: str, value: StrEnum) -> bool:
        try:
            WebDriverWait(self.driver, timeout=timeout).until(EC.presence_of_element_located((by, value)))
        except TimeoutException:
            return False

        return True

    def __check_current_url_pattern(self, required_url: str) -> bool:
        try:
            WebDriverWait(self.driver, timeout=10).until(EC.url_matches(required_url))
        except TimeoutException:
            return False

        return True

    def __check_current_url(self, required_url: str) -> bool:
        try:
            WebDriverWait(self.driver, timeout=2).until(EC.url_to_be(required_url))
        except TimeoutException:
            return False

        return True

    def login(
            self,
            email: str | None = None,
            password: str | None = None,
    ) -> None:
        if not email or not password:
            email, password = self.__prompt_email_password()
        self.driver.get("https://www.linkedin.com/")
        logger.info('Opened linkedin page')
        self.__go_from_main_page_to_login()
        self.__login(email=email, password=password)
        logger.info('Login successful')

    def get_profile_image(self) -> str:
        if not self.__check_current_url_pattern(required_url="https://www.linkedin.com/feed/"):
            self.driver.get("https://www.linkedin.com/feed")
        self.__wait_until_element_located(timeout=10, by=By.CLASS_NAME, value=CLASS.FEED_MENU)
        logger.info('Feed page opened')
        self.__go_from_feed_to_profile()
        profile_image_link = self.__get_profile_image()
        logger.info('Profile image link obtained')
        return profile_image_link

    def get_username(self):
        if not self.__check_current_url_pattern(required_url="https://www.linkedin.com/feed/"):
            self.driver.get("https://www.linkedin.com/feed")
        self.__wait_until_element_located(timeout=10, by=By.CSS_SELECTOR, value=CSS.PROFILE_CARD_NAME)
        element = self.driver.find_element(By.CSS_SELECTOR, CSS.PROFILE_CARD_NAME)
        return element.text

    @staticmethod
    def __prompt_email_password():
        email = input("Enter your email or number: ")
        password = getpass.getpass(prompt="Enter your password: ")
        return email, password

    def __login(self, email: str, password: str):
        self.__wait_until_element_located(timeout=10, by=By.CLASS_NAME, value=CLASS.LOGIN_FORM)
        logger.info('Login form loaded')

        email_input = self.driver.find_element(By.ID, "username")
        email_input.send_keys(email)
        logger.info('Email inserted')

        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys(password)
        logger.info('Password inserted')

        password_input.submit()
        logger.info('Form submitted')

        if self.__check_current_url_pattern(required_url="https://www.linkedin.com/checkpoint/challenge/"):
            logger.warning(f'Captcha occurred while login ({email})')
            print('Please solve captcha manually. You have 20 seconds')

        if not self.__wait_until_element_located(timeout=20, by=By.CLASS_NAME, value=CLASS.FEED_MENU):
            logger.error(f'Something went wrong while login ({email})')
            raise LoginException(email=email)

    def __get_profile_image(self) -> str:
        self.__wait_until_element_located(timeout=10, by=By.CLASS_NAME, value=CLASS.PROFILE_PHOTO_EDIT_BUTTON)
        self.driver.find_element(By.CLASS_NAME, CLASS.PROFILE_PHOTO_EDIT_BUTTON).click()
        logger.info('Profile image opened')

        self.__wait_until_element_located(timeout=10, by=By.CSS_SELECTOR, value=CSS.PROFILE_PHOTO)
        element = self.driver.find_element(By.CSS_SELECTOR, CSS.PROFILE_PHOTO)
        logger.info('Profile image loaded')

        return element.get_attribute("src")

    def __go_from_feed_to_profile(self):
        self.__wait_until_element_located(timeout=10, by=By.CSS_SELECTOR, value=CSS.PROFILE_CARD_PICTURE)

        element = self.driver.find_element(By.CSS_SELECTOR, CSS.PROFILE_CARD_PICTURE)
        element_parent = element.find_element(By.XPATH, '..')
        profile_path_link = element_parent.get_attribute("href")
        logger.info("Acquired profile link")
        self.driver.get(profile_path_link)
        logger.info("Opened profile page")

    def __go_from_main_page_to_login(self):
        self.__wait_until_element_located(timeout=10, by=By.XPATH, value=XPATH.SIGH_IN_BUTTON)

        element = self.driver.find_element(By.XPATH, XPATH.SIGH_IN_BUTTON)
        element.click()
        logger.info('Opened linkedin login page')
