/*
ID: shanzho2
PROG: dualpal
LANG: C++
*/

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <memory.h>
#include <cmath>
#include <vector>
#include <algorithm>

using namespace std;

string table = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";

string giveNum(int num, const int n)
{
    string res = "";
    while(num > 0)
    {
        res += table[num%n];
        num /= n;
    }
    reverse(res.begin(), res.end());
    return res;
}

int main(void)
{
    ifstream fin("dualpal.in");
    ofstream fout("dualpal.out");

    int n, s;
    string str1, str2;
    fin>>n>>s;

    while(n>0)
    {
        s++;
        int cnt = 0;
        for (int i = 2; i <= 10 && cnt < 2; i++)
        {
            str1 = giveNum(s, i);
            str2 = str1;
            reverse(str2.begin(), str2.end());
            if (str1 == str2)
            {
                cnt++;
            }
        }
        if (cnt >= 2)
        {
            fout<<s<<endl;
            n--;
        }
    }
    return 0;
}
