#include "digital.h"

int Canslove(std::vector<int> chess)
{
    int ni=0,w;
    for(int i=0;i<Digital_num;i++)
    {
        if(chess[i]==0){
            w = i;
            continue;
        }
        for(int j=i+1;j<Digital_num;j++)
        {
            if(chess[j] == 0)
                continue;
            if(chess[i]>chess[j])
                ni++;
        }
    }
//    int x=w/chess_size;
//    int y=w%chess_size;
//    ni+=abs(x-chess_size)+abs(y-chess_size);

    int y = w/chess_size;
    int k = abs(y-goal[0][0]);
    if(ni%2==k%2)
        return 1;
    else
        return 0;
}

int hv(std::vector<int> chess)
{
    int cost = 0;
    for(int i = 0;i < Digital_num;i++){
        int w = chess[i];
        int x = i / chess_size;
        int y = i % chess_size;
        cost += abs(x-goal[w][0]) + abs(y-goal[w][1]);
    }
    return cost;
}

void swap(int p1,int p2,std::vector<int>& chess)
{
    int tmp;
    tmp = chess[p1];
    chess[p1] = chess[p2];
    chess[p2] = tmp;
}

bool bfs(int sx,int sy,int len,int limit,std::vector<int>& path,std::vector<int>& chess)
{
    int nx,ny;
//    if(flag)
//        return;
    int dv=hv(chess);
    if(len == limit){
        if(dv == 0)
            return true;
        else
            return false;
    }
    else if(len < limit){
        if(dv == 0)
            return true;
    }
//    if(dv == 0)
//        return true;
//    if(len==limit)
//        return false;
    int pre_move;
    if(path.empty())
        pre_move = -1;
    else
        pre_move = path.back();
    for(int i=0;i<4;i++)
    {
        if(pre_move != -1 && i+pre_move==3 && len>0)
            continue;
        nx=sx+offset[i][0];
        ny=sy+offset[i][1];
        if(0<=nx&&nx<chess_size && 0<=ny&&ny<chess_size)
        {
            int p1 = nx * chess_size + ny;
            int p2 = sx * chess_size + sy;
            swap(p1,p2,chess);
            int p=hv(chess);
            if(p+len<=limit)
            {
                path.push_back(i);
                if(bfs(nx,ny,len+1,limit,path,chess))
                    return true;
                path.pop_back();
            }
            swap(p1,p2,chess);
        }
    }
    return false;
}
