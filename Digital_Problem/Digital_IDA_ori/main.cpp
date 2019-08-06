#include<stdio.h>
#include<string.h>
#include<cmath>

#define size 4

int move[4][2]={{-1,0},{0,-1},{0,1},{1,0}};
char op[4]={'U','L','R','D'};
int map[size][size],map2[size*size],limit,path[100];
int flag,length;
int goal[16][2]= {{3,3},{0,0},{0,1}, {0,2},{0,3}, {1,0},
                  {1,1}, {1,2}, {1,3},{2,0}, {2,1}, {2,2},{2,3},{3,0},{3,1},{3,2}};
int nixu(int a[size*size])
{
    int i,j,ni,w,x,y;  
    ni=0;
    for(i=0;i<size*size;i++)  
    {
        if(a[i]==0) 
            w=i;
        for(j=i+1;j<size*size;j++){
            if(a[i]>a[j])
                ni++;
        }
    }
    x=w/size;
    y=w%size;
    ni+=std::abs(x-3)+std::abs(y-3);
    if(ni%2==1)
        return 1;
    else
        return 0;
}

int hv(int a[][size])
{
    int i,j,cost=0;
    for(i=0;i<size;i++)
    {
        for(j=0;j<size;j++)
        {
            int w=map[i][j];
            cost+=std::abs(i-goal[w][0])+std::abs(j-goal[w][1]);
        }
    }
    return cost;
}

void swap(int*a,int*b)
{
    int tmp;
    tmp=*a;
    *a=*b;
    *b=tmp;
}
void dfs(int sx,int sy,int len,int pre_move)
{
    int i,nx,ny;
    if(flag)
        return;
    int dv=hv(map);
    if(len==limit)
    {
        if(dv==0)  
        {
            flag=1;
            length=len;
            return;
        }
        else
            return;  
    }
    else if(len<limit)
    {
        if(dv==0)  
        {
            flag=1;
            length=len;
            return;
        }
    }
    for(i=0;i<4;i++)
    {
        if(i+pre_move==3&&len>0)
            continue;
        nx=sx+move[i][0];  
        ny=sy+move[i][1];
        if(0<=nx&&nx<size && 0<=ny&&ny<size) 
        {
            swap(&map[sx][sy],&map[nx][ny]);
            int p=hv(map);  
            if(p+len<=limit&&!flag) 
            {
                path[len]=i;
                dfs(nx,ny,len+1,i);  
                if(flag)
                    return;
            }
            swap(&map[sx][sy],&map[nx][ny]);  
        }
    }
}
int main()
{
    int i,j,k,l,m,n,sx,sy;
    char c,g;
    i=0;
    printf("How many test：\n");
    scanf("%d",&n);
    while(n--)
    {   printf("Inputs：\n");
        flag=0,length=0;
        memset(path,-1,sizeof(path));  
        for(i=0;i<16;i++) 
        {
            scanf("%d",&map2[i]);
            if(map2[i]==0)
            {
                map[i/size][i%size]=0;
                sx=i/size;sy=i%size;
            }
            else
            {
                map[i/size][i%size]=map2[i];
            }

        }


        if(nixu(map2)==1)                
        {
            limit=hv(map); 
            while(!flag&&length<=50)
            {
                printf("%d\n",limit);
                dfs(sx,sy,0,0);
                if(!flag)
                    limit++; 
            }
            if(flag)
            {
                for(i=0;i<length;i++)
                    printf("%c",op[path[i]]); 
                printf("\n");
            }
        }
        else if(!nixu(map2)||!flag)
            printf("This puzzle is not solvable.\n");
    }
    return 0;
}