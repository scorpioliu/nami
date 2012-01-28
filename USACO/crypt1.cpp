/*
ID: shanzho2
PROG: crypt1
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

bool num[10] = {false};

static bool check(int k, int n)
{
    int temp  = k;
    int temp2 = n;
    while (--n)
    {
        if (num[k % 10] == false)
            return false;
        k /= 10;
    }
    // Note that k > 10 must before num[k] == false
    if (k > 10 || num[k] == false)
        return false;
    return true;
}

int main(void)
{
    ifstream fin("crypt1.in");
    ofstream fout("crypt1.out");

    int n;
    fin>>n;
    vector<int>vec;
    vec.resize(n);
    for (int i = 0; i != n; i++)
    {
        fin>>vec[i];
        num[vec[i]] = true;
    }

    int res = 0;
    for (int x = 0; x != n; x++)
    for (int y = 0; y != n; y++)
    for (int z = 0; z != n; z++)
    for (int i = 0; i != n; i++)
    for (int j = 0; j != n; j++)
    {
        int temp = vec[x] * 100 + vec[y] * 10 + vec[z];
        int first = temp * vec[j];
        int second = temp * vec[i];
        int third = first + second * 10;
        if (check(first, 3) && check(second, 3) && check(third, 4))
            res++;
    }

    fout<<res<<endl;
    return 0;
}
