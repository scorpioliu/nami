fi = open('train.gb', encoding = 'gb18030')
fo = open('ICTCLASRes.utf8', 'w', encoding = 'utf8')

for line in fi:
    line = line.split()
    for i in line:
        idx = i.rfind('/')
        fo.write(i[0:idx] + ' ')
    fo.write('\n')