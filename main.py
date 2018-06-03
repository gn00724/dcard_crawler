# -*- coding: utf-8 -*- 
from process import ConnectWeb
from process import GetDcardBoradList
from process import GetpostList
from process import Getcontent
import threading

import sqlite3

#max_threading number
semlock = threading.BoundedSemaphore(10)

#scarpy Dcard and make the database as sqlite setting
#connect our db
def renewBoardList():
    conn = sqlite3.connect('./Resource/database/dcard.db')
    cursor = conn.cursor()

    #1.check the boradList and make the table
    target = ConnectWeb("https://www.dcard.tw/f/")
    boarddic = GetDcardBoradList(target)
    keys = boarddic.keys()
    #Create empty table if not exit, primary key is need to be set
    cursor.execute('''CREATE TABLE if not exists dcardBoardList("boardID" INT ,"boardUrl" PRIMARY KEY NOT NULL ,"boardName")''')
    boardCount = 0
    for x in keys:
        #Insert a row of data
        boardCount += 1
        _commad = "INSERT OR REPLACE INTO dcardBoardList(boardID,boardUrl,boardName) VALUES "
        _input = "(" + "\"" + str(boardCount) + "\"" + ","  + "\""+ str(boarddic[x].url)+ "\"" + "," + "\"" + str(boarddic[x].boardname)+ "\"" + ")"
        print(_commad + _input)
        cursor.execute(_commad + _input)

    #Done And Close
    conn.commit()
    conn.close()

    print("renewBoardList Done")

#2.renew all board
def renewPostList():
    conn = sqlite3.connect('./Resource/database/dcard.db')
    cursor = conn.cursor()
    boardList = list(cursor.execute('SELECT boardUrl From dcardBoardList'))
    _tcount = 0
    _tcount2 = 0

    conn.commit()
    conn.close()

    for x in boardList:
        conn = sqlite3.connect('./Resource/database/dcard.db')
        cursor = conn.cursor()
        _tcount2 = 0
        _tcount += 1
        print("Trying to calBoard " + str(_tcount) + " of " + str(len(boardList)))

        _commad = "CREATE TABLE if not exists "
        _tableName = "board_"+ x[0].split("//")[2]
        try:
            _tableName = "board_" + _tableName.split("f/")[1]
        except:
            None
        _content = "(postID INT PRIMARY KEY NOT NULL, postUrl, MorF, School, postTime, countlikes, countComments, Content" + ")" 
        print(_commad+_tableName+_content)
        cursor.execute(_commad+_tableName+_content)

        _url = "https://www.dcard.tw/" + x[0].split("//")[2]
        _commad = _url + "?latest=true"
        print("deal with url " + _url)

        target = ConnectWeb(_commad)
        postdic = GetpostList(target,228994827)

        #To Create the class and get the data
        for key in postdic.keys():
            _total = len(postdic.keys())
            _tcount2 += 1
            semlock.acquire()
            mthread = threading.Thread(target=givevalue_thread,args=(postdic[key],_tcount2,_total) ,name="threading_" + str(_tcount2))
            mthread.start()
        
        mthread.join()
        #To add in Table DB
        for addkey in postdic.keys():
            _commad = "INSERT OR REPLACE INTO "+_tableName
            _command_column = "(postID, postUrl, MorF, School, postTime, countlikes, countComments, Content) VALUES "
            _input = "(" \
                        + "\"" + str(addkey) + "\"" + ","  \
                        + "\""+ str(postdic[addkey].c_url)+ "\"" + "," \
                        + "\"" + str(postdic[addkey].c_MorF)+ "\"," \
                        + "\"" + str(postdic[addkey].c_school)+ "\"," \
                        + "\"" + str(postdic[addkey].c_postTime)+ "\"," \
                        + "\"" + str(postdic[addkey].c_countLikes)+ "\"," \
                        + "\"" + str(postdic[addkey].c_countComments)+ "\"," \
                        + "\"" + str(postdic[addkey].c_postContent)+ "\")"

            print(_commad + _command_column + _input)
            try:
                cursor.execute(_commad + _command_column + _input)
            except:
                #May have some Emoji but pass thought the check
                _commad = "INSERT OR REPLACE INTO "+_tableName
                _command_column = "(postID, postUrl, MorF, School, postTime, countlikes, countComments, Content) VALUES "
                _input = "(" \
                        + "\"" + str(addkey) + "\"" + ","  \
                        + "\""+ str(postdic[addkey].c_url)+ "\"" + "," \
                        + "\"" + str(postdic[addkey].c_MorF)+ "\"," \
                        + "\"" + str(postdic[addkey].c_school)+ "\"," \
                        + "\"" + str(postdic[addkey].c_postTime)+ "\"," \
                        + "\"" + str(postdic[addkey].c_countLikes)+ "\"," \
                        + "\"" + str(postdic[addkey].c_countComments)+ "\"," \
                        + "\"" + "Content ERROR"+ "\")"

                cursor.execute(_commad + _command_column + _input)
            
        conn.commit()
        conn.close()
        
    print("renewPostList Done")

def givevalue_thread(class_postdickey,count,total):
    m_postdic = class_postdickey
    print("Trying to calPost " + str(count) + " of " + str(total))

    _url = m_postdic.c_url
    rawlist = Getcontent(_url)
    m_postdic.c_MorF = rawlist[4]
    m_postdic.c_school = rawlist[5]
    m_postdic.c_postTime = "2018/" + rawlist[6]
    m_postdic.c_countLikes = rawlist[1]
    m_postdic.c_countComments = rawlist[2]
    m_postdic.c_postContent = rawlist[3]

    semlock.release()
    print("realease")

renewPostList()