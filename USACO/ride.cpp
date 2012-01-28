/*
ID: shanzho2
PROG: ride
LANG: C++
*/
#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int getNum(string str)
{
    int n = 1;
    for(int i = 0; i < str.length(); i++)
    {
        n *= (str[i] - 'A' + 1);
    }
    return n%47;
}


int main() {
    ofstream fout ("ride.out");
    ifstream fin ("ride.in");
    string str, name;
    int n, m;
    while(fin>>name>>str)
    {
        n = getNum(name);
        m = getNum(str);
        if (n == m)
        {
            fout<<"GO"<<endl;
        }
        else
        {
            fout<<"STAY"<<endl;
        }
    }
    return 0;
}
