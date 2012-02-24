#!/usr/bin/env python

'''
segmentScore.py : estimate segmentation performance.
Train set, test set and segment result are all files which are segmented.

@author: scorpioLiu, shanzhongdeyunqi@gmail.com, 2012.02.24
@version: 0.1
@license: MIT
@copyright: (c) 2012, Project Nami, Project Sanji
'''

import difflib
import sys

def getFMeasure(valPrecision, valRecall):
    try:
        F = 2 * (valPrecision * valRecall) / (valPrecision + valRecall)
    except Exception as e:
        print ('Err accurs in calculate F1 :', e)
        return 0
    return 2 * (valPrecision * valRecall) / (valPrecision + valRecall)

def checkChar(word):
    # if word has just one charactor, it is leagle
    for i in word:
        if ord(i[0]) >= 0x4e00 or ord(i[0]) <= 0x9fa5:
            return True            
    return False

def getDictSet(fileName, coding):
    dictSet = {}
    try:
        fi = open(fileName, encoding = coding)
    except Exception as e:
        print ('Err accurs in open', fileName, ':\n', e)
        return {}
    for line in fi:
        line = line.split()
        for i in line:
            if checkChar(i):
                dictSet[i] = 0
    fi.close()
    return dictSet

def getOOV(baseSet, testSet):
    if 0 == len(baseSet) and 0 == len(testSet):
        return 0
    if 0 == len(baseSet) and len(testSet) > 0:
        return 1
    cnt = 0
    for i in testSet:
        if i not in baseSet:
            cnt += 1
    return cnt/len(baseSet)

def getIV(baseSet, testSet):
    if 0 == len(baseSet):
        return 1
    cnt = 0
    for i in testSet:
        if i in baseSet:
            cnt += 1
    return cnt/len(baseSet)   

def getSegmentScore(resFileName, testFileName, trainFileName, coding):
    try:
        fiTest = open(testFileName, encoding = coding)
        fiRes  = open(resFileName, encoding = coding)
    except Exception as e:
        print ('Err accurs in open', testFileName, 'or', resFileName, ':\n', e)
        return []
    
    diff = difflib.Differ()
    
    totalUnit     = 0 # for G
    totalSen      = 0 # test sentence num
    totalRight    = 0 # for P on whole sentence
    testCount     = 0 # for R
    resCount      = 0 # for P
    resRightCount = 0 # for R and P
    
    for line in fiTest:
        testLine = line.split()
        resLine = fiRes.readline().split()
        # space line continue
        if 0 == len(testLine): 
            continue
        totalSen += 1
        for i in testLine:
            totalUnit += len(testLine)
        
        testCount += len(testLine)
        resCount += len(resLine)
        cmpRes = list(diff.compare(testLine, resLine))
        localRight = 0
        for i in cmpRes:
            if i[0] == ' ':
                localRight += 1
        if localRight == len(testLine):
            totalRight += 1
        resRightCount += localRight
        
    fiTest.close()
    fiRes.close()
    
    trainSet = getDictSet(trainFileName, coding)
    testSet = getDictSet(testFileName, coding)
    resSet = getDictSet(resFileName, coding)
    OOVSet = {}
    for i in testSet:
        if i not in trainSet:
            OOVSet[i] = 0

    originOOV = getOOV(trainSet, testSet)
    OOV = getOOV(trainSet, resSet)
    ROOV = getIV(OOVSet, resSet)
    RIV = getIV(testSet, resSet)
        
    report = []
    report.append(['Recall(R)', resRightCount/testCount])
    report.append(['Precision(P)', resRightCount/resCount])
    report.append(['F1-Score(F)', getFMeasure(resRightCount/testCount, resRightCount/resCount)])
    report.append(['Original OOV(OOV)', originOOV])
    report.append(['Test Words Recall(Riv)', RIV])
    report.append(['Test OOV Recall(Roov)', ROOV])
    report.append(['Segment Result OOV', OOV])
    report.append(['Test Sentence', totalSen])
    report.append(['Total Right Sentence', totalRight])
    report.append(['Total Sentence Precision', totalRight/totalSen])
    report.append(['Total lexicon', totalUnit])
    report.append(['Original Granularity', testCount/totalUnit])
    report.append(['Segment Granularity(G)', resCount/totalUnit])
    return report
    
def showScoreReport(report):
    if 0 == len(report):
        print ('No report showed.')
        return
    maxLen = 0
    for i in report:
        maxLen = max(maxLen, len(i[0]))

    for i in report:
        if 0 == i[1]%1:
            print (i[0].ljust(maxLen), ':', '%d'%i[1])
        else:
            print (i[0].ljust(maxLen), ':', '%.4f'%i[1])

if '__main__' == __name__:
    if len(sys.argv) < 4 or '--help' == sys.argv[1]:
        print ('Usage : segmenScore.py {result file} {test result file} {train file} {[opt] coding}')
        sys.exit(1)
    if len(sys.argv) == 5:
        coding = sys.argv[4]
    else:
        coding = 'utf8'
 
    showScoreReport(getSegmentScore(sys.argv[1], sys.argv[2], sys.argv[3], coding))
