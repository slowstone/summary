#ifndef DIGITAL_H
#define DIGITAL_H

#include <vector>
#include <string>
#include <algorithm>
#include <chrono>
#include <random>

const int Digital_num = 16;
const int chess_size = 4;

const int goal[16][2] = {
    {3,3},{0,0},{0,1},{0,2},
    {0,3},{1,0},{1,1},{1,2},
    {1,3},{2,0},{2,1},{2,2},
    {2,3},{3,0},{3,1},{3,2}
};
const int offset[4][2]={{-1,0},{0,-1},{0,1},{1,0}};
//const std::string direction[4] = {"↑","←","→","↓"};
const std::string direction[4] = {"↓","→","←","↑"};

int Canslove(std::vector<int> chess);
int hv(std::vector<int> chess);
void swap(int p1,int p2,std::vector<int>& chess);
bool bfs(int sx,int sy,int len,int limit,std::vector<int>& path,std::vector<int>& chess);

#endif // DIGITAL_H
