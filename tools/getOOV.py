fi = open('pku_test_gold.utf8', encoding = 'utf8')
dict = {}
print ('herer')
for line in fi:
    try:
        line = line.split()
    except:
        continue
    for i in line:
        dict[i] = 0
print (len(dict))
fo = open('test_words.txt', 'w', encoding = 'utf8')
for i in dict:
    if len(i) <= 1:
        continue
    try:
        fo.write(i + '\n')
    except:
        pass