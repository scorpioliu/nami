#!/usr/bin/env python

'''
givePinyin.py : simple pinyin tool based on viterbie

@author: scorpioLiu, shanzhongdeyunqi@gmail.com, 2012.01.31
@version: 0.1
@license: MIT
@copyright: (c) 2012, Project Nami
'''

from simpleSeg import simpleSeg

class pinyiMarker(simpleSeg):
    def __init__(self, wordFile, wordCoding, logFile, logCoding, lim):
        self.pMap, self.pinyinMap = self.getMap(wordFile, wordCoding)
        self.pLog = self.getLog(logFile, logCoding)
        self.lim = lim
        
    def getMap(self, wordFile, wordCoding):  
        pMap = {}
        pinyinMap = {}
        try:
            fi = open(wordFile, encoding = wordCoding)
        except Exception as e:
            print ('Err exists in opening', wordFile, ':', e)
            return pMap, pinyinMap
        for line in fi:
            line = line.split()
            pinyin = ''
            for i in range(0, len(line) - 2):
                pinyin = pinyin + '\'' + line[i]
            if line[-2] not in pMap:
                pMap[line[-2]] = int(line[-1])
                pinyinMap[line[-2]] = pinyin
            else:
                if pMap[line[-2]] < int(line[-1]):
                    pMap[line[-2]] = int(line[-1])
                    pinyinMap[line[-2]] = pinyin
        fi.close()
        return pMap, pinyinMap

    def givePinyin(self, s):
        pinyin = ''
        s = s.split()
        if 0 == len(s):
            return pinyin
        s = self.getSingleRes(s[0])
        s = s.split()   
        for i in s:
            pinyin += self.pinyinMap[i]
        return pinyin
    