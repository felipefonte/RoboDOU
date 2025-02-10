# -*- coding: utf-8 -*-
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.common.by import By
    
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
    # Get number of results
    driver.implicitly_wait(5)
    numberResults = driver.find_element(By.CLASS_NAME, 'search-total-label')
    numberResultsText = numberResults.text
    print(numberResultsText)
    # Show result
    st.success(f'{numberResultsText}')

    #with st.echo():
    #st.code(driver.page_source)
    driver.quit()


if __name__ == '__main__':
    main()