#!/usr/bin/env python3

'''
createCRFSet.py : Create training set and test set for CRF++ and
get segment result from CRF++ result.

Usage : python3 createCRFSet.py {in file} {out file} {test/traning/result}

NOTE : PLEASE USE IT IN LINUX BEACAUSE THAT \n IN WINDOWS IS \r\n
utf-8 file used.

Label Standard is six types such as S, B, C, D, M, E.
B is begin of a word
C is second char of a word
D is third char of a word
M is other word which is not end
E is end char of a word
S is a single char and also a word

@author: scorpioLiu, hongjun.liu@cootek.cn, 2012.03.14
@version: 0.1
@copyright: (c) 2012, Project Sanji, Project Nami
'''

import sys

def isNeedSplit(word):
	# Five type word need not to split to keep its completeness
	# Please see Segment Standard in documnet
	
	if 1 == len(word):
		return True
		
	alphaFlag = False
	digitFlag = False
	dotFlag = False
	atFlag = False
	urlFlag = False
	otherFlag = False
	for i in range(len(word)):
		if ord(word[i]) >= 0x4e00 and ord(word[i]) <= 0x9fa5:
			return True
		if word[i].isdigit():
			digitFlag = True
			continue
		if word[i] >= 'A' and word[i] <= 'Z':
			alphaFlag = True
			continue
		if word[i] >= 'a' and word[i] <= 'z':
			alphaFlag = True
			continue
		if '\'' == word[i] and 0 != i and len(word) - 1 != i:
			alphaFlag = True
			continue
		# dot at the begining ot end of a sentence is not email address or file name
		if '.' == word[i] and 0 != i and len(word) - 1 != i: 
			dotFlag = True
			continue
		# @ at the begining of a sentence is not email address
		if '@' == word[i] and 0 != i and len(word) - 1 != i: 
			atFlag = True
			continue
		if ':' == word[i] and 0 != i and len(word) - 1 != i:
			urlFlag = True
			continue
		if '/' == word[i] and 0 != i and len(word) - 1 != i:
			urlFlag = True
			continue
		otherFlag = True

	# Type 0 and 1 : IPv4 address and pure digit
	if not alphaFlag and digitFlag and not atFlag and not urlFlag and not otherFlag:
		res = word.split('.')
		if len(res) < 3:
			return False # pure digit
		elif 4 == len(res):
			for k in res:
				if len(k) < 1:
					return True
				if int(k) > 255 or int(k) < 0:
					return True
			return False # pure IPv4 address
		else:
			return True
	# Type 2 : pure English word
	if alphaFlag and not digitFlag and not dotFlag and not atFlag and not urlFlag and not otherFlag:
		return False
	# Type 3 : email address
	if atFlag and not otherFlag:
		if not dotFlag:
			return True
		if not alphaFlag and not digitFlag:
			return True
		return False
	# Type 4 : URL address or file name
	if not atFlag and not otherFlag:
		if not dotFlag:
			return True
		if digitFlag or alphaFlag:
			return False
	return True

def isAlphaOrDigit(c):
	if c.isdigit():
		return True
	if c >= 'A' and c <= 'Z':
		return True
	if c >= 'a' and c <= 'z':
		return True
	return False
	
def isLeagelStr(c):
	if isAlphaOrDigit(c):
		return True
	if '\'' == c or '@' == c or '.' == c or ':' == c or '/' == c:
		return True
	return False
	
def createTrainingSet(inFile, outFile, coding):
	try:
		fi = open(inFile, encoding = coding)
		fo = open(outFile, 'w', encoding = coding)
	except Exception as e:
		print (e)
		return 

	for line in fi:
		# NOTE : SPACE IN LINE WILL BE IGNORED
		line = line.split()
		if 0 == len(line):
			continue
		for i in line:
			if len(i) == 1:
				fo.write('%s\tS\n'%i)
				continue
			if not isNeedSplit(i):
				fo.write('%s\tS\n'%i)
				continue
			word = []
			content = ''
			for j in range(len(i)):
				if isAlphaOrDigit(i[j]):
					content += i[j]
					continue
				else:
					if '' != content:
						word.append(content)
					content = ''
					word.append(i[j])
			if '' != content:
				word.append(content)

			for j in range(len(word)):
				if j == 0:
					fo.write('%s\tB\n'%word[j])
				elif j == len(word) - 1:
					fo.write('%s\tE\n'%word[j])
				elif j == 1:
					fo.write('%s\tC\n'%word[j])
				elif j == 2:
					fo.write('%s\tD\n'%word[j])
				else:
					fo.write('%s\tM\n'%word[j])
		fo.write('\n')		
	fi.close()
	fo.close()

def splitContent(content):
	# content has no space
	res = []
	if not isNeedSplit(content):
		res.append(content)
	else:
		subContent = ''
		for j in content:
			if isAlphaOrDigit(j):
				subContent += j
				continue
			else:
				if '' != subContent:
					res.append(subContent)
					subContent = ''
				res.append(j)
		if '' != subContent:
			res.append(subContent)
			subContent = ''
	return res
	
	
def createTestSet(inFile, outFile, coding):
	try:
		fi = open(inFile, encoding = coding)
		fo = open(outFile, 'w', encoding = coding)
	except Exception as e:
		print (e)
		return
		
	for line in fi:
		# erase \r\n or \n
		line = line.replace('\n', '')
		line = line.replace('\r', '')
		# ignore space line
		if 0 == len(line): 
			continue
		content = ''
		for i in line:
			if ' ' == i:
				# clear content I
				if '' != content:
					subContent = splitContent(content)
					for j in subContent:
						fo.write(j + '\n')
					content = ''
				continue # ignore origin space
			if isLeagelStr(i):
				content += i
				continue
			# clear content II
			if '' != content:
				subContent = splitContent(content)
				for j in subContent:
					fo.write(j + '\n')
				content = ''
			fo.write(i + '\n')
		# clear content III
		if '' != content:
			subContent = splitContent(content)
			for j in subContent:
				fo.write(j + '\n')
			content = ''	
		fo.write('\n')
	fi.close()
	fo.close()
		
def getSegRes(inFile, outFile, coding):
	try:
		fi = open(inFile, encoding = coding)
		fo = open(outFile, 'w', encoding = coding)
	except Exception as e:
		print (e)
		return
	
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
	if len(res) > 0 and res[-1] == ' ':
		res = res[0:-1]
		fo.write(res + '\n')
	fi.close()
	fo.close()


def main():
	if len(sys.argv) < 4 or '--help' == sys.argv[1]:
		print ('Usage : python3', sys.argv[0], '{in file} {out file} {test/traning/result}')
		sys.exit(1)
	
	inFile = sys.argv[1]
	outFile = sys.argv[2]
	flag = sys.argv[3].upper() 
	if 'TEST' == flag:	
		createTestSet(inFile, outFile, 'utf8')
	elif 'TRAINING' == flag:
		createTrainingSet(inFile, outFile, 'utf8')
	elif 'RESULT' == flag:
		getSegRes(inFile, outFile, 'utf8')
	else:
		print(sys.argv[3], 'is illeagel.')
		sys.exit(1)
	
if '__main__' == __name__:
	main()