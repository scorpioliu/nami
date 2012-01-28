/*
ID: shanzho2
PROG: gift1
LANG: C++
*/

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>

using namespace std;

int main() {
    ofstream fout ("gift1.out");
    ifstream fin ("gift1.in");

    int n, t, m;
    string str;
    fin>>n;
    m = n;
    map<string, int>tree;
    map<string, int>::iterator it, it2;
    vector<string>vec;
    while(m--)
    {
        fin>>str;
        tree.insert(make_pair(str, 0));
        vec.push_back(str);
    }

    string name;
    while(n--)
    {
        fin>>name;
        it = tree.find(name);
        fin>>t>>m;
        if (m == 0)
        {
            continue;
        }
        t = t/m;

        while(m--)
        {
            fin>>name;
            it->second -= t;
            it2 = tree.find(name);
            it2->second += t;
        }
    }

    for(int i = 0; i != vec.size(); i++)
    {
        fout<<vec[i]<<" ";
        it = tree.find(vec[i]);
        fout<<it->second<<endl;
    }

    return 0;
}
