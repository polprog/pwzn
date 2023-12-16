#!/usr/bin/env python3
# Ściągnij nagłówki ze strony PAPu i wypisz je na stdout
# PwZN 2023
# Wersja 1.0

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException


def get_driver():
    options=Options()
    # options.add_argument("--headless")
    options.add_argument("--height=900")
    options.add_argument("--width=1200")

    firefox_profile = FirefoxProfile()
    #firefox_profile.set_preference("javascript.enabled", False)
    options.profile = firefox_profile
    
    return webdriver.Firefox(options=options)


def pap_get_headings(driver: webdriver):
    driver.get("https://www.pap.pl")

    naglowek1 = driver.find_element(By.CSS_SELECTOR, "h3.title")

    wait = WebDriverWait(driver, timeout=2)
    wait.until(lambda d : naglowek1.is_displayed())

    print("Nagłówki są wyświetlone")

    return driver.find_elements(By.CSS_SELECTOR, "h3.title")



driver = get_driver()
naglowki = pap_get_headings(driver)


i = 0
for k in naglowki:
    print("%d: %s" % (i, k.text))
    try:
        link = k.find_element(By.CSS_SELECTOR, "a")
        print("[ %s ]" % link.get_attribute("href"))
    except NoSuchElementException:
        print("(brak hiperłącza)")
    print("-" * 40)
    i += 1


driver.quit()
