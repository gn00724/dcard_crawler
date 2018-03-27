# -*- coding: utf-8 -*- 
from selenium import webdriver 
import time
import random
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup as bs
import sys

#"appgn00724@gmail.com" "Aa19820727"

#googleDriver_mobile Setup

#initZone
board_dic = {}

class DcardBoradList:
    def __init__(self, boardname, url):
            self.boardname = boardname
            self.url = "https://www.dcard.tw/" + url

def waitForload(driver):
    elem = driver.find_element_by_tag_name("html")
    count = 0
    while True:
        count += 1
        if count > 20:
            print("Timeing out after 10 seconds and returning")
            return
        time.sleep(random.randint(0.5,3))
        try:
            elem == driver.find_element_by_tag_name("html")
        except StaleElementReferenceException:
            return

def ConnectWeb(url):
    m_url = url
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

    #mobile_emulation = { "deviceName": "iPhone 6" }
    #chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    #_driver = webdriver.Chrome(executable_path="./Resource/driver/chromedriver",chrome_options = chrome_options)

    _driver = webdriver.Chrome(executable_path="./Resource/driver/chromedriver")
    _driver.headers = m_headers
    

    #Attach the Target html like man does
    x = _driver.get("https://www.google.com/")
    time.sleep(random.randint(1,3))
    x = _driver.get(m_url)
    print("Connect Done")
    time.sleep(random.randint(1,3))

    return _driver

def GetDcardBoradList(driver):
    m_driver = driver
    m_bs = bs(m_driver.page_source, "html.parser").find_all("li")
    m_boardlist = []
    
    for x in m_bs:

        #Get url and boardtitle
        if x.a.get('href'):

            #make sure boardtitle is unique
            if board_dic.get(x.text) == None:
                board_dic[x.text] = DcardBoradList(boardname=x.text, url=x.a.get('href'))

    return board_dic

boarddic = GetDcardBoradList(ConnectWeb("https://www.dcard.tw/f/"))

#the main tool to get class member
#keys = boarddic.keys()
#for x in keys:
#    boarddic[x].url
#    boarddic[x].boardname
    