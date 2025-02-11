# -*- coding: utf-8 -*-
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.common.by import By
import smtplib
from email.mime.text import MIMEText
from datetime import date

def send_email(body):

    # Taking inputs
    email_sender = st.secrets["EMAIL_SENDER"]
    email_password = st.secrets["EMAIL_PASSWORD"]
    email_receiver = st.secrets["EMAIL_RECEIVER"]
    subject = "DOU " + str(date.today())

    # Send email
    try:
        msg = MIMEText(body)
        msg['From'] = email_sender
        msg['To'] = email_receiver
        msg['Subject'] = subject
        
        server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
        server.starttls()
        server.login(email_sender, email_password)
        server.sendmail(email_sender, email_receiver, msg.as_string())
        server.quit()

        st.success('Email sent successfully! 🚀')
    except Exception as e:
        st.error(f"Failed to send email: {e}")
    
    
def get_item_from_dou():

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
    
    try:
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

        # Send email
        send_email(f'{numberResults}\n\n{latest_description}')
    except Exception as e:
        st.error(f"Failed to read DOU: {e}")

if __name__ == '__main__':
    get_item_from_dou()