"""Main module for scraping of fake emails from the database.

OS: Windows 10 64-bit
built in Python 3.9.2
"""


import logging
import os
import time
from typing import Generator

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

import utils

LOGIN = utils.read_txt("login.txt")
PASSWORD = utils.read_txt("pass.txt")
LOGIN_URL = "https://thenidiel.eu/login"
LOGOUT_URL = "https://thenidiel.eu/logout"
TIME = 1
OUTPUT_FILE = "output.csv"
PAGE_URLS = "page_urls.txt"
MAIL_URLS = "mail_urls.txt"


def set_scraper():
    """Function kills running applications and set up the ChromeDriver."""
    utils.killer("chrome.exe")
    utils.killer("excel.exe")

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

    return driver


def site_login(driver) -> None:
    """Function for login."""
    driver.get(LOGIN_URL)
    driver.find_element_by_id("email").send_keys(LOGIN)
    driver.find_element_by_id("password").send_keys(PASSWORD)
    time.sleep(TIME)
    driver.find_element_by_class_name("btn.btn-dark").click()


def site_logout(driver) -> None:
    """Function for logout."""
    time.sleep(TIME)
    driver.find_element_by_css_selector(
        "ul.navbar-nav.mr-auto> li:nth-child(4)> a.nav-link.dropdown-toggle"
    ).click()
    time.sleep(TIME)
    driver.find_element_by_xpath("//a[contains(., 'Logout')]").click()
    logging.info("Webscraping finished.")


def get_mail_link(driver) -> Generator:
    """Function for getting urls for emails."""
    time.sleep(TIME)
    last_page = driver.find_elements_by_css_selector("ul.pagination> li")[-2].text

    for suffix in range(1, int(last_page)):
        page_url = "https://thenidiel.eu/filter?page=" + str(suffix)
        utils.write_txt(PAGE_URLS, page_url)

    for page in utils.generate_txt(PAGE_URLS):
        driver.get(page)

        urls = driver.find_elements_by_css_selector(
            "tbody.email_table> tr> td:nth-child(1)> a"
        )

        for url in urls:
            adresa = url.get_attribute("href")

            yield adresa


def is_scraped(email: str, existing_file: str) -> bool:
    """Function checks if email url is contained in existing_file."""
    if os.path.exists(existing_file):
        with open(existing_file) as file:
            content = file.readlines()
            emails = content[0].split(",")
            if email in emails:
                return True
            return False
    else:
        utils.write_txt(MAIL_URLS, email)
        return False


def scrape_mail(driver) -> Generator:
    """Function returns Subject, Date, Abstract, Source, Link, Tags,
    Link, Mentioned characters, Body, Attachment links and Duplicate emails of the mail.
    If on of them is missing, returns empty string."""

    for mail in list(get_mail_link(driver)):
        if not is_scraped(mail, existing_file=MAIL_URLS):
            driver.get(mail)

            print(f"I am scraping: '{mail}'")

            try:
                date_child = driver.find_element_by_xpath(
                    "//strong[contains(text(), 'Date:')]"
                )
                date = (
                    date_child.find_element_by_xpath("..")
                    .text.replace("Date:", "")
                    .strip()
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
                    link_child.find_element_by_xpath("..")
                    .text.replace("Link:", "")
                    .strip()
                )
            except NoSuchElementException:
                link = ""

            try:
                tag = driver.find_element_by_id("tags_container").text
                tag_list = tag.split(" ")
            except NoSuchElementException:
                tag_list = []

            try:
                mentioned_parent = driver.find_element_by_id("characters_container")
                mentioned = mentioned_parent.find_elements_by_tag_name("a")
                mentioned_list = []

                for body in mentioned:
                    mentioned_list.append(body.text)

            except NoSuchElementException:
                mentioned_list = []

            try:
                body_child = driver.find_element_by_xpath(
                    "//strong[contains(text(), 'Body:')]"
                )
                body = (
                    body_child.find_element_by_xpath("..")
                    .text.replace("Body:", "")
                    .strip()
                )
            except NoSuchElementException:
                body = ""

            try:
                duplicate_date = driver.find_element_by_xpath(
                    "//*[@id='main-container']/main/div/div/div[1]/div/div[8]/div/table/tbody/tr/td[3]"
                ).text

            except NoSuchElementException:
                duplicate_date = ""

            result = {
                "result_date": date,
                "result_subject": subject,
                "result_abstract": abstract,
                "result_source": source,
                "result_link": link,
                "result_tag_list": tag_list,
                "result_mentioned_list": mentioned_list,
                "result_body": body,
                "result_duplicate_date": duplicate_date,
                "result_email_link": mail,
            }

            yield result
        else:
            print(f"This email has been already scraped: '{mail}'")


def save_result(driver) -> None:
    """Function saves results into csv."""
    for result in scrape_mail(driver):
        save = [
            result["result_date"],
            result["result_subject"],
            result["result_abstract"],
            result["result_source"],
            result["result_link"],
            result["result_tag_list"],
            result["result_mentioned_list"],
            result["result_body"],
            result["result_duplicate_date"],
        ]
        utils.write_csv(OUTPUT_FILE, save)
        utils.write_txt(MAIL_URLS, result["result_email_link"])


def main() -> None:
    """Main function that is call when the script is run."""

    driver = set_scraper()
    site_login(driver)
    get_mail_link(driver)
    scrape_mail(driver)
    save_result(driver)
    site_logout(driver)
    utils.remove(PAGE_URLS)


if __name__ == "__main__":
    main()
