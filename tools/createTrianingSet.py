#!/usr/bin/env python

'''
createTrainingSet.py : create training set for all segmentation

@author: scorpioLiu, shanzhongdeyunqi@gmail.com, 2012.02.24
@version: 0.1
@license: MIT
@copyright: (c) 2012, Project Nami, Project Sanji
'''

import sys

class trainingSetCreator(object):    
    def __init__(self, inFileName, outFileName1,  outFileName2, testFileName, coding, cutNum, segType):
        self.inFileName = inFileName
        self.outFileName1 = outFileName1
        self.outFileName2 = outFileName2
        self.testFileName = testFileName
        self.coding = coding
        self.segType = segType
        self.cutNum = cutNum
        self.OOVSet = {}
        
    def getOOVSet(self):
        OOVSet = {}
        if '' == self.testFileName:
            return {}
        trainSet = {}
        try: 
            fi = open(self.inFileName, encoding = self.coding)
        except Exception as e:
            print ('Err exists in open :', self.inFileName)
            return {}
        # Create training dict
        cnt = 1
        for line in fi:
            if 0 != self.cutNum and cnt > self.cutNum:
                break
            cnt += 1 
            line = line.split()
            for i in line:
                trainSet[i] = 0
        fi.close()
        # Create oov words set
        try:
            fi = open(self.testFileName, encoding = self.coding)
        except Exception as e:
            print ('Err exists in open :', self.testFileName)
            return {}    
        for line in fi:
            line = line.split()
            for i in line:
                if i not in trainSet and len(i) > 1:
                    OOVSet[i] = 0
        fi.close()
        return OOVSet
   
    def createSetForCRF(self):
        try:
            fi = open(self.inFileName, encoding = self.coding)
        except Exception as e:
            print ('Err accurs in open', self.inFileName, ':\n', e)
            return
        
        fo = open(self.outFileName1, 'w', encoding = self.coding)
        cnt = 1
        for line in fi:
            if 0 != self.cutNum and cnt > self.cutNum:
                break
            cnt += 1 
            line = line.split()
            for i in line:
                if len(i) == 1:
                    fo.write('%s\tS\n'%i)
                    continue
                for j in range(len(i)):
                    if j == 0:
                        fo.write('%s\tB\n'%i[j])
                    elif j == len(i) - 1:
                        fo.write('%s\tE\n'%i[j])
                    elif j == 1:
                        fo.write('%s\tC\n'%i[j])
                    elif j == 2:
                        fo.write('%s\tD\n'%i[j])
                    else:
                        fo.write('%s\tM\n'%i[j])
            fo.write('\n')
        fi.close()
        fo.close()
        print(self.outFileName1, 'created.')
        
        self.OOVSet = self.getOOVSet()
        if 0 == len(self.OOVSet):
            return
        
        fi = open(self.inFileName, encoding = self.coding)
        fo = open(self.outFileName2, 'w', encoding = self.coding)
        cnt = 1
        for line in fi:
            if 0 != self.cutNum and cnt > self.cutNum:
                break
            cnt += 1 
            line = line.split()
            for i in line:
                if len(i) == 1:
                    fo.write('%s\tS\n'%i)
                    continue
                for j in range(len(i)):
                    if j == 0:
                        fo.write('%s\tB\n'%i[j])
                    elif j == len(i) - 1:
                        fo.write('%s\tE\n'%i[j])
                    elif j == 1:
                        fo.write('%s\tC\n'%i[j])
                    elif j == 2:
                        fo.write('%s\tD\n'%i[j])
                    else:
                        fo.write('%s\tM\n'%i[j])
            fo.write('\n')
        fi.close()
        for i in self.OOVSet:
            for j in range(len(i)):
                if j == 0:
                    fo.write('%s\tB\n'%i[j])
                elif j == len(i) - 1:
                    fo.write('%s\tE\n'%i[j])
                elif j == 1:
                    fo.write('%s\tC\n'%i[j])
                elif j == 2:
                    fo.write('%s\tD\n'%i[j])
                else:
                    fo.write('%s\tM\n'%i[j])
            fo.write('\n')
        fo.close()
        print(self.outFileName2, 'created.')
        
    def createSetForNormal(self):
        return 0

    def setCreator(self):
        creator = {'CRF++':self.createSetForCRF}
        creator.get(self.segType, self.createSetForNormal)()
        
def main(argv):
    if len(argv) < 2 or '--help' == argv[1]:
        print ('Usage : createTraining.py {--in input file name}\n', 
               '{--out1 out file name without test words under cut num lines}\n', 
               '{--out2 out file name with test words under cut num lines}\n', 
               '{--cut cut number}\n', 
               '{--type segmentor type}\n', 
               '{--coding encoding style}\n',
               '{--test test answer file}')
        return 1
    
    outFileName1 = ''
    outFileName2 = ''
    testFileName = ''
    inFileName = ''
    segType = 'CRF++'
    coding = 'utf8'
    cutNum = 0
    for i in range(1, len(argv)):
        if 1 == i%2:
            if '--' != argv[i][0:2]:
                print ('command format wrong in :', arg[i])
                return 1
            try:
                if 'out1' == argv[i][2:]:
                    outFileName1 = argv[i + 1]
                elif 'out2' == argv[i][2:]:
                    outFileName2 = argv[i + 1]
                elif 'type' == argv[i][2:]:
                    segType = argv[i + 1]
                elif 'cut' == argv[i][2:]:
                    cutNum = int(argv[i + 1])
                elif 'coding' == argv[i][2:]:
                    coding = argv[i + 1]
                elif 'test' == argv[i][2:]:
                    testFileName = argv[i + 1]
                elif 'in' == argv[i][2:]:
                    inFileName = argv[i + 1]
                else:
                    continue
            except Exception as e:
                print ('Err exists in command :', e)
                continue
        else:
            continue
        
    creator = trainingSetCreator(inFileName, outFileName1, outFileName2, testFileName, coding, cutNum, segType)
    creator.setCreator()
    return 0

if '__main__' == __name__:
    sys.exit(main(sys.argv))

