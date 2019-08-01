import csv
import time
import datetime
import os
from random import randint
from pygame import mixer
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException


class WebDriver:
    def __init__(self, _driver: webdriver, logs_sub_dir: str):
        self.driver: webdriver = _driver
        self.driver.girls_set = set()
        self.driver.stack_of_errors = []
        self.logs_sub_dir = logs_sub_dir

    def __enter__(self) -> webdriver:
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            current_dir = os.path.dirname(os.path.realpath(__file__))
            log_file_name = "log_" + str(datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) + ".csv"
            with open(os.path.join(current_dir, LOGS_DIR, self.logs_sub_dir, log_file_name), 'w',
                      newline='') as csv_file:
                # log_writer = csv.writer(csv_file, delimiter=' ',
                #                         quotechar='|', quoting=csv.QUOTE_MINIMAL)
                log_writer = csv.writer(csv_file)
                for tuple1 in self.driver.girls_set:
                    log_writer.writerow(list(tuple1))

        finally:
            print('RESULTS ===============================')
            _ = {print(x) for x in self.driver.girls_set}
            self.driver.close()


def do_that_func_only_if_css_element_was_found(orig_func):
    def modified_func_with(**kwargs):
        try:
            return orig_func(**kwargs)
        except NoSuchElementException:
            # print(f'Unable to locate element with css class:{kwargs.get("css_sel_or_xpath", "")} ')
            kwargs['_driver'].stack_of_errors.insert(0, NoSuchElementException)
            pass
        except ElementClickInterceptedException:
            # print(f' ElementClickInterceptedException  with css class:{kwargs.get("css_sel_or_xpath", "")} ')
            kwargs['_driver'].stack_of_errors.insert(0, ElementClickInterceptedException)

            pass
        except Exception as ex:
            err_name: str = type(ex).__name__
            kwargs['_driver'].stack_of_errors.insert(0, err_name)
            print(f' css class {kwargs.get("css_sel_or_xpath", "")} error = {err_name}')
            # time.sleep(60 * 60 * 24)  # strange error lets keep browser open
            return err_name

    return modified_func_with


@do_that_func_only_if_css_element_was_found
def send_to_field_with(css_sel_or_xpath: str, keys: str, _driver: webdriver):
    login_field = _driver.find_element_by_css_selector(f'{css_sel_or_xpath}')
    login_field.clear()
    login_field.send_keys(keys)
    return login_field


@do_that_func_only_if_css_element_was_found
def click_btn_with(css_sel_or_xpath: str, _driver: webdriver, login_func=None, use_xpath: bool = False):
    btn_login = _driver.find_element_by_xpath(css_sel_or_xpath) if use_xpath else \
        _driver.find_element_by_css_selector(f'{css_sel_or_xpath}')
    btn_login.click()
    time.sleep(random_float_number(1, 2))
    if login_func is not None:
        login_func(_driver)
    return btn_login


def set_scale(_driver: webdriver):
    _driver.execute_script("document.body.style.transform='scale(1.0)'")


def random_float_number(a: int, b: int):
    return randint(a * 10, b * 10) / 10.0


@do_that_func_only_if_css_element_was_found
def return__element_by_xpath(xpath: str, _driver: webdriver):
    return _driver.find_element_by_xpath(xpath)


def ask_question_with_sound(question: str, sound_file: str) -> str:
    mixer.init()
    mixer.music.load(f"{sound_file}.mp3")
    mixer.music.play()
    _answer = input(question).strip()
    mixer.music.stop()
    return _answer


LOGS_DIR = 'logs'
