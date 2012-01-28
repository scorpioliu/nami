/*
ID: shanzho2
PROG: palsquare
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
    ifstream fin("palsquare.in");
    ofstream fout("palsquare.out");

    int n;
    string str1, str2, res;
    fin>>n;

    for (int i = 1; i <= 300; i++)
    {
        str1 = giveNum(i*i, n);
        str2 = str1;
        reverse(str1.begin(), str1.end());
        if (str1 == str2)
        {
            res = giveNum(i, n);
            fout<<res<<" "<<str2<<endl;
        }
    }
    return 0;
}
