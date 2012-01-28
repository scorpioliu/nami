/*
ID: shanzho2
PROG: beads
LANG: C++
*/

#include <iostream>
#include <fstream>
#include <string>
#include <memory.h>
#include <cmath>

using namespace std;

int main(void)
{
    ifstream fin("beads.in");
    ofstream fout("beads.out");

    int n;
    string str;
    fin>>n>>str;

    str += str;
    int a, b, res, w;
    char flag;

    a = 1; b = res = w = 0;
    flag = str[0];
    if (str[0] == 'w')
    {
        w++;
    }

    for (int i = 1; i < str.length(); i++)
    {
        if (str[i] == 'w' || str[i] == flag)
        {
            a++;
        }
        else if (flag == 'w' && str[i] != 'w')
        {
            flag = str[i];
            a++;
        }
        else if (flag != 'w' && str[i] != flag)
        {
            flag = str[i];
            b = a - w;
            a = w + 1;
        }
        if (str[i] == 'w')
        {
            w++;
        }
        else
        {
            w = 0;
        }
        res = max(res, a+b);
    }
    if (res > n)
    {
        fout<<n<<endl;
    }
    else
    {
        fout<<res<<endl;
    }
    return 0;
}
