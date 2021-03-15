from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

import time


def read_txt(file: str) -> str:
    """Function reads from txt file."""
    with open(file) as f:
        lines = f.readlines()
        return lines[0]


LOGIN = read_txt("login.txt")
PASSWORD = read_txt("pass.txt")
LOGIN_URL = "https://thenidiel.eu/login"
LOGOUT_URL = "https://thenidiel.eu/logout"
TIME = 1

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)


def site_login() -> None:
    """Function for login."""
    driver.get(LOGIN_URL)
    driver.find_element_by_id("email").send_keys(LOGIN)
    driver.find_element_by_id("password").send_keys(PASSWORD)
    time.sleep(TIME)
    driver.find_element_by_class_name("btn.btn-dark").click()


def site_logout() -> None:
    """Function for logout."""
    time.sleep(TIME)
    driver.find_element_by_css_selector(
        "ul.navbar-nav.mr-auto> li:nth-child(3)> a.nav-link.dropdown-toggle"
    ).click()
    time.sleep(TIME)
    driver.find_element_by_xpath("//a[contains(., 'Logout')]").click()


def get_mail_link() -> str:
    "Function for getting urls for emails."
    time.sleep(TIME)
    last_page = driver.find_elements_by_css_selector("ul.pagination> li")[-2].text
    PAGE_URLS = []

    for number in range(1, int(last_page)):
        page_url = "https://thenidiel.eu/filter?page=" + str(number)
        PAGE_URLS.append(page_url)

    for page in PAGE_URLS:
        driver.get(page)

        urls = driver.find_elements_by_css_selector(
            "tbody.email_table> tr> td:nth-child(1)> a"
        )

        for url in urls:
            adresa = url.get_attribute("href")
            yield adresa


def scrape_mail() -> str:
    """Function returns Subject, Date, Abstract, Source, Link, Tags,
    Link, Mentioned characters, Body, Attachment links and Duplicate emails of the mail.
    If on of them is missing, returns empty string."""

    for email in list(get_mail_link()):
        driver.get(email)

        try:
            date_child = driver.find_element_by_xpath(
                "//strong[contains(text(), 'Date:')]"
            )
            date = (
                date_child.find_element_by_xpath("..").text.replace("Date:", "").strip()
            )
        except NoSuchElementException:
            date = ""

        try:
            subject_child = driver.find_element_by_xpath(
                "//strong[contains(text(), 'Subject:')]"
            )
            subject = (
                subject_child.find_element_by_xpath("..")
                .text.replace("Subject:", "")
                .strip()
            )
        except NoSuchElementException:
            subject = ""

        try:
            abstract_child = driver.find_element_by_xpath(
                "//strong[contains(text(), 'Abstract:')]"
            )
            abstract = (
                abstract_child.find_element_by_xpath("..")
                .text.replace("Abstract:", "")
                .strip()
            )
        except NoSuchElementException:
            abstract = ""
        try:
            source_child = driver.find_element_by_xpath(
                "//strong[contains(text(), 'Source:')]"
            )
            source = (
                source_child.find_element_by_xpath("..")
                .text.replace("Source:", "")
                .strip()
            )
        except NoSuchElementException:
            source = ""
        try:
            link_child = driver.find_element_by_xpath(
                "//strong[contains(text(), 'Link:')]"
            )
            link = (
                link_child.find_element_by_xpath("..").text.replace("Link:", "").strip()
            )
        except NoSuchElementException:
            link = ""

        try:
            tag = driver.find_element_by_id("tags_container").text
            tag_list = tag.split(" ")
        except NoSuchElementException:
            tag_list = []

        try:
            mentioned = driver.find_element_by_id("characters_container").text
            mentioned_list = mentioned.split(" ")
        except NoSuchElementException:
            mentioned_list = []

    result = [date, subject, abstract, source, link, tag_list, mentioned_list]


def main():
    """Main function that is call when the script is run."""
    site_login()
    get_mail_link()
    scrape_mail()
    site_logout()


if __name__ == "__main__":
    main()
