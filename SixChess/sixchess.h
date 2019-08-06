#ifndef SIXCHESS_H
#define SIXCHESS_H

#include <QApplication>
#include <QPushButton>
#include <queue>

// 记录下子次数
static int times;
// 是否第一次下子
static bool isFirst;

enum paint_char{black=1,white=2,empty=-1,nempty=-2,side=3,sum=3};
enum vertion{player,computer};

const int chessbored_size=17;//棋盘尺寸(15*15)
const int max2=2147483647,fen_max=99999999;
const int min2=-2147483647,fen_min=-99999999;
const int player_color=black;//玩家棋子颜色
const int computer_color=white; //电脑棋子颜色
const int wide=4,depth=6;//搜索的深度和广度

struct node
{
    int i,j;
    int value;
    int c[2][4];//各方向形成的连接的子数
    friend bool operator < (node a,node b)
    {
        return a.value<b.value;
    }
    friend bool operator > (node a,node b)
    {
        return a.value>b.value;
    }
} ;
struct sixnode
{
    int x1,y1,x2,y2;
};

extern QVector <QPushButton *> button_vec;
extern int chessbored[chessbored_size][chessbored_size];
extern QVector <node> empty_node;

int szfz(int a[chessbored_size][chessbored_size],int b[chessbored_size][chessbored_size]);
int near_num(int x,int y);//返回此点形成的最高连珠数
int empty_value_sub(node e,int a);//a表示视角是玩家还是电脑 ，空格评分函数。
int empty_value(node &e,int a);
int empty_value2(node &e,int a);//评分函数
int pingfen(int pc);//总评函数
void before_move(int x,int y);
void updata_empty_node(int x,int y);//更新棋子周围的空点
int myfen(int pc,int depth2,int jz);//我的分数
int youfen(int pc,int depth2,int jz);//你的分数 ,jz剪枝
sixnode get_bestnode(int pc);//得到最优点 ,pc表示以哪一方为自己
bool computer_move(int pc);
bool player_move(int x,int y);

#endif // SIXCHESS_H
