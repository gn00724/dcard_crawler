# -*- coding: utf-8 -*- 
from process import ConnectWeb
from process import GetDcardBoradList
from process import GetpostList
from process import Getcontent

import sqlite3

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

#2.renew all board
def renewPostList():
    conn = sqlite3.connect('./Resource/database/dcard.db')
    cursor = conn.cursor()
    boardList = cursor.execute('SELECT boardUrl From dcardBoardList')
    for x in boardList:
        _commad = "CREATE TABLE if not exists "
        _tableName = "board_"+ x[0].split("//")[2]
        _content = "(postID INT PRIMARY KEY NOT NULL, postUrl, MorF, School, postTime, countlikes, countComments, Content" + ")" 
        #print(_commad+_tableName+_content)
        cursor.execute(_commad+_tableName+_content)

        _url = "https://www.dcard.tw/" + x[0].split("//")[2]
        _commad = _url + "?latest=true"
        target = ConnectWeb(_commad)
        postdic = GetpostList(target,228980271)

        #To Create the class and get the data
        for key in postdic.keys():
            _url = postdic[key].c_url
            rawlist = Getcontent(_url)
            postdic[key].c_MorF = rawlist[4]
            postdic[key].c_school = rawlist[5]
            postdic[key].c_postTime = "2018+/" + rawlist[6]
            postdic[key].c_countLikes = rawlist[1]
            postdic[key].c_countComments = rawlist[2]
            postdic[key].c_postContent = rawlist[3]

        #To add in Table DB
        for addkey in postdic.keys():
            _commad = "INSERT OR REPLACE INTO "+_tableName
            _command_column = "(postID, postUrl, MorF, School, postTime, countlikes, countComments, Content) VALUES "
            _input = "(" \
                        + "\"" + str(addkey) + "\"" + ","  \
                        + "\""+ str(postdic[addkey].c_url)+ "\"" + "," \
                        + "\"" + str(postdic[addkey].c_MorF)+ "\"" \
                        + "\"" + str(postdic[addkey].c_school)+ "\"" \
                        + "\"" + str(postdic[addkey].c_postTime)+ "\"" \
                        + "\"" + str(postdic[addkey].c_countLikes)+ "\"" \
                        + "\"" + str(postdic[addkey].c_countComments)+ "\"" \
                        + "\"" + str(postdic[addkey].c_postContent)+ "\"" \
                        + ")"

            print(_commad + _command_column + _input)
            cursor.execute(_commad + _command_column + _input)




    conn.commit()
    conn.close()

renewBoardList()
renewPostList()
