# viterbi_simple.py
# simple viterbi is only for HMM without hidden node.

# by scorpioLiu
# 2012.01.29

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
                            minStr = preStr + '+' + c
                    print (cP, preP, minP, preStr, c, minStr)
            resSet.append([minStr, minP])                 
    return resSet[len(str)]

def giveTable(wordFile, logFile):
    fi = open(wordFile, encoding = 'gb18030')
    strPriority = {}
    logP = []
    for line in fi:
        line = line.split()
        if line[-2] not in strPriority:
            strPriority[line[-2]] = int(line[-1])
    fi.close()
    fi = open(logFile, encoding = 'utf8')
    for line in fi:
        line = line.split(',')
        logP.append(int(line[0]))
    fi.close()
    return strPriority, logP

pri, logP = giveTable('../../dataset/chinese.txt', '../../dataset/codebook.c')
fi = open('../../dataset/testset.txt', encoding = 'gb18030')
str = fi.readline()
res = viterbi_simple(str, pri, logP)
print (res)




