# -*- coding: utf-8 -*-
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.common.by import By
import pywhatkit as kit

def send_whatsapp(message):
    # Specify the phone number (with country code) and the message
    phone_number = st.secrets["PHONE_NUMBER"]

    # Send the message instantly
    kit.sendwhatmsg_instantly(phone_number, message)
    
def main():

    @st.cache_resource
    def get_driver():
        return webdriver.Chrome(
            service=Service(
                ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
            ),
            options=options,
        )

    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")

    driver = get_driver()
    
    # Get searched term from secrets
    search = st.secrets["SEARCH"]
    search = search.replace(" ", "+")
    search = search.upper()
    
    # Get page
    driver.get(f'https://www.in.gov.br/consulta/-/buscar/dou?q=%22{search}%22&s=todos&exactDate=all&sortType=0')
    driver.implicitly_wait(5)
    
    # Get number of results
    numberResults = driver.find_element(By.CLASS_NAME, 'search-total-label').text
    st.success(f'{numberResults}')
    
    # Get the latest result
    place = driver.find_elements(By.CLASS_NAME, 'hierarchy-item-marker')[1].text
    edition = driver.find_elements(By.CLASS_NAME, 'hierarchy-item-marker')[2].text
    latest = driver.find_elements(By.CLASS_NAME, 'title-marker')[0]
    latest_child = latest.find_element(By.TAG_NAME, 'a')
    title = latest_child.text
    url = latest_child.get_attribute('href')
    latest_description = f'Último resultado:\n{place}\n{edition}\n{title}\n{url}'
    st.success(latest_description)
    
    send_whatsapp(f'{numberResults}\n\n{latest_description}')

if __name__ == '__main__':
    main()