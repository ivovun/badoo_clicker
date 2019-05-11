import time
from random import randint
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import secret_keys
import datetime


class WebDriver():
    def __init__(self, driver):
        self.driver: webdriver = driver

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
        except:
            pass
    return modified_func_with


@do_that_func_only_if_css_element_was_found
def send_to(css_class_name: str, with_driver: webdriver, keys: str = ''):
    login_field = with_driver.find_element_by_css_selector(f'.{css_class_name}')
    login_field.clear()
    login_field.send_keys(keys)


@do_that_func_only_if_css_element_was_found
def click_button(css_class_name: str, with_driver: webdriver, re_login: bool = False):
    btn_login = with_driver.find_element_by_css_selector(f'.{css_class_name}')
    btn_login.click()
    if re_login:
        login(with_driver)


def login(_driver:webdriver):
    send_to(css_class_name='js-signin-login', with_driver=_driver, keys=secret_keys.badoo_email)
    send_to(css_class_name='js-signin-password', with_driver=_driver, keys=secret_keys.badoo_pass)
    click_button(css_class_name='sign-form__submit', with_driver=_driver)
    time.sleep(2)
    driver.get('https://badoo.com/encounters')


with WebDriver(webdriver.Chrome('./chromedriver')) as driver:
    driver.get('https://badoo.com/ru/signin/?f=top')
    login(driver)
    time.sleep(2)
    i = 0
    while True:
        i += 1
        # deny blocking questions
        click_button(css_class_name='js-chrome-pushes-deny', with_driver=driver)
        click_button(css_class_name='js-continue', with_driver=driver)
        click_button(css_class_name='js-session-expire', with_driver=driver, re_login=True)
        time.sleep(randint(1, 2))
        was_clicked = 'like'
        if randint(0, 1) == 1:
            click_button(css_class_name='js-profile-header-vote-yes', with_driver=driver)
        else:
            was_clicked = 'dislike'
            click_button(css_class_name='js-profile-header-vote-no', with_driver=driver)
        print(f'{i}.  {was_clicked}   --- {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        time.sleep(randint(1, 4))





# click_button(css_class_name='js-chrome-pushes-deny', with_driver=driver)
# time.sleep(randint(1, 3))
