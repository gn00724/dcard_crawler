# -*- coding: utf-8 -*- 
from selenium import webdriver 
import time
import random
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup as bs
import sys

def ConnectFB(account,psd):
    m_headers = {
        'Referer':'https://duckduckgo.com/',
        'Host':'www.facebook.com',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection':'keep-alive',
        'Accept-Encoding':'br, gzip, deflate',
        'Accept-Language': 'zh-tw',
        'DNT': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6'
    }
    app_account = account
    app_psd = psd

    #_driver = webdriver.Chrome(executable_path="/Users/Mac/Documents/作品/Xcode/Python/New/chromedriver")
    _driver = webdriver.Safari()
    _driver.headers = m_headers

    x = _driver.get("https://www.google.com/")
    time.sleep(3)
    x = _driver.get("https://zh-tw.facebook.com/login")

    # send username and password
    elem = _driver.find_element_by_id('email')

    for x in app_account:
        elem.send_keys(x)
        time.sleep(random.randrange(1))

    elem = _driver.find_element_by_id('pass')
    for x in app_psd:
            elem.send_keys(x)
            time.sleep(random.randrange(1))

    # send enter to login
    elem = _driver.find_element_by_id('loginbutton')
    elem.click()
    print("login process")
    time.sleep(5)
    return _driver


def CheckFBProfile(_driver,ID):
    tmp_box = []
    m_driver = _driver

    # redirect to our mission
    usernameID = str(ID)
    x = m_driver.get("https://m.facebook.com/profile.php?v=info&id="+ usernameID)
    y = bs(m_driver.page_source, "html.parser")

    for _x in m_driver.find_elements_by_class_name("_5cdv"):
        _name = _x.parent.title # name
        if "性" in _x.text:
            tmp_box.append(_name)
            tmp_box.append(_x.text)
            break;

    x_age = m_driver.get("https://m.facebook.com/profile.php?id="+ usernameID)

    for age in m_driver.find_elements_by_class_name("_5xu4"):
        if "加入" in age.text:
            tmp_box.append(age.text.split("年")[0])
            break;

    return tmp_box


# Test Zone
aa = ConnectFB("appgn00724@gmail.com","Aa19820727")
nameIDList = [1353348899,100000387085704,100002028771508]

for x in nameIDList:
    print(CheckFBProfile(aa,x))





