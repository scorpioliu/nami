// DengklekTryingToSleep.cpp
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

class DengklekTryingToSleep
{
    public:
    int minDucks(vector <int> d)
    {
        sort(d.begin(), d.end());
        return d[d.size() - 1] - d[0] + 1 - d.size();
    }
};

int main()
{
    return 0;
}
