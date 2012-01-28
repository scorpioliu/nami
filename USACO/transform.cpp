/*
ID: shanzho2
PROG: transform
LANG: C++
*/

#include <iostream>
#include <fstream>
#include <string>
#include <memory.h>
#include <cmath>
#include <vector>

using namespace std;

bool check1(vector<string>& vec1, vector<string>& vec2)
{
    for (int i = 0; i != vec1.size(); i++)
    {
        for (int j = 0; j != vec1.size(); j++)
        {
            if (vec1[i][j] != vec2[j][vec2.size() - 1 - i])
            {
                return false;
            }
        }
    }
    return true;
}

bool check2(vector<string>& vec1, vector<string>& vec2)
{
    for (int i = 0; i != vec1.size(); i++)
    {
        for (int j = 0; j != vec1.size(); j++)
        {
            if (vec1[i][j] != vec2[vec1.size() - 1 - i][vec1.size() - 1 - j])
            {
                return false;
            }
        }
    }
    return true;
}

bool check3(vector<string>& vec1, vector<string>& vec2)
{
    for (int i = 0; i != vec1.size(); i++)
    {
        for (int j = 0; j != vec1.size(); j++)
        {
            if (vec1[i][j] != vec2[j][i])
            {
                return false;
            }
        }
    }
    return true;
}
bool check4(vector<string>& vec1, vector<string>& vec2)
{
    for (int i = 0; i != vec1.size(); i++)
    {
        for (int j = 0; j != vec1.size(); j++)
        {
            if (vec1[i][j] != vec2[i][vec1.size() - 1 - j])
            {
                return false;
            }
        }
    }
    return true;
}

bool check5(vector<string>& vec1, vector<string>& vec2)
{
    vector<string>temp = vec2;

    for (int i = 0; i != vec1.size(); i++)
    {
        for (int j = 0; j != vec1.size(); j++)
        {
            temp[i][j] = vec1[i][vec1.size() - 1 - j];
        }
    }

    if (check1(temp, vec2)) return true;
    if (check2(temp, vec2)) return true;
    if (check3(temp, vec2)) return true;
    return false;
}

bool check6(vector<string>& vec1, vector<string>& vec2)
{
    for (int i = 0; i != vec1.size(); i++)
    {
        for (int j = 0; j != vec1.size(); j++)
        {
            if (vec1[i][j] != vec2[i][j])
            {
                return false;
            }
        }
    }
    return true;
}

int check(vector<string>& vec1, vector<string>& vec2)
{
    int res = 7;
    if (check1(vec1, vec2)) return 1;
    if (check2(vec1, vec2)) return 2;
    if (check3(vec1, vec2)) return 3;
    if (check4(vec1, vec2)) return 4;
    if (check5(vec1, vec2)) return 5;
    if (check6(vec1, vec2)) return 6;
    return res;
}

int main(void)
{
    ifstream fin("transform.in");
    ofstream fout("transform.out");

    int n;
    string str;
    fin>>n;
    vector<string>vec1, vec2;
    vec1.resize(n);
    vec2.resize(n);
    for (int i = 0; i != n; i++)
    {
        fin>>vec1[i];
    }

    for (int i = 0; i != n; i++)
    {
        fin>>vec2[i];
    }

    fout<<check(vec1, vec2)<<endl;
    //cout<<check(vec1, vec2)<<endl;
    return 0;
}
