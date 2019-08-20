import pytest, random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date, timedelta, datetime


def random_date(start_date, end_date):
    return start_date + timedelta(
        seconds=random.randint(0, int((end_date - start_date).total_seconds())))


@pytest.fixture()
def browser():
    browser = webdriver.Chrome()
    yield browser
    browser.quit()


class TestRegistrationForm(object):
    def test_send_registration_form(self, browser):

        link = "https://form.jotformeu.com/92314680969367"
        birthday_date = random_date(date(1920, 1, 1), date(2019, 1, 1))
        instruments = ['Violin', 'Guitar', 'Bass', 'Drums', 'Vocals']
        browser.get(link)

        name = browser.find_element_by_id("first_3")
        name.send_keys("Lena")

        last_name = browser.find_element_by_id("last_3")
        last_name.send_keys("Serg")

        select_month = Select(browser.find_element_by_id("input_4_month"))
        select_month.select_by_value(birthday_date.strftime("%B"))

        select_day = Select(browser.find_element_by_id("input_4_day"))
        select_day.select_by_value(str(birthday_date.day))

        select_year = Select(browser.find_element_by_id("input_4_year"))
        select_year.select_by_value(str(birthday_date.year))

        select_instrument = Select(browser.find_element_by_id("input_5"))
        select_instrument.select_by_value(random.choice(instruments))

        browser.find_element_by_id('input_6_0').click()

        comment = browser.find_element_by_id('input_8')
        comment.send_keys("I want to study!")

        browser.execute_script("window.scrollBy(0, 222);")

        button = browser.find_element_by_id('input_2')
        button.click()

        success_msg = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h1')))

        assert 'Thank You' in success_msg.text

    def test_send_empty_registration_form(self, browser):
        link = "https://form.jotformeu.com/92314680969367"
        browser.get(link)
        browser.execute_script("window.scrollBy(0, 222);")

        button = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, 'input_2')))
        button.click()

        error_msg = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '.form-button-error > p')))

        assert 'There are errors on the form. Please fix them before continuing.' in error_msg.text
