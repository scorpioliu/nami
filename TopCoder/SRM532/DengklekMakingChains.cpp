// DengklekMakingChains.cpp
//

#include <vector>
#include <list>
#include <map>
#include <set>
#include <deque>
#include <queue>
#include <stack>
#include <bitset>
#include <string>
#include <algorithm>
#include <functional>
#include <numeric>
#include <utility>

#include <sstream>
#include <fstream>
#include <iostream>
#include <iomanip>

#include <cstdio>
#include <cstdlib>
#include <cctype>
#include <cstring>
#include <cmath>
#include <ctime>

using namespace std;

//BEGINTEMPLATE_BY_SCORPIOLIU
//ENDEMPLATE_BY_SCORPIOLIU

class DengklekMakingChains
{
    public:
    int maxBeauty(vector <string> c)
    {
        int res = 0;
        int head = 0;
        int tail = 0;
        int temp, temp1 = 0;
        int middle = 0;
        for (int i = 0; i != c.size(); i++)
        {
            if (notRusty(c[i]))
            {
                temp1 += getVal(c[i]);
                continue;
            }
            temp = getMid(c[i]);
            if (temp > middle)
            {
                middle = temp;
            }
        }
        for (int i = 0; i != c.size(); i++)
        {
            for (int j = 0; j != c.size(); j++)
            {
                if (i == j)
                {
                    res = max(res, temp1 + max(getHead(c[i]), getTail(c[j])));
                }
                else
                {
                    res = max(res, temp1 + getHead(c[i]) + getTail(c[j]));
                }
            }
        }
        if (middle > res + head + tail)
        {
            return middle;
        }
        else
            return res + head + tail;
    }
    bool notRusty(string c)
    {
        for (int i = 0; i != c.length(); i++)
        {
            if (c[i] == '.')
            {
                return false;
            }
        }
        return true;
    }
    int getVal(string c)
    {
        int res = 0;
        stringstream ss;
        int temp;
        for (int i = 0; i != c.length(); i++)
        {
            ss.clear();
            ss<<c[i];
            ss>>temp;
            res += temp;
        }
        return res;
    }
    int getHead(string c)
    {
        if (notRusty(c))
            return 0;
        int res = 0;
        stringstream ss;
        int temp;
        for (int i = 0; i != c.length(); i++)
        {
            if (c[i] == '.')
            {
                break;
            }
            ss.clear();
            ss<<c[i];
            ss>>temp;
            res += temp;
        }
        return res;
    }
    int getMid(string c)
    {
        int res = 0;
        stringstream ss;
        if (c[0] == '.' && c[2] == '.')
        {
            ss<<c[1];
            ss>>res;
        }
        return res;
    }
    int getTail(string c)
    {
        if (notRusty(c))
            return 0;
        int res = 0;
        stringstream ss;
        int temp;
        for (int i = c.length() - 1; i >= 0; i--)
        {
            if (c[i] == '.')
            {
                break;
            }
            ss.clear();
            ss<<c[i];
            ss>>temp;
            res += temp;
        }
        return res;
    }
};

int main()
{
    string str[11] = {"412", "..7", ".58", "7.8", "32.", "6..", "351", "3.9", "985", "...", ".46"};
    vector<string>vec;
    for (int  i = 0; i != 11; i++)
    {
        vec.push_back(str[i]);
    }
    DengklekMakingChains a;
    cout<<a.maxBeauty(vec)<<endl;
    return 0;
}
