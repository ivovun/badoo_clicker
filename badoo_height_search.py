import time
from random import randint
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions
import secret_keys
import datetime
import csv


class WebDriver:
    def __init__(self, _driver: webdriver):
        self.driver: webdriver = _driver
        self.driver.girls_set = set()

    def __enter__(self) -> webdriver:
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            log_file_name = "log_" + str(datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) + ".csv"
            with open(log_file_name, 'w', newline='') as csv_file:
                log_writer = csv.writer(csv_file, delimiter=' ',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for new_row in self.driver.girls_set:
                    log_writer.writerow([new_row])

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
            pass
        except ElementClickInterceptedException:
            # print(f' ElementClickInterceptedException  with css class:{kwargs.get("css_sel_or_xpath", "")} ')
            pass
        except Exception as ex:
            err_name = type(ex).__name__
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

    btn_login = _driver.find_element_by_xpath(css_sel_or_xpath) if use_xpath else\
        _driver.find_element_by_css_selector(f'{css_sel_or_xpath}')
    btn_login.click()
    time.sleep(random_float_number(0, 1))
    if need_to_login:
        login(_driver)
    return btn_login



@do_that_func_only_if_css_element_was_found
def get_user_name(_driver: webdriver) -> str:
    return _driver.find_element_by_css_selector('.profile-header__name').text


# class selenium.webdriver.support.expected_conditions.staleness_of(element)[source]


def login(_driver: webdriver):
    send_to_field_with(css_sel_or_xpath='.js-signin-login', keys=secret_keys.badoo_email, _driver=_driver)
    send_to_field_with(css_sel_or_xpath='.js-signin-password', keys=secret_keys.badoo_pass, _driver=_driver)
    click_btn_with(css_sel_or_xpath='.sign-form__submit', _driver=_driver)
    time.sleep(random_float_number(0, 1))
    driver.get('https://badoo.com/encounters')


def random_float_number(a: int, b: int):
    return randint(a * 10, b * 10)/10.0


def return__element_by_xpath(xpath: str, _driver:webdriver):
    try:
        # class selenium.webdriver.support.expected_conditions.staleness_of(element)[source]
        return _driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        pass
        # print(f'Unable to locate element with css class:{kwargs.get("css_sel_or_xpath", "")} ')
    return None


with WebDriver(webdriver.Chrome('./chromedriver')) as driver:
    driver.get('https://badoo.com/ru/signin/?f=top')
    # driver = webdriver.Chrome('./chromedriver')
    # driver.execute_script()
    login(driver)
    # driver.execute_script('document.body.style.zoom = "50 %"')
    driver.execute_script("document.body.style.transform='scale(0.5)'")
    unsuccessful_click_counter = 0
    i = 0
    old_user_or_error_name = ''
    while True:
        i += 1
        # deny blocking questions
        click_btn_with(css_sel_or_xpath='.js-chrome-pushes-deny', _driver=driver)
        click_btn_with(css_sel_or_xpath='.js-continue', _driver=driver)
        click_btn_with(css_sel_or_xpath='.icon.js-ovl-close', _driver=driver)  # new match close
        click_btn_with(css_sel_or_xpath='.js-session-expire', _driver=driver, need_to_login=True)
        click_btn_with(css_sel_or_xpath='//div[@onclick="window.location.reload();', _driver=driver, need_to_login=True
                       , use_xpath=True)

        # //div[@onclick="window.location.reload();"]
        time.sleep(random_float_number(1, 3))

        click_btn_with(css_sel_or_xpath='.b-link.js-profile-header-name.js-hp-view-element', _driver=driver)
        # river = webdriver.Chrome('./chromedriver')
        time.sleep(random_float_number(3, 4))
        # appearance_div_h = return__element_by_xpath("//b[contains(text(),'Appearance:')]", driver)

        # https://xmltoolbox.appspot.com/xpath_generator.html
        # https://www.softwaretestingclass.com/using-contains-sibling-ancestor-to-find-element-in-selenium/
        # sibElements = driver.findElements(By.xpath("//a[contains(text()," +\
        # "'Inside div block 2.')]/parent::div//following-sibling::div[@class='c']//a"));
        appearance_div_h = return__element_by_xpath("//div[@class='form-label b']/b[contains(text(),\
         'Appearance:')]/parent::div//following-sibling::div", driver)
        # //div[@class='form-label b']/b[contains(text(), 'Appearance:')]/parent::div//following-sibling::div
        # //div[@class='form-label b']/b[contains(text(), 'Appearance:')]/parent::div//following-sibling::div/text()
        # "//div[@class='form-label b']/b[contains(text(), 'Appearance:')]/parent::div//following-sibling::div").text
        if appearance_div_h is not None:
            tup = tuple(range(150, 184))
            girl_is_found = False
            print(f'testing --- {appearance_div_h.text}')
            for x in tup:
                # ошибка тут - отрибут текст отсутвует иногда у appearance_div_h.text  нужно добавить проверку на наличие атрибута
                if str(x) in appearance_div_h.text:
                    # click_btn_with(css_sel_or_xpath='js-profile-header-vote-yes', _driver=driver)
                    # File "/Users/vladimirfilippov/Dropbox/mbp/Developer/learning/py/dating/badoo/badoo_height_search.py", line 131, in <module>
                    #     # //span[@class='profile-section__txt']
                    # AttributeError: 'NoneType' object has no attribute 'text'

                    about = return__element_by_xpath("//span[@class='profile-section__txt']", driver)
                    # //span[@class='profile-section__txt']
                    description_txt = f"!!!!!! ===>>>height = {x}, about={about.text if about is not None else '' }\
                        appearance={appearance_div_h.text} "
                    driver.girls_set.add(description_txt)
                    print(description_txt)
                    click_btn_with(css_sel_or_xpath='.js-profile-header-vote-yes', _driver=driver)
                    girl_is_found = True
                    break

            if not girl_is_found:
                click_btn_with(css_sel_or_xpath='.js-profile-header-vote-no', _driver=driver)

            # time.sleep(4)
        else:
            click_btn_with(css_sel_or_xpath='.js-profile-header-vote-no', _driver=driver)

        # time.sleep(10000)
        time.sleep(random_float_number(1, 2))


        # was_clicked = 'like'
        # if randint(0, 1) == 1:
        #     click_btn_with(css_sel_or_xpath='js-profile-header-vote-yes', _driver=driver)
        # else:
        #     was_clicked = 'dislike'
        #     click_btn_with(css_sel_or_xpath='js-profile-header-vote-no', _driver=driver)
        # new_user_or_error_name = get_user_name(_driver=driver)
        # if new_user_or_error_name == old_user_or_error_name:
        #     unsuccessful_click_counter += 1
        #     if unsuccessful_click_counter >= 3:
        #         print(f"too many tries to click with no result (maybe hit the vote limit), lets sleep to wait\
        #         , user_or_error_name = {new_user_or_error_name}")
        #         time.sleep(60 * 60 * 1)
        #         unsuccessful_click_counter = 0
        # else:
        #     unsuccessful_click_counter = 0
        # old_user_or_error_name = new_user_or_error_name
        # print(f'{i}. {was_clicked}---{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}--user=>{old_user_or_error_name}')






# click_button(css_sel_or_xpath='js-chrome-pushes-deny', with_driver=driver)
# time.sleep(randint(1, 3))
