import sys

fi = open('pku_training.utf8', encoding = 'utf8')
fo = open('pku_training_crf.utf8', 'w', encoding = 'utf8')

for l in fi:
    it = l.split()
    for i in range(len(it)):
        ww = it[i].split('/')[0]
        for j in range(len(ww)):
            if len(ww) == 1:
                fo.write('%s\tS\n'%ww[j])
                break
            elif j == 0:
                fo.write('%s\tB\n'%ww[j])
            elif j == len(ww) - 1:
                fo.write('%s\tE\n'%ww[j])
            elif j == 1:
                fo.write('%s\tC\n'%ww[j])
            elif j == 2:
                fo.write('%s\tD\n'%ww[j])
            else:
                fo.write('%s\tM\n'%ww[j])
    fo.write('\n')
fi.close()
fo.close()
