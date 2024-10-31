from dataclasses import dataclass


@dataclass(eq=False)
class CaptchaException(Exception):
    email: str | None = None

    @property
    def message(self):
        return 'Captcha occurred :('


@dataclass(eq=False)
class LoginException(Exception):
    email: str | None = None

    @property
    def message(self):
        return f'An error occurred while logging in! ({self.email})'
