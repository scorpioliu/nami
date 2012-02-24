#!/usr/bin/env python

'''
getWordFreq.py : Get the frequency of each word in the list from Baidu.

@author: scorpioLiu, shanzhongdeyunqi@gmail.com, 2012.02.21
@version: 0.1
@license: MIT
@copyright: (c) 2012, Project Nami
'''

import time
import sys
import os
import random
import httplib2

url_fm = 'inputT=%d'
h = httplib2.Http(".cache")

if len(sys.argv) < 3:
    print ('Usage : ' + sys.argv[0] + ' {word list file} {word freq file}\n')
    sys.exit(1)

wordFile = sys.argv[1]
freqFile = sys.argv[2]
try:
    fi = open(wordFile, 'r')
except Exception as e:
    print (e)
    sys.exit(1)

wordSet = {}

def process(s, val):
    t = s.decode('gb18030')
    i = t.find('style="margin-left:120px">') + 33
    j = i + t[i:].find('</span>') - 1
    w = t[i:j]
    w = w.replace(',', '')
    print (w)
    wordSet[val] = int(w)
    return t[j:]

def process_content(str, val):
    t = str
    s = process(t, val)

for i in fi:
    retry_cnt = 0
    i = i.replace('\n', '')
    i = i.split()
    print('Hello')
    try:
        print (i[0])
    except:
        break
    sucess = False
    while not sucess:
        try:
            response, content = h.request('http://www.baidu.com/s?wd=' + '%22' + i[0] + '%22&' + (url_fm % int(500*random.random()+4000)))
            process_content(content, i[0])
            sucess = True
        except Exception:
            retry_cnt += 1
            if retry_cnt <= 3:
                print("error, failed %s, retry" % i[0])
                continue
            else:
                print("giveup.. %s" % i)
                break
    time.sleep(1*random.random()+2)
fi.close()

wordVec = []
for i in wordSet:
    wordVec.append([i, wordSet[i]])
wordVec.sort(key=lambda wordVec:wordVec[1], reverse=True)
fo = open(freqFile, 'w')
for i in wordVec:
    fo.write(i[0] + ' ' + str(i[1]) + '\n')
fo.close()

os.system('del .cache /q/f')
os.system('rd .cache /q/s')
print ('Cal word frequency done.\n')