#!/usr/bin/env/python3

'''
webInfoChecker : Claw the web page to get special content.
Multiprocessor is used.

@author: scorpioLiu, shanzhongdeyunqi@gmail.com, 2012.03.01
@version: 0.1
@license: MIT
@copyright: (c) 2012, Project Nami
'''

import sys
import time
import random

import urllib.request
import urllib.parse

import multiprocessing
import queue

class procMonitor(multiprocessing.Process):
    def __init__(self, workQueue, resultQueue, statQueue, processNum, configList):
        multiprocessing.Process.__init__(self)
        
        self.workQueue = workQueue
        self.resultQueue = resultQueue  
        self.statQueue = statQueue
        self.processorNum = processorNum
        self.configList = configList
        self.kill_received = False
        self.statTable = {}
        self.killCnt = processorNum
        self.waitTime = 10.0
    
    def run(self):
        while not self.kill_received:
            if self.workQueue.empty():
                break
            
            delVec = []
            while not self.statQueue.empty():
                procStat = self.statQueue.get_nowait() 
        
                if '' == procStat[2]:
                    self.statTable[procStat[0]] = [0, procStat[-1]]
                if '' == procStat[1] and procStat[0] in self.statTable:
                    self.statTable.pop(procStat[0])

            for i in self.statTable:
                self.statTable[i][0] += 1
                if self.statTable[i][0] > self.waitTime:
                    killRes = os.system('taskkill /pid ' + str(i) + ' /F')
                    if 0 != killRes:
                        continue
                    delVec.append([i, self.statTable[i][1]])
                    
            # remove dead pid
            for i in delVec:
               self.killCnt += 1
               self.statTable.pop(i[0])
               self.workQueue.put(i[1]) 
               checker = webInfoChecer(self.workQueue, self.resultQueue, self.statQueue, self.killCnt, self.configList)
               checker.start()
               
            time.sleep(self.waitTime/self.processorNum)
               

class webInfoChecer(multiprocessing.Process):
    def __init__(self, wordQueue, resultQueue, statQueue, processNum, configList):
        
        multiprocessing.Process.__init__(self)
                
        self.wordQueue = wordQueue
        self.resultQueue = resultQueue  
        self.statQueue = statQueue      
        self.kill_received = False
        
        self.processNum = processNum
        self.contentHead = '<span class=\"w-change\">'
        self.contentEnd = '</span>'
        self.freqHeadList = configList[0]
        self.freqEndList = configList[1]
        self.coding = 'utf8' 
        
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
    
    def __getContent__(self, word):
        URL = 'http://dict.cn/' + urllib.parse.quote(word)
        content = self.__getPageData__(URL)
        # Check if special content tag exists 
        i = content.find(self.contentHead)
        if i < 0:
            return [], False
        i = i + len(self.contentHead)
        j = i + content[i:].find(self.contentEnd)
        contentArea = content[i:j]
        res = []
        for k in range(len(self.freqHeadList)):
            i = contentArea.find(self.freqHeadList[k])
            if i < 0:
                res.append([])
            else:
                i += len(self.freqHeadList[k])
                j = i + contentArea[i:].find(self.freqEndList[k])
                res.append(contentArea[i:j])        
        return res, True
    def run(self):
        while not self.kill_received:
            # this will not needed.
            time.sleep(1)
            try:
                word = self.wordQueue.get_nowait()                
            except queue.Empty:
                break
            startTime = time.strftime('%Y%m%d%H%M%S', time.gmtime())
            self.statQueue.put([self.pid, startTime, '', word])
            try:
                freq, flag = self.__getContent__(word)
            except Exception as e:
                print ('Err exists in get freq :', e)
                print (word, 'search failed', self.processNum)
                self.resultQueue.put([word, []])
                endTime = time.strftime('%Y%m%d%H%M%S', time.gmtime())
                self.statQueue.put([self.pid, '', endTime, word])
                continue
            try:
                if flag:
                    self.resultQueue.put([word, freq])
                    #print (word, freq, self.processNum)                    
                else:
                    self.resultQueue.put([word, []])
                    #print (word, 'search failed', self.processNum)                    
            except Exception as e:
                print ('Err exists in print or put :', e)
                endTime = time.strftime('%Y%m%d%H%M%S', time.gmtime())
                self.statQueue.put([self.pid, '', endTime, word])
                continue
            
            endTime = time.strftime('%Y%m%d%H%M%S', time.gmtime())
            self.statQueue.put([self.pid, '', endTime, word])
                
def createWordQueue(fileName, coding, configFile):
    configList = [[],[]]
    wordQueue = multiprocessing.Queue()
    
    try:
        fi = open(configFile, 'r', encoding = coding)
    except Exception as e:
        print ('Open', configFile, 'failed :', e)
        return wordQueue, len(wordSet), configList
    
    for line in fi:
        configHead = line.split()[0]
        configEnd = '</a>'
        configList[0].append(configHead)
        configList[1].append(configEnd)
    fi.close()

    wordSet = {}
    try:
        fi = open(fileName, 'r', encoding = coding)
    except Exception as e:
        print ('Open', fileName, 'failed :', e)
        return wordQueue, len(wordSet), configList
    for line in fi:
        line = line.split()
        if 0 == len(line):
            continue
        word = line[0]
        if word not in wordSet:
            wordQueue.put(word)
            wordSet[word] = 0
    return wordQueue, len(wordSet), configList

if '__main__' == __name__:
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
    
    wordQueue, wordNum, configList = createWordQueue(inFile, coding, 'webInfoChecker.conf')
    resultQueue = multiprocessing.Queue()
    statQueue = multiprocessing.Queue()
    resultVec = []
    wordHitSet = {}
    
    monitor = procMonitor(wordQueue, resultQueue, statQueue, processorNum, configList)
    monitor.start()
     
    for i in range(processorNum):
        checker = webInfoChecer(wordQueue, resultQueue, statQueue, i, configList)
        checker.start()

    fo = open(outFile, 'w', encoding = 'gb18030')
    while len(wordHitSet) < wordNum:
        res = resultQueue.get()
        wordHitSet[res[0]] = 0
        print (len(wordHitSet), res)
        flag = False
        for i in res[1]:
            if len(i) > 0:
                flag = True
                break
        if flag:
            fo.write(res[0] + ' ')
            for i in res[1]:
                if len(i) > 0:
                    fo.write(i + ' ')
                else:
                    fo.write('NULL ')
            fo.write('\n')
            fo.flush()