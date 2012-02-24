def viterbi_simple(line, strPriority, logP):
    resSet = []
    resSet.append(['',0])
    INF = len(line) * logP[0]
    for i in range(0,len(line)):
        if 0 == i:
            if (line[i]) not in strPriority:
                return line, 0
            resSet.append([line[i], logP[strPriority[line[i]]]])
        else:
            minStr = ''
            minP = INF
            for k in range(0, i + 1):
                j = i - k
                c = line[j:i+1]
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
            resSet.append([minStr, minP])                 
    return resSet[len(line)]

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

def baseSeg(line, pri, logP):
    line = line.split()
    lineRes = []
    for i in line:
        lastIdx = 0
        if ord(i[0]) < 0x4e00 or ord(i[0]) > 0x9fa5:
            charFlag = False
            alphaFlag = True
        else:
            charFlag = True
            alphaFlag = False     
        for j in range(0, len(i)):
            if ord(i[j]) < 0x4e00 or ord(i[j]) > 0x9fa5:
                if alphaFlag:
                    continue
                else:
                    lineRes.append(i[lastIdx:j])
                    charFlag = False
                    alphaFlag = True
                    lastIdx = j
            else:
                if charFlag:
                    continue
                else:
                    lineRes.append(i[lastIdx:j])
                    charFlag = True
                    alphaFlag = False
                    lastIdx = j
        lineRes.append(i[lastIdx:j + 1])       
    line = []
    for i in lineRes:
        if ord(i[0]) < 0x4e00 or ord(i[0]) > 0x9fa5:
            line.append(i)
        else:
            line.append(viterbi_simple(i, pri, logP)[0])
    res = []
    for i in line:
        j = i.split()
        for k in j:
            res.append(k)
    return res


pri, logP = giveTable('../../dataset/chinese.txt', '../../dataset/codebook.c')

fi = open('train.utf8', encoding = 'utf8')
fo = open('baseTest.utf8', 'w', encoding = 'utf8')
for line in fi:
    line = line.replace('\n', '')
    res = baseSeg(line, pri, logP)
    for i in res:
        fo.write(i + ' ')
    fo.write('\n')
    
