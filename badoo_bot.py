import time
from random import randint
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import secret_keys
import datetime


class WebDriver:
    def __init__(self, _driver: webdriver):
        self.driver: webdriver = _driver

    def __enter__(self) -> webdriver:
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()


def do_that_func_only_if_css_element_was_found(orig_func):
    def modified_func_with(**kwargs):
        try:
            orig_func(**kwargs)
        except NoSuchElementException:
            # print(f'Unable to locate element with css class:{kwargs.get("css_class_name", "")} ')
            pass
        except Exception as ex:
            return type(ex).__name__
    return modified_func_with


@do_that_func_only_if_css_element_was_found
def send_to_field_with(css_class_name: str, keys: str, _driver: webdriver):
    login_field = _driver.find_element_by_css_selector(f'.{css_class_name}')
    login_field.clear()
    login_field.send_keys(keys)


@do_that_func_only_if_css_element_was_found
def click_btn_with(css_class: str, _driver: webdriver, need_to_login: bool = False):
    btn_login = _driver.find_element_by_css_selector(f'.{css_class}')
    btn_login.click()
    if need_to_login:
        login(_driver)


@do_that_func_only_if_css_element_was_found
def get_user_name(_driver: webdriver) -> str:
    return _driver.find_element_by_css_selector('.profile-header__name').text


def login(_driver: webdriver):
    send_to_field_with(css_class_name='js-signin-login', keys=secret_keys.badoo_email, _driver=_driver)
    send_to_field_with(css_class_name='js-signin-password', keys=secret_keys.badoo_pass, _driver=_driver)
    click_btn_with(css_class='sign-form__submit', _driver=_driver)
    time.sleep(2)
    driver.get('https://badoo.com/encounters')


with WebDriver(webdriver.Chrome('./chromedriver')) as driver:
    driver.get('https://badoo.com/ru/signin/?f=top')
    login(driver)
    unsuccessful_click_counter = 0
    i = 0
    old_user_or_error_name = ''
    while True:
        i += 1
        # deny blocking questions
        click_btn_with(css_class='js-chrome-pushes-deny', _driver=driver)
        click_btn_with(css_class='js-continue', _driver=driver)
        click_btn_with(css_class='js-ovl-close', _driver=driver)  # new match close
        click_btn_with(css_class='js-session-expire', _driver=driver, need_to_login=True)
        time.sleep(randint(1, 2))
        was_clicked = 'like'
        if randint(0, 1) == 1:
            click_btn_with(css_class='js-profile-header-vote-yes', _driver=driver)
        else:
            was_clicked = 'dislike'
            click_btn_with(css_class='js-profile-header-vote-no', _driver=driver)
        new_user_or_error_name = get_user_name()
        if new_user_or_error_name == old_user_or_error_name:
            unsuccessful_click_counter += 1
            if unsuccessful_click_counter >= 2:
                print(f"too many tries to click with no result, lets sleep to wait, user_or_error_name\
                 = {new_user_or_error_name}")
                time.sleep(60 * 60 * 1)
                unsuccessful_click_counter = 0
        else:
            unsuccessful_click_counter = 0
        old_user_or_error_name = new_user_or_error_name
        print(f'{i}.  {was_clicked}   --- {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        time.sleep(randint(1, 4))





# click_button(css_class_name='js-chrome-pushes-deny', with_driver=driver)
# time.sleep(randint(1, 3))
