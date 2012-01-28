/*
ID: shanzho2
PROG: barn1
LANG: C++
*/

#include <iostream>
#include <fstream>
#include <string>
#include <memory.h>
#include <cmath>
#include <vector>
#include <algorithm>

using namespace std;

int main(void)
{
    ifstream fin("barn1.in");
    ofstream fout("barn1.out");

    int m, s, c;
    fin>>m>>s>>c;
    int res = c;

    vector<int>temp, vec;
    temp.resize(c);
    for (int i = 0; i != c; i++)
    {
        fin>>temp[i];
    }
    sort(temp.begin(), temp.end());

    int cnt = 1;
    for (int i = 1; i < temp.size(); i++)
    {
        if (temp[i] - temp[i-1] > 1)
        {
            vec.push_back(temp[i] - temp[i-1] - 1);
            cnt++;
        }
    }
    sort(vec.begin(), vec.end());

    for (int i = 0; i < cnt - m; i++)
    {
        res += vec[i];
    }


    fout<<res<<endl;
    return 0;
}
