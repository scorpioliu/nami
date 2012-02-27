#!/usr/bin/env python

'''
simpleSeg.py : simple segmentation based on forward Viterbie algorithm

@author: scorpioLiu, shanzhongdeyunqi@gmail.com, 2012.02.26
@version: 0.1
@license: MIT
@copyright: (c) 2012, Project Nami
'''

class forwardViterbie(object):
    def __init__(self, pMap, pLog, lim):
        self.pMap = pMap
        self.pLog = pLog
        self.lim = lim
        
    def getLeagleStr(self, s):
        idx = len(s)
        for i in range(len(s)):
            if ord(s[i]) < 0x4e00 or ord(s[i]) > 0x9fa5:
                idx = i
                break
        return s[0:idx]
        
    def giveState(self, s):
        s = self.getLeagleStr(s)
        t = []
        if 0 == len(s) or 0 == len(self.pLog) or 0 == len(self.pMap):
            return t    
        for i in range(len(s)):
            if 0 == i:
                t.append([[self.pLog[self.pMap[s[i]]], s[i]]])
                continue
            tc = []
            for j in range(0, i + 1):
                c = s[i - j:i + 1]
                if c not in self.pMap:
                    continue
                else:
                    if i == j:
                        tc.append([self.pLog[self.pMap[c]], c])
                        continue
                    tp = t[i - j - 1]
                    for k in range(len(tp)):
                        p = self.pLog[self.pMap[c]] + tp[k][0]
                        tc.append([p, tp[k][1] + ' ' + c])
            tc.sort(key=lambda tc:tc[1], reverse=True)
            tc = tc[0:self.lim]
            t.append(tc)
        return t

class simpleSeg(forwardViterbie):
    def __init__(self, wordFile, wordCoding, logFile, logCoding, lim):
        self.pMap = self.getMap(wordFile, wordCoding)
        self.pLog = self.getLog(logFile, logCoding)
        self.lim = lim
        
    def getMap(self, wordFile, wordCoding):  
        pMap = {}
        try:
            fi = open(wordFile, encoding = wordCoding)
        except Exception as e:
            print ('Err exists in opening', wordFile, ':', e)
            return pMap
        for line in fi:
            line = line.split()
            if line[-2] not in pMap:
                pMap[line[-2]] = int(line[-1])
            else:
                if pMap[line[-2]] < int(line[-1]):
                    pMap[line[-2]] = int(line[-1])
        fi.close()
        return pMap
    
    def getLog(self, logFile, logCoding):
        pLog = []
        try:
            fi = open(logFile, encoding = logCoding)
        except Exception as e:
            print ('Err exists in opening', logFile, ':', e)
            return pLog
        for line in fi:
            line = line.split(',')
            pLog.append(int(line[0]))
        fi.close()
        return pLog
          
    def showStateRes(self, s):
        t = self.giveState(s)
        if 0 == len(t):
            return
        maxLen = 0
        for i in t[-1]:
            maxLen = max(len(i[1]), maxLen)            
        for i in t[-1]:
            print (i[1].ljust(maxLen), ':', i[0])
            
    def getSingleRes(self, s):
        t = self.giveState(s)
        if len(t) > 0:
            return t[-1][0][1]
        else:
            return []

