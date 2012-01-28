/*
ID: shanzho2
PROG: milk
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

int main(void)
{
    ifstream fin("milk.in");
    ofstream fout("milk.out");
    int n, m, p, a;
    fin>>n>>m;

    vector<pair<int, int> >vec;
    while(m--)
    {
        fin>>p>>a;
        vec.push_back(make_pair(p, a));
    }

    sort(vec.begin(), vec.end());
    int res = 0;
    for (int i = 0; i != vec.size() && n > 0; i++)
    {
        cout<<vec[i].first<<endl;
        if (n >= vec[i].second)
        {
            res += (vec [i].first*vec[i].second);
            n -= vec[i].second;
        }
        else
        {
            res += (vec[i].first*n);
            n = 0;
        }
    }
    fout<<res<<endl;
    return 0;
}
