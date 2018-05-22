# -*- coding: utf-8 -*- 
import process

tmpdriver = process.ConnectWeb("https://www.dcard.tw/f/tvepisode?latest=true")
print(process.GetpostList(tmpdriver,228780271))
