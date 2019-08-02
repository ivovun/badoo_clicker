import os
import time
from selenium import webdriver
import datetime
from common import (
    WebDriver,
    send_to_field_with,
    click_btn_with,
    set_scale,
    do_that_func_only_if_css_element_was_found,
    random_float_number,
    return__element_by_xpath,
    ask_question_with_sound,
    format_text_for_terminal_print,
    return_first_existing_element_or_none_for
)
import re


@do_that_func_only_if_css_element_was_found
def get_user_name(_driver: webdriver) -> str:
    return _driver.find_element_by_css_selector('.profile-header__name').text


def login(_driver: webdriver):
    send_to_field_with(css_sel_or_xpath='.js-signin-login', keys=BADOO_EMAIL, _driver=_driver)
    send_to_field_with(css_sel_or_xpath='.js-signin-password', keys=BADOO_PASS, _driver=_driver)
    click_btn_with(css_sel_or_xpath='//button[@class="btn btn--sm btn--block"]', _driver=_driver, login_func=login
                   , use_xpath=True)
    time.sleep(random_float_number(1, 2))

    # if unsuccessful login, lets retry
    sign_in_link = return__element_by_xpath(xpath="//a[@class='link js-signin-link']", _driver=_driver)
    if sign_in_link is not None:
        sign_in_link.click()
        time.sleep(2)
        login(_driver)

    set_scale(_driver)
    time.sleep(3)
    _driver.get('https://badoo.com/encounters')


def main_cycle():
    with WebDriver(webdriver.Chrome('./chromedriver'), 'badoo_height_search_logs') as driver:
        driver.get('https://badoo.com/ru/signin/?f=top')
        login(driver)
        i = 0
        max_number_without_appearence = 30
        number_without_appearance = 0
        while True:
            i += 1
            number_without_appearance += 1
            if number_without_appearance > max_number_without_appearence:
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
            click_btn_with(css_sel_or_xpath='.js-session-expire', _driver=driver, login_func=login)
            click_btn_with(css_sel_or_xpath='//div[@onclick="window.location.reload();"]', _driver=driver,
                           login_func=login, use_xpath=True)
            set_scale(driver)

            go_to_profile_xpath = '//*[@class ="b-link js-profile-header-name js-hp-view-element"]'
            click_btn_with(css_sel_or_xpath=go_to_profile_xpath, _driver=driver, use_xpath=True)
            # click_btn_with(css_sel_or_xpath='.b-link.js-profile-header-name.js-hp-view-element', _driver=driver)
            time.sleep(random_float_number(0, 1))

            page_content_main = return_first_existing_element_or_none_for(xpaths=("//*[@id='app_c']",
                                                                                  "//*[contains(@class,'has-profile-info')]",
                                                                                  "//*[contains(@class ,'profile--info')]"),
                                                                          _driver=driver)
            if page_content_main:

                name_span = return_first_existing_element_or_none_for(
                    xpaths=('//*[contains(@class,"profile-header__user")]',
                            '//*[contains(@data-element-name,"userName")]',
                            '//*[contains(@class,"js-profile-header-name")]'),
                    _driver=driver)

                name_span_txt = (name_span.text.strip() if name_span is not None else '').replace('\n', '')

                page_content_main_text = format_text_for_terminal_print(page_content_main.text)

                number_without_appearance = 0
                heights = tuple(map(str, range(177, 184)))
                girl_is_found = False
                print(f'{"-" * 100}')
                print(f'testing --{datetime.datetime.now().strftime("%d.%m, %H:%M:%S")}'
                      f'--[{name_span_txt}] ==> {page_content_main_text}')
                have_kids = False
                if 'Kids:' in page_content_main_text:  # kids
                    if 'Someday' not in page_content_main_text and 'No, never' not in page_content_main_text:
                        rids_str = ' ==== KIDS ===================================='
                        print(rids_str)
                        # print(page_content_main_text.replace('\n', '  '))
                        print(rids_str)
                        have_kids = True
                if not have_kids:
                    for search_word in heights:
                        search_word += ' cm'
                        if search_word in page_content_main_text:

                            description_txt = format_text_for_terminal_print(
                                f"!!!==>>>height = {search_word},[{name_span_txt}]")
                            driver.girls_set.add((description_txt, page_content_main_text))
                            print(description_txt)

                            while True:
                                answer = ask_question_with_sound(
                                    question="to finish enter 'f', for vote-NO enter: 'n', "
                                             "for vote-YES enter: 'y' : "
                                    , sound_file="a2002011001-e02-128k")
                                if answer not in ['f', 'n', 'y', 'F', 'N', 'Y']:
                                    continue
                                if answer == 'f':
                                    exit()
                                elif answer == 'n':
                                    girl_is_found = False
                                elif answer == 'y':
                                    girl_is_found = True
                                break

                click_btn_with(css_sel_or_xpath='.js-profile-header-vote-' + ('yes' if girl_is_found else 'no')
                               , _driver=driver)

        else:
            click_btn_with(css_sel_or_xpath='.js-profile-header-vote-no', _driver=driver)
        time.sleep(random_float_number(0, 1))


BADOO_EMAIL = os.environ.get('BADOO_EMAIL')
BADOO_PASS = os.environ.get('BADOO_PASS')

if __name__ == '__main__':

    if not BADOO_EMAIL or not BADOO_PASS:
        ask_question_with_sound(
            question="BADOO_EMAIL and BADOO_PASS isn't set in environ, press any key to stop music (and exit program): "
            , sound_file="Pink Floyd - Another Brick In The Wall (HQ)")
        exit()
    try:
        while True:
            main_cycle()
    except Exception as ex:
        print(f" error = {ex}")
        ask_question_with_sound(question="Error has occurred!  press any key to stop music (and exit program): "
                                , sound_file="Pink Floyd - Another Brick In The Wall (HQ)")
        raise ex
