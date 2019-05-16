import time
from random import randint
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions
import secret_keys
import datetime
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pygame import mixer
from bs4 import BeautifulSoup


class WebDriver:
    def __init__(self, _driver: webdriver):
        self.driver: webdriver = _driver
        self.driver.girls_set = set()
        self.driver.stack_of_errors = []

    def __enter__(self) -> webdriver:
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            log_file_name = "log_" + str(datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) + ".csv"
            with open(log_file_name, 'w', newline='') as csv_file:
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
        global stack_of_errors
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
def click_btn_with(css_sel_or_xpath: str, _driver: webdriver, need_to_login: bool = False, use_xpath: bool = False):
    btn_login = _driver.find_element_by_xpath(css_sel_or_xpath) if use_xpath else \
        _driver.find_element_by_css_selector(f'{css_sel_or_xpath}')
    # btn_login = get_element_with_browser_delay(css_sel_or_xpath, _driver, By.XPATH if use_xpath else By.CSS_SELECTOR)
    btn_login.click()
    time.sleep(random_float_number(1, 2))
    if need_to_login:
        login(_driver)
    return btn_login


def get_element_with_browser_delay(css_sel_or_xpath: str, _driver: webdriver, element_located_by=By.CSS_SELECTOR):
    delay = 3  # seconds
    element = None
    try:
        # myElem = WebDriverWait(_driver, delay).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
        element = WebDriverWait(_driver, delay).until(EC.presence_of_element_located((element_located_by
                                                                                      , css_sel_or_xpath)))
        # print("Page is ready!")

    except TimeoutException:
        print("Loading took too much time!")
    finally:
        return element


@do_that_func_only_if_css_element_was_found
def get_user_name(_driver: webdriver) -> str:
    return _driver.find_element_by_css_selector('.profile-header__name').text


def login(_driver: webdriver):
    send_to_field_with(css_sel_or_xpath='.js-signin-login', keys=secret_keys.badoo_email, _driver=_driver)
    send_to_field_with(css_sel_or_xpath='.js-signin-password', keys=secret_keys.badoo_pass, _driver=_driver)
    click_btn_with(css_sel_or_xpath='//button[@class="btn btn--sm btn--block"]', _driver=_driver, need_to_login=False, use_xpath=True)
    time.sleep(random_float_number(2, 3))

    # if unsuccessful login, lets retry
    signin_link = return__element_by_xpath(xpath="//a[@class='link js-signin-link']", _driver=_driver)
    if signin_link is not None:
        signin_link.click()
        time.sleep(2)
        login(_driver)

    _driver.get('https://badoo.com/encounters')


def random_float_number(a: int, b: int):
    return randint(a * 10, b * 10) / 10.0


@do_that_func_only_if_css_element_was_found
def return__element_by_xpath(xpath: str, _driver: webdriver):
    # try:
    #     # return  get_element_with_browser_delay(css_sel_or_xpath, _driver
    #     #                                                    , By.XPATH if use_xpath else By.CSS_SELECTOR)
    return _driver.find_element_by_xpath(xpath)
    #
    # except NoSuchElementException:
    #     pass
    #     # print(f'Unable to locate element with css class:{kwargs.get("css_sel_or_xpath", "")} ')
    # return None


def extract_text(old_text: str):
    soup = BeautifulSoup(old_text, 'html.parser')

    tags = soup("div", {"class": "profile-section"})
    text1 = ''
    for tag in tags:
        text1 += tag.text.strip() + '\n'

    while True:
        new_r = text1.replace('  ', '\n')
        if new_r == text1:
            break
        else:
            text1 = new_r

    while True:
        new_r = text1.replace('\n\n', '\n')
        if new_r == text1:
            break
        else:
            text1 = new_r

    while True:
        new_r = text1.replace(':\n', ':')
        if new_r == text1:
            break
        else:
            text1 = new_r

    return text1


def main_circle():

    with WebDriver(webdriver.Chrome('./chromedriver')) as driver:
        driver.get('https://badoo.com/ru/signin/?f=top')
        login(driver)
        # time.sleep(100000)
        driver.execute_script("document.body.style.transform='scale(0.5)'")
        time.sleep(3)
        i = 0
        max_number_without_appearence = 30
        number_without_appearence = 0
        while True:
            i += 1

            number_without_appearence += 1
            if number_without_appearence > max_number_without_appearence:
                return

            max_number_of_same_errors = 100
            set_of_errors = set()
            ii = 0
            if max_number_of_same_errors <= len(driver.stack_of_errors):
                for err in driver.stack_of_errors:
                    set_of_errors.add(err)
                    if ii == max_number_of_same_errors:
                        break
                    ii += 1

                if len(set_of_errors) == 1:
                    return

            # deny blocking questions
            time.sleep(random_float_number(0, 1))
            click_btn_with(css_sel_or_xpath='.js-chrome-pushes-deny', _driver=driver)
            click_btn_with(css_sel_or_xpath='.js-continue', _driver=driver)
            click_btn_with(css_sel_or_xpath='.icon.js-ovl-close', _driver=driver)  # new match close
            click_btn_with(css_sel_or_xpath='.js-session-expire', _driver=driver, need_to_login=True)
            click_btn_with(css_sel_or_xpath='//div[@onclick="window.location.reload();"]', _driver=driver
                           , need_to_login=True
                           , use_xpath=True)
            # go to profile
            click_btn_with(css_sel_or_xpath='.b-link.js-profile-header-name.js-hp-view-element', _driver=driver)
            time.sleep(random_float_number(3, 4))

            appearance_div_h = return__element_by_xpath(xpath="//div[@class='form-label b']/b[contains(text(),\
             'Appearance:')]/parent::div//following-sibling::div", _driver=driver)

            if appearance_div_h is not None:
                number_without_appearence = 0
                tup = tuple(range(177, 184))
                girl_is_found = False
                print(f'testing --- {appearance_div_h.text}')
                for x in tup:
                    if str(x) in appearance_div_h.text:
                        about = return__element_by_xpath(xpath="//span[@class='profile-section__txt']", _driver=driver)
                        description_txt = f"!!!==>>>height = {x}, about={about.text if about is not None else ''}\
                            appearance={appearance_div_h.text} "

                        whole_info = return__element_by_xpath(xpath="//div[@class='profile__info']", _driver=driver)
                        whole_info_text = whole_info.text if whole_info is not None else ''

                        driver.girls_set.add((description_txt, whole_info_text) )
                        print(description_txt)


                        mixer.init()
                        mixer.music.load("a2002011001-e02-128k.mp3")
                        mixer.music.play()
                        # time.sleep(100000)

                        answer = input("to stop enter y: ")
                        if answer != 'y':
                            click_btn_with(css_sel_or_xpath='.js-profile-header-vote-yes', _driver=driver)
                            girl_is_found = True
                            mixer.music.stop()
                            break
                        else:
                            exit()

                if not girl_is_found:
                    click_btn_with(css_sel_or_xpath='.js-profile-header-vote-no', _driver=driver)
            else:
                click_btn_with(css_sel_or_xpath='.js-profile-header-vote-no', _driver=driver)
            time.sleep(random_float_number(1, 2))


# class selenium.webdriver.support.expected_conditions.staleness_of(element)[source]
if __name__ == '__main__':

    while True:
        main_circle()
