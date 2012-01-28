/*
ID: shanzho2
PROG: friday
LANG: C++
*/

#include <iostream>
#include <fstream>
#include <string>
#include <memory.h>

using namespace std;

int days[2][12] = {31,28,31,30,31,30,31,31,30,31,30,31,
31,29,31,30,31,30,31,31,30,31,30,31};

int p[7] = {0};

int checkYear(int n)
{
    if (n % 4 == 0 && n % 100 != 0 || n % 400 == 0)
    {
        return 1;
    }
    else
    {
        return 0;
    }
}

void giveP(int n)
{
    int k = 1900;
    int t = 0;
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < 12; j++)
        {
            p[(t+13)%7] ++;
            t += days[checkYear(k+i)][j];
        }
    }
}



int main() {
    ofstream fout ("friday.out");
    ifstream fin ("friday.in");

    int n;
    fin>>n;

    memset(p, 0, 7*sizeof(int));
    giveP(n);

    for (int i = 6; i < 12; i++)
    {
        fout<<p[i%7]<<" ";
    }
    fout<<p[5]<<endl;

    return 0;
}
