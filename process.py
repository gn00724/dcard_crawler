# -*- coding: utf-8 -*- 
from selenium import webdriver 
import time
import random
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup as bs
import sys
import sqlite3 as sql
from datetime import datetime
import re

#initZone
board_dic = {}

class DcardBoradList:
    def __init__(self, boardname, url):
            self.boardname = boardname
            self.url = "https://www.dcard.tw/" + url
            self.postlist = []

class Dcardpost:
    def __init__(self, c_postID):
            self.c_postID = int(c_postID)
            self.title = ""
            self.c_MorF = ""
            self.c_school = ""
            self.c_postTime = ""
            self.c_countLikes = int
            self.c_countComments = int
            self.c_url = ""
            self.c_postContent = ""

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

    #setting headless mode
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    try:
        _driver = webdriver.Chrome(executable_path="./Resource/driver/chromedriver", chrome_options=options)
    except:
        print("Using Windows chromedriver")
        _driver = webdriver.Chrome(executable_path="./Resource/driver/chromedriver.exe", chrome_options=options)
    _driver.headers = m_headers
    

    #Attach the Target html like man does
    #x = _driver.get("https://www.google.com/")
    #time.sleep(random.randint(1,3))
    x = _driver.get(m_url)
    print("Connect Done")
    time.sleep(random.randint(3,5))

    return _driver

def GetDcardBoradList(driver):
    m_driver = driver
    m_bs = bs(m_driver.page_source, "html.parser").find_all("li")
    board_dic = {}
    
    for x in m_bs:

        #Get url and boardtitle
        if x.a.get('href'):

            #make sure boardtitle is unique
            if board_dic.get(x.text) == None:
                board_dic[x.text] = DcardBoradList(boardname=x.text, url=x.a.get('href'))
    m_driver.close()
    return board_dic

def GetpostList(driver,datalstID):
    m_id = datalstID
    lstID = 0
    _driver = driver
    _driver.execute_script("window.scrollTo(0, 1000000)")
    #wait for loading
    time.sleep(random.randint(3,5))

    m_bs = bs(_driver.page_source, "html.parser").find_all("a", class_="PostEntry_root_V6g0r")
    m_postdict = {}
    _tmp = {}

    for x in m_bs:
        r = x.get('href').find('-')
        r1 = x.get('href')
        r_url = r1[0:r]
        r_title = r1[r+1:len(r1)]
        r_postID = r1[0:r].split("/")[-1]

        #Case that string have so many "-", so split use "-"" locate
        #url,title

        if not _tmp.__contains__(r_postID):
            _tmp[r_postID] = [r_url,  r_title]

    #search -1 sort keys and turn in to int
    lstID = int(list(_tmp.keys())[-1])

    if lstID > m_id:
        
        print(lstID, m_id)
        return GetpostList(_driver,m_id)

    else:
        print("lst = " + str(lstID) + " datalstID = " + str(datalstID) + " process Done")
        #when final check, add return bsitem
        for x in m_bs:
            r = x.get('href').find('-')
            r1 = x.get('href')
            r_url = r1[0:r]
            r_title = r1[r+1:len(r1)]
            r_postID = r1[0:r].split("/")[-1]

        #Case that string have so many "-", so split use "-"" locate
        #url,title

            if not m_postdict.__contains__(r_postID):
                m_postdict[r_postID] = Dcardpost(r_postID)
                m_postdict[r_postID].c_url = "https://www.dcard.tw" + r_url
                m_postdict[r_postID].c_title = r_title

        _driver.close()
        #print("returning " + str(m_postdict))
        return m_postdict
    

def Getcontent(article_url):
    #id, likes_count, respones_count, content
    m_url = article_url
    _driver = ConnectWeb(m_url)

    print("Trying to get post " + m_url)
    m_bs_id = ""
    m_content = ""
    m_likes = ""
    m_respons = ""
    m_MorF = ""
    m_school = ""
    m_date = ""

    try:
        m_bs_content = bs(_driver.page_source, "html.parser").find_all("div", class_="Post_content_NKEl9")
        m_bs_likes = bs(_driver.page_source, "html.parser").find_all("button", class_="PostFooter_likeBtn_jmo71")
        m_bs_respon = bs(_driver.page_source, "html.parser").find_all("button", class_="PostFooter_commentBtn_X8ZXa")
        m_bs_Author = bs(_driver.page_source, "html.parser").find_all("div", class_="PostAuthorHeader_avatar_1V21V")
        m_bs_Author_school = bs(_driver.page_source, "html.parser").find_all("span", class_="PostAuthor_root_3vAJf")
        m_bs_postDate = bs(_driver.page_source, "html.parser").find_all("span", class_="Post_date_2ipeY")

    except:
        print("Dcard was changed the class location")
    
    try:
        m_bs_id = m_url.split("/")[-1]
        m_content = CheckandRemoveEmoji(m_bs_content[0].text)
        m_likes = m_bs_likes[0].text.split(" ")[1]
        m_respons = m_bs_respon[0].text.split(" ")[1]
        m_MorF = "F" if "female" in str(m_bs_Author[0].contents[0]) else "M"
        m_school = CheckandRemoveEmoji(m_bs_Author_school[0].text)
        m_date = m_bs_postDate[0].text.replace("日", "").replace("月", "/")
    except:
        m_content = "Deleted"
        print(str(m_bs_id) + " the post was deleted")

    _driver.close()
    return [m_bs_id, m_likes, m_respons, m_content, m_MorF, m_school, m_date]


def CheckandRemoveEmoji(inputString):
    outputString = ""
    m_input = inputString

    emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                            "]+", flags=re.UNICODE)
    outputString= emoji_pattern.sub(r'', m_input) # no emoji
    return outputString


#print(Getcontent("https://www.dcard.tw/f/makeup/p/228944963"))

#the main tool to get class member
#boarddic = GetDcardBoradList(ConnectWeb("https://www.dcard.tw/f/"))
#keys = boarddic.keys()
#for x in keys:
#    boarddic[x].url
#    boarddic[x].boardname

print(Getcontent("https://www.dcard.tw/f/makeup/p/228965095"))