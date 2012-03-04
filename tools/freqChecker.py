#!/usr/bin/env/python3

'''
freqChecker.py : give frequency of words from Baidu search engine.
Max search string length is 38 charactor.
Multiprocessor is used.

NOTE : Processing monitor only support Windows or Linux.

Processing monitor will wait 10 circles, 
after that it will kill process and create another one
State queue style is [pid, start time, end time, work content]
Start time is '' means work finish.
End time is '' means work begin.

@author: scorpioLiu, shanzhongdeyunqi@gmail.com, 2012.02.28
@version: 0.1
@license: MIT
@copyright: (c) 2012, Project Nami
'''

import platform
import os
import sys
import time
import random

import urllib.request
import urllib.parse

import multiprocessing
import queue

class procMonitor(multiprocessing.Process):
    def __init__(self, workQueue, resultQueue, statQueue, processNum):
        multiprocessing.Process.__init__(self)
        
        self.workQueue = workQueue
        self.resultQueue = resultQueue  
        self.statQueue = statQueue
        self.processorNum = processorNum
        self.kill_received = False
        self.statTable = {}
        self.killCnt = processorNum
        self.waitTime = 10.0
        self.workCnt = workQueue.qsize()
        self.finishCnt = 0
        
        platformType = platform.platform()
        if platformType.find('Windows') >= 0:
            self.platform = 'Windows'
        elif platformType.find('Linux') >= 0:
            self.platform = 'Linux'
        else:
            self.platform = 'Others'
    
        
    def run(self):
        while not self.kill_received:
            if self.finishCnt == self.workCnt:
                break
            
            while not self.statQueue.empty():
                procStat = self.statQueue.get()    
                if '' == procStat[2]:
                    self.statTable[procStat[0]] = [0, procStat[-1]]
                if '' == procStat[1]:
                    self.finishCnt += 1
                if '' == procStat[1] and procStat[0] in self.statTable:
                    self.statTable.pop(procStat[0])

            delVec = []
            for i in self.statTable:
                self.statTable[i][0] += 1
                if self.statTable[i][0] > 10: # Means 10 circle wait
                    if 'Windows' == self.platform:
                        killRes = os.system('taskkill /pid ' + str(i) + ' /F')                        
                    elif 'Linux' == self.platform:
                        killRes = os.system('kill ' + str(i))  
                    else:
                        continue
                    if 0 != killRes:
                        continue
                    delVec.append([i, self.statTable[i][1]])
                    
            # remove dead pid
            for i in delVec:
               self.killCnt += 1
               self.statTable.pop(i[0])
               self.workQueue.put(i[1]) 
               print (i[1], ' push back.')
               checker = baiduChecker(self.workQueue, self.resultQueue, self.statQueue, self.killCnt)
               checker.start()               
            time.sleep(self.waitTime/self.processorNum)
        print ('Monitor proccess finished.')

class baiduChecker(multiprocessing.Process):
    def __init__(self, wordQueue, resultQueue, statQueue, processNum):
        
        multiprocessing.Process.__init__(self)
                
        self.wordQueue = wordQueue
        self.resultQueue = resultQueue    
        self.statQueue = statQueue       
        self.kill_received = False
        
        self.processNum = processNum
        self.freqHead = 'style=\"margin-left:120px\">'
        self.freqEnd = '</span>'
        self.coding = 'gb18030' # encoding of Baidu is gb18030
        
    def __getPageData__(self, URL):
        try:
            content = urllib.request.urlopen(URL)
        except Exception as e:
            print ('Get', URL, 'failed :\n', e)
            return ''
        try:
            content = content.read().decode(self.coding)
        except Exception as e:
            print (e)
            return ''
        return content
    
    def __getFreq__(self, word):
        URL = 'http://www.baidu.com/s?wd=%22' + urllib.parse.quote(word) + '%22&' + 'inputT=%d' % int(500*random.random()+4000)
        content = self.__getPageData__(URL)
        i = content.find(self.freqHead)
        if i < 0:
            return 0, False
        i = i + 32
        j = i + content[i:].find(self.freqEnd) - 1
        freqStr = content[i:j]
        # Sometimes there is a char 'about'(yue in chinese) before num
        if not freqStr[0].isdigit():
            freqStr = freqStr[1:]            
        freqStr = freqStr.replace(',', '')
        try:
            freq = int(freqStr)
        except Exception as e:
            print (e)
            return 0, False
        return freq, True
    
    def run(self):
        while not self.kill_received:
            try:
                word = self.wordQueue.get_nowait()                
            except queue.Empty:
                break
            
            startTime = time.strftime('%Y%m%d%H%M%S', time.gmtime())
            self.statQueue.put([self.pid, startTime, '', word])
            try:
                freq, flag = self.__getFreq__(word)
            except Exception as e:
                print ('Err exists in get freq :', e)
                print (word, 'search failed', self.processNum)
                self.resultQueue.put([word, -1])
                endTime = time.strftime('%Y%m%d%H%M%S', time.gmtime())
                self.statQueue.put([self.pid, '', endTime, word])
                continue
            try:
                if flag:
                    self.resultQueue.put([word, freq])
                    print (word, freq, self.processNum)                    
                else:
                    self.resultQueue.put([word, -1])
                    print (word, 'search failed', self.processNum)                    
            except Exception as e:
                print ('Err exists in print or put :', e)
                endTime = time.strftime('%Y%m%d%H%M%S', time.gmtime())
                self.statQueue.put([self.pid, '', endTime, word])
                continue
            endTime = time.strftime('%Y%m%d%H%M%S', time.gmtime())
            self.statQueue.put([self.pid, '', endTime, word])
                
def createWordQueue(fileName, coding):
    try:
        fi = open(fileName, 'r', encoding = coding)
    except Exception as e:
        print ('Open', fileName, 'failed :', e)
    
    wordQueue = multiprocessing.Queue()
    wordSet = {}
    for line in fi:
        line = line.split()
        if 0 == len(line):
            continue
        if len(line[0]) > 38:
            print (line[0], 'is too long > 38, ignored')
            continue
        if line[0] not in wordSet:
            wordQueue.put(line[0])
            wordSet[line[0]] = 0
        else:
            print (line[0], 'already exists.')
    fi.close()
    
    return wordQueue, len(wordSet)
        
if '__main__' == __name__:
    platformType = platform.platform()
    if platformType.find('Windows') < 0 and  platformType.find('Linux'):
        print (platformType, 'is not support.')
        sys.exit(0)
    if len(sys.argv) < 3 or '--help' == sys.argv[1]:
        print ('Usage :', sys.argv[0], '{word list file}, {result file}, {word encode}, {processor num}')
        sys.exit(1)
    inFile = sys.argv[1]
    outFile = sys.argv[2]

    if 4 == len(sys.argv):
        coding = sys.argv[3]
    else:
        coding = 'gb18030'
        
    if 5 == len(sys.argv):
        processorNum = int(sys.argv[4])
    else:
        processorNum = 2
    
    wordQueue, wordNum = createWordQueue(inFile, coding)
    resultQueue = multiprocessing.Queue()
    statQueue = multiprocessing.Queue()
    resultVec = []
    wordHitSet = {}
    
    monitor = procMonitor(wordQueue, resultQueue, statQueue, processorNum)
    monitor.start()
     
    for i in range(processorNum):
        checker = baiduChecker(wordQueue, resultQueue, statQueue, i)
        checker.start()
    while len(wordHitSet) < wordNum:
        res = resultQueue.get()
        wordHitSet[res[0]] = 0
        if -1 != res[-1]:
            resultVec.append(res)
     
    resultVec.sort(key=lambda resultVec:resultVec[1], reverse=True)   
    fo = open(outFile, 'w', encoding = coding)
    for i in resultVec:
        fo.write(i[0] + ' ' + str(i[1]) + '\n')
    fo.close()
    
