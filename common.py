import sys

if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

if not sys.prefix.__contains__('/venv'):
    # print(sys.prefix)
    print('Please run from virtual environment !!!!')
    exit()

import csv
import time
import datetime
import os
from random import randint
from pygame import mixer
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
    ElementNotVisibleException,
    TimeoutException
)
import collections
import textwrap

MAXIMUM_QUANTITY_OF_ERRORS_OF_SAME_TYPE = 30


class TooMuchErrorsException(Exception):
    def __init__(self, some_exception: Exception):
        super().__init__()
        self.exception_instance = some_exception


class TooLongStayingOnTheSamePageException(Exception): pass


def add_error(self, current_error: Exception):
    self.errors_dict[current_error] += 1
    if self.errors_dict[current_error] >= MAXIMUM_QUANTITY_OF_ERRORS_OF_SAME_TYPE:
        self.errors_dict.clear()
        raise TooMuchErrorsException(current_error)


class WebDriver:
    def __init__(self, _driver: webdriver, logs_sub_dir: str):
        self.driver: webdriver = _driver
        self.driver.girls_set = set()
        self.driver.errors_dict = collections.defaultdict(int)
        self.driver.add_error = add_error
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
            _ = {print(format_text_for_terminal_print(f'{x[0]} + " " + {x[1]}')) for x in self.driver.girls_set}
            self.driver.close()


def do_that_func_only_if_css_element_was_found(orig_func):
    def modified_func_with(**kwargs):
        try:
            return orig_func(**kwargs)
        except NoSuchElementException:
            # print(f'Unable to locate element with css class:{kwargs.get("css_sel_or_xpath", "")} ')
            kwargs['_driver'].add_error(kwargs['_driver'], NoSuchElementException)
            pass
        except ElementClickInterceptedException:
            # print(f' ElementClickInterceptedException  with css class:{kwargs.get("css_sel_or_xpath", "")} ')
            kwargs['_driver'].add_error(kwargs['_driver'], ElementClickInterceptedException)
            pass
        except ElementNotVisibleException:
            # print(f' ElementNotVisibleException  with css class:{kwargs.get("css_sel_or_xpath", "")} ')
            # kwargs['_driver'].stack_of_errors.insert(0, ElementNotVisibleException)
            kwargs['_driver'].add_error(kwargs['_driver'], ElementNotVisibleException)
            pass

        except Exception as ex:
            err_name: str = type(ex).__name__
            print(f' css class {kwargs.get("css_sel_or_xpath", "")} error = {err_name}')
            # time.sleep(60 * 60 * 24)  # strange error lets keep browser open
            kwargs['_driver'].add_error(kwargs['_driver'], ex)
            return err_name

    return modified_func_with


@do_that_func_only_if_css_element_was_found
def send_to_field_with(css_sel_or_xpath: str, keys: str, _driver: webdriver):
    login_field = _driver.find_element_by_css_selector(f'{css_sel_or_xpath}')
    login_field.clear()
    login_field.send_keys(keys)
    return login_field


@do_that_func_only_if_css_element_was_found
def click_btn_with(css_sel_or_xpath: str, _driver: webdriver, login_func=None, use_xpath: bool = False,
                   clear_errors: bool = False):
    btn_login = _driver.find_element_by_xpath(css_sel_or_xpath) if use_xpath else \
        _driver.find_element_by_css_selector(f'{css_sel_or_xpath}')
    btn_login.click()
    if clear_errors:
        _driver.errors_dict.clear()
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


def return_first_existing_element_or_none_for(xpaths: tuple, _driver: webdriver):
    for xpath_variant in xpaths:
        elem = return__element_by_xpath(xpath=xpath_variant, _driver=_driver)
        if elem:
            return elem
    return None


def ask_question_with_sound(question: str = "Error has occurred!  press any key to stop music (and exit program): ",
                            sound_file: str = "Pink Floyd - Another Brick In The Wall (HQ)") -> str:
    mixer.init()
    mixer.music.load(f"{sound_file}.mp3")
    mixer.music.play()
    _answer = input(question).strip()
    mixer.music.stop()
    return _answer


def format_text_for_terminal_print(init_txt: str) -> str:
    dend_txt = textwrap.dedent(init_txt)
    result_txt = textwrap.fill(dend_txt, initial_indent='==>',
                               subsequent_indent=' ' * 8,
                               width=120)
    return result_txt


LOGS_DIR = 'logs'
