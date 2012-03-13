#!/usr/bin/env python3

'''
freqChecker.py : give frequency of words from Baidu search engine.
Max search string length is 38 charactor.
Multiprocessor is used.

NOTE : Processing monitor only support Windows or Linux.

Processing monitor will wait 5 circles, 
after that it will kill process and create another one
State queue style is [pid, process time, work content, return stat]
2 means return good
1 means start to search
0 means print Err
-1 means can not find content in page
-2 means error exists in page
-3 means monitor finish


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
        self.killReceived = False
        self.killCnt = processorNum
        self.waitTime = 10.0
        self.waitCircle = 3
        self.workCnt = workQueue.qsize()
        self.finishCnt = 0
        self.statTable = {}
        self.platform = self.__getPlatform()
        
    def __getPlatform(self):
        platformType = platform.platform()
        if platformType.find('Windows') >= 0:
            return 'Windows'
        elif platformType.find('Linux') >= 0:
            return 'Linux'
        else:
            return 'Others'
    
    def __killSingleProc(self, pid):
        if 'Windows' == self.platform:
            os.system('taskkill /pid ' + str(pid) + ' /F')                   
        elif 'Linux' == self.platform:
            os.system('kill ' + str(pid))
        else:
            return False
        return True
    
    def __killAllProc(self):
        time.sleep(self.waitTime)
        # Collect all the live process
        while not self.statQueue.empty():
            procStat = self.statQueue.get()    
            if 1 == procStat[-1]:
                self.statTable[procStat[0]] = [0, procStat[2]]
        for i in self.statTable:
            self.__killSingleProc(i)
        self.statTable = []
        self.resultQueue.put(['NULL', -3])
        
    def run(self):
        waitRound = 0
        fullKillRound = 0
        badCnt = 0
        while not self.killReceived:
            if self.finishCnt == self.workCnt:
                break
            
            while not self.statQueue.empty():
                procStat = self.statQueue.get()    
                if 1 == procStat[-1]:
                    self.statTable[procStat[0]] = [0, procStat[2]]
                if 1 != procStat[-1]:
                    self.finishCnt += 1
                if 1 != procStat[-1] and procStat[0] in self.statTable:
                    self.statTable.pop(procStat[0])
                if -1 != procStat[-1] and 1 != procStat[-1]:
                    badCnt = 0
                elif -1 == procStat[-1]:
                    badCnt += 1
            if self.waitCircle * self.processorNum < badCnt:
                self.__killAllProc()
                break
            
            delVec = []
            killCnt = 0
            for i in self.statTable:
                self.statTable[i][0] += 1
                if self.statTable[i][0] > self.waitCircle: 
                    if 'Windows' == self.platform:
                        killRes = os.system('taskkill /pid ' + str(i) + ' /F')                   
                    elif 'Linux' == self.platform:
                        killRes = os.system('kill ' + str(i))
                    else:
                        continue
					# No matter kill success or not, pid must delete
                    if 0 == killRes :
                        killCnt += 1
                        delVec.append([i, self.statTable[i][1], True])
                    else:
                        delVec.append([i, self.statTable[i][1], False])
            
            if killCnt >= self.processorNum:
                fullKillRound += 1
                if fullKillRound > self.waitCircle:
                    self.__killAllProc()
                    print ('All proc are blocked, so spider closed.')
                    break
            else:
                fullKillRound = max(0, fullKillRound - 1)
                    
            # remove dead pid
            for i in delVec:
               self.statTable.pop(i[0])
               self.workQueue.put(i[1]) 
               print (i[1], ' push back.')
               if i[2]:
                   checker = baiduChecker(self.workQueue, self.resultQueue, self.statQueue, self.killCnt)
                   checker.start()
                   self.killCnt += 1
            
            # if num of process below processor num for long time, create new process
            # Monitor may create more process than processor number
            # but after process killed, it will become normal number.
            if self.processorNum > len(self.statTable):
                waitRound += 1
                if waitRound > self.waitCircle:
                    waitRound = 0
                    for i in range(self.processorNum - len(self.statTable)):
                        checker = baiduChecker(self.workQueue, self.resultQueue, self.statQueue, self.killCnt)
                        checker.start()
                        self.killCnt += 1
            else:
                waitRound = 0
			
            print ('Monitor is working', self.statTable)
            time.sleep(self.waitTime/self.processorNum)
            if self.workQueue.empty():
                self.resultQueue.put(['NULL', -3])
                break            
        print ('Monitor proccess finished.')

class baiduChecker(multiprocessing.Process):
    def __init__(self, workQueue, resultQueue, statQueue, processNum):
        
        multiprocessing.Process.__init__(self)
                
        self.workQueue = workQueue
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
                word = self.workQueue.get_nowait()                
            except queue.Empty:
                break
            startTime = time.strftime('%Y%m%d%H%M%S', time.gmtime())
            self.statQueue.put([self.pid, startTime, word, 1]) # 1 means start
            try:
                freq, flag = self.__getFreq__(word)
            except Exception as e:
                print ('Err exists in get freq :', e)
                print (word, 'search failed', self.processNum)
                self.resultQueue.put([word, -2]) # -2 means bad code style in page
                endTime = time.strftime('%Y%m%d%H%M%S', time.gmtime())
                self.statQueue.put([self.pid, endTime, workQueue, -2])
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
                self.statQueue.put([self.pid, endTime, word, 0]) # 0 means just print failed
                continue
            endTime = time.strftime('%Y%m%d%H%M%S', time.gmtime())
            if flag: 
                self.statQueue.put([self.pid, endTime, word, 2]) # 2 means just return right
            else:
                self.statQueue.put([self.pid, endTime, word, -1]) # -1 means search failed
        print (self.pid, 'closed.')
                
def createWorkQueue(fileName, coding):
    try:
        fi = open(fileName, 'r', encoding = coding)
    except Exception as e:
        print ('Open', fileName, 'failed :', e)
    
    workQueue = multiprocessing.Queue()
    wordSet = {}
    for line in fi:
        line = line.split()
        if 0 == len(line):
            continue
        if len(line[0]) > 38:
            print (line[0], 'is too long > 38, ignored')
            continue
        if line[0] not in wordSet:
            workQueue.put(line[0])
            wordSet[line[0]] = 0
        else:
            print (line[0], 'already exists.')
    fi.close()
    
    return workQueue, len(wordSet)
        
if '__main__' == __name__:
    platformType = platform.platform()
    if platformType.find('Windows') < 0 and platformType.find('Linux') < 0:
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
    
    workQueue, wordNum = createWorkQueue(inFile, coding)
    resultQueue = multiprocessing.Queue()
    statQueue = multiprocessing.Queue()
    resultVec = []
    wordHitSet = {}
    
    monitor = procMonitor(workQueue, resultQueue, statQueue, processorNum)
    monitor.start()
     
    for i in range(processorNum):
        checker = baiduChecker(workQueue, resultQueue, statQueue, i)
        checker.start()
    while len(wordHitSet) < wordNum:
        res = resultQueue.get()
        if -3 == res[-1]: 
            break
        wordHitSet[res[0]] = 0
        if res[-1] >= 0:
            resultVec.append(res)
    
    resultVec.sort(key=lambda resultVec:resultVec[1], reverse=True)   
    fo = open(outFile, 'w', encoding = coding)
    for i in resultVec:
        fo.write(i[0] + ' ' + str(i[1]) + '\n')
    fo.close()
    
