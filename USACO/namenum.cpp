/*
ID: shanzho2
PROG: namenum
LANG: C++
*/

#include <iostream>
#include <fstream>
#include <string>
#include <memory.h>
#include <cmath>
#include <vector>

using namespace std;

/*
2: A,B,C     5: J,K,L    8: T,U,V
3: D,E,F     6: M,N,O    9: W,X,Y
4: G,H,I     7: P,R,S
*/

bool check(string str, string n)
{
    if (str.length() != n.length())
    {
        return false;
    }
    if (str.find("Z") != string::npos || str.find("Q") != string::npos)
    {
        return false;
    }

    string name = "";
    for (int i = 0; i < str.length(); i++)
    {
        if (str[i] == 'A' || str[i] == 'B' || str[i] == 'C')
            name += "2";
        if (str[i] == 'D' || str[i] == 'E' || str[i] == 'F')
            name += "3";
        if (str[i] == 'G' || str[i] == 'H' || str[i] == 'I')
            name += "4";
        if (str[i] == 'J' || str[i] == 'K' || str[i] == 'L')
            name += "5";
        if (str[i] == 'M' || str[i] == 'N' || str[i] == 'O')
            name += "6";
        if (str[i] == 'P' || str[i] == 'R' || str[i] == 'S')
            name += "7";
        if (str[i] == 'T' || str[i] == 'U' || str[i] == 'V')
            name += "8";
        if (str[i] == 'W' || str[i] == 'X' || str[i] == 'Y')
            name += "9";
    }
    if (name == n)
        return true;
    else
        return false;
}

int main(void)
{
    ifstream fin("namenum.in");
    ofstream fout("namenum.out");

    string n;
    fin>>n;
    fin.clear();
    fin.close();
    fin.open("dict.txt");

    string str;
    int cnt = 0;
    while(fin>>str)
    {
        if (check(str, n))
        {
            fout<<str<<endl;
            cnt ++;
        }
    }
    if (cnt == 0)
    {
        fout<<"NONE"<<endl;
    }

    return 0;
}
