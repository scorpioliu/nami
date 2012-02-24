#!/usr/bin/env python

'''
giveCRFRes.py : give sigment result from CRF result.

CRF format must be:
char B/C/D/E/M/S/etc...
B is begin of a word
C is second char of a word
D is third char of a word
M is other word which is not end
E is end char of a word
S is a single char and also a word

@author: scorpioLiu, shanzhongdeyunqi@gmail.com, 2012.02.20
@version: 0.1
@license: MIT
@copyright: (c) 2012, Project Nami
'''

import sys

def giveCRFRes(inFile, outFile, coding):
    try:
        fi = open(inFile, encoding = coding)
    except Exception as e:
        print ('Err accurs in open', inFile, ':\n', e)
        return 
    fo = open(outFile, 'w', encoding  = coding)
    res = ''
    for line in fi:
        i = line.split()
        if len(i) == 0:
            if len(res) > 0:
                if res[-1] == ' ':
                    res = res[0:-1]
                fo.write(res + '\n')
                res = ''
            else:
                fo.write('\n')
        elif i[-1] == 'S' or i[-1] == 'E':
            res = res + i[0] + ' '
        else:
            res += i[0]
        print (res)
    if len(res) > 0 and res[-1] == ' ':
        res = res[0:-1]
    fo.write(res + '\n')
    print ('Format CRF Result done.')

if '__main__' == __name__:
    if len(sys.argv) < 2:
        print ('Usage : giveCRFRes.py {CRF result file} {segment result file} {[opt] coding}')
        sys.exit(1)
    if len(sys.argv) == 4:
        coding = sys.argv[3] 
    else:
        coding = 'utf8'
    giveCRFRes(sys.argv[1], sys.argv[2], coding)
