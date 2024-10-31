from enum import StrEnum


class CLASS(StrEnum):
    LOGIN_FORM = "login__form"
    FEED_MENU = "global-nav__primary-link"
    PROFILE_PHOTO_EDIT_BUTTON = "profile-photo-edit__edit-btn"


class CSS(StrEnum):
    PROFILE_CARD_PICTURE = ".profile-card-profile-picture"
    PROFILE_CARD_NAME = ".profile-card-name"
    PROFILE_PHOTO = ".imgedit-profile-photo-frame-viewer__target-image"


class XPATH(StrEnum):
    SIGH_IN_BUTTON = "//a[@data-tracking-control-name='guest_homepage-basic_nav-header-signin']"

