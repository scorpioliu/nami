/*
ID: shanzho2
PROG: milk2
LANG: C++
*/

#include <iostream>
#include <fstream>
#include <string>
#include <memory.h>
#include <cmath>
#include <algorithm>
#include <vector>

using namespace std;

int main(void)
{
    ifstream fin("milk2.in");
    ofstream fout("milk2.out");

    int n, b, e;
    vector<pair<int, int> >r, t;
    fin>>n;
    while(n--)
    {
        fin>>b>>e;
        r.push_back(make_pair(b, e));
    }
    sort(r.begin(), r.end());

    t.push_back(r[0]);
    int idx = 0;
    for (int i = 1; i != r.size(); i++)
    {
        if (r[i].first <= t[idx].second)
        {
            if (r[i].second>t[idx].second)
            {
                t[idx].second = r[i].second;
            }
        }
        else
        {
            idx++;
            t.push_back(r[i]);
        }
    }

    int res1, res2;
    res1 = t[0].second - t[0].first;
    res2 = 0;
    for (int i = 1; i != t.size(); i++)
    {
        res1 = max(t[i].second - t[i].first, res1);
        res2 = max(t[i].first - t[i-1].second, res2);
    }
    fout<<res1<<" "<<res2<<endl;
    return 0;
}
