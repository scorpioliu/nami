# givePinyin.py
# Give pinyin automatically using simple viterbi

# by scorpioliu
# 2012.01.31

def viterbi_simple(str, strPriority, logP):
    resSet = []
    resSet.append(['',0])
    INF = len(str) * logP[0]
    for i in range(0,len(str)):
        if 0 == i:
            if (str[i]) not in strPriority:
                return str, 0
            resSet.append([str[i], logP[strPriority[str[i]]]])
        else:
            minStr = ''
            minP = INF
            for k in range(0, i + 1):
                j = i - k
                c = str[j:i+1]
                if c not in strPriority:
                    continue
                else:
                    cP = logP[strPriority[c]]
                    preStr, preP = resSet[j]
                    if minP >= cP + preP:
                        minP = cP + preP
                        if '' == preStr:
                            minStr = c
                        else:
                            minStr = preStr + ' ' + c
                    #print (cP, preP, minP, preStr, c, minStr)
            resSet.append([minStr, minP])                 
    return resSet[len(str)]

def giveTable(wordFile, logFile):
    fi = open(wordFile, encoding = 'gb18030')
    strPriority = {}
    logP = []
    pinyinTable = {}
    for line in fi:
        line = line.split()
        freq = int(line[-1])
        word = line[-2]
        pinyin = ''
        for i in range(0, len(line) - 2):
            pinyin = pinyin + '\'' + line[i]
        if word not in strPriority:
            strPriority[word] = freq
            pinyinTable[word] = pinyin
        else:
            if strPriority[word] < freq:
                strPriority[word] = freq
                pinyinTable[word] = pinyin
    fi.close()
    fi = open(logFile, encoding = 'utf8')
    for line in fi:
        line = line.split(',')
        logP.append(int(line[0]))
    fi.close()
    return strPriority, logP, pinyinTable

def givePinyin(str, pinyinTable):
    str = str.split()
    if 0 == len(str):
        return ''
    pinyin = ''
    for phrase in str:
        pinyin += pinyinTable[phrase]
    return pinyin

pri, logP, pinyinTable = giveTable('../../dataset/chinese.txt', '../../dataset/codebook.c')
fi = open('../../dataset/testset.txt', encoding = 'gb18030')
for line in fi:    
    str = line.split()[0]
    res = viterbi_simple(str, pri, logP)
    pinyin = givePinyin(res[0], pinyinTable)
    print (pinyin, res[0])
