# createTestSetCRF.py
# Create test set for CRF

# Just split all the item in test, each item takes one line
# The end of each event takes one space line

# by scorpioLiu
# 2012.02.21

import sys
code = 'utf8'

if __name__ == "__main__": 
    if len(sys.argv) < 3 or '--help' == sys.argv[1]:
        print ('Usage : python3 ' + sys.argv[0] + ' {input test file} {output test file} {opt : sign}\n')
    else:
        fi = open(sys.argv[1], encoding = code)
        fo = open(sys.argv[2], 'w', encoding = code)
        
        if len(sys.argv) >= 3:
            sign = sys.argv[3]
        else:
            sign  = ''
        
        for line in fi:
            line = line.replace('\n', '')
            line = line.replace('\r', '')
            if 0 == len(line):
                print ('Hello')
                continue
            for i in line:
                if '' == sign:
                    fo.write(i + '\n')
                else:
                    fo.write(i + ' ' + sign + '\n')
            fo.write('\n')
        
        print ('Create test set for CRF done.\n')