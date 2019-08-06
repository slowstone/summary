#include "sixchess.h"

int szfz(int a[chessbored_size][chessbored_size],int b[chessbored_size][chessbored_size])
{
    int i,j;
    for(i=0;i<chessbored_size;i++)
        for(j=0;j<chessbored_size;j++)
            b[i][j]=a[i][j];
    return 0;
}

int near_num(int x,int y)//返回此点形成的最高连珠数
{
    int s,m,k,n=chessbored[x][y];
    s=1;
    for(k=1;k<6&&chessbored[x][y-k]==n;k++)s++;
    for(k=1;k<6&&chessbored[x][y+k]==n;k++)s++;
    m=s;
    s=1;
    for(k=1;k<6&&chessbored[x-k][y]==n;k++)s++;
    for(k=1;k<6&&chessbored[x+k][y]==n;k++)s++;
    if(s>m)m=s;
    s=1;
    for(k=1;k<6&&chessbored[x-k][y-k]==n;k++)s++;
    for(k=1;k<6&&chessbored[x+k][y+k]==n;k++)s++;
    if(s>m)m=s;
    s=1;
    for(k=1;k<6&&chessbored[x-k][y+k]==n;k++)s++;
    for(k=1;k<6&&chessbored[x+k][y-k]==n;k++)s++;
    if(s>m)m=s;
    return m;
}

int empty_value_sub(node e,int a)//a表示视角是玩家还是电脑 ，空格评分函数。
{
    int temp=chessbored[e.i][e.j];
    chessbored[e.i][e.j]=a;
    if(near_num(e.i,e.j)>5)
    {
        chessbored[e.i][e.j]=temp;
        return fen_max;
    }
    chessbored[e.i][e.j]=temp;
      int b=1,i,j,k,s=0,n,fa=black+white-a,b2=0;
      for(k=1;k<6;k++)
      {
            if(chessbored[e.i][e.j-k]==a)b*=4;
            else if(chessbored[e.i][e.j-k]<0)
            {
                b2++;
                if(b2>1)
                {
                    break;
                }
                b*=2;
            }
            else
                break;
      }
      b2=0;
      for(k=1;k<6;k++)
      {
            if(chessbored[e.i][e.j+k]==a)b*=4;
            else if(chessbored[e.i][e.j+k]<0)
            {
                b2++;
                if(b2>1)
                {
                    break;
                }
                b*=2;
            }
            else
                break;
      }
      n=0;
      for(k=1;k<6&&chessbored[e.i][e.j-k]!=fa&&chessbored[e.i][e.j-k]!=side;k++)
        n++;
      for(k=1;k<6&&chessbored[e.i][e.j+k]!=fa&&chessbored[e.i][e.j+k]!=side;k++)
        n++;
      if(n<5)b=0;
      if(n==5&&b==512)b=1024;
      s=s+b;

      b=1;b2=0;
      for(k=1;k<6;k++)
      {
            if(chessbored[e.i-k][e.j]==a)b*=4;
            else if(chessbored[e.i-k][e.j]<0)
            {
                b2++;
                if(b2>1)
                {
                    break;
                }
                b*=2;
            }
            else
                break;
      }
      b2=0;
      for(k=1;k<6;k++)
      {
            if(chessbored[e.i+k][e.j]==a)b*=4;
            else if(chessbored[e.i+k][e.j]<0)
            {
                b2++;
                if(b2>1)
                {
                    break;
                }
                b*=2;
            }
            else
                break;
      }
      n=0;
      for(k=1;k<6&&chessbored[e.i-k][e.j]!=fa&&chessbored[e.i-k][e.j]!=side;k++)
        n++;
      for(k=1;k<6&&chessbored[e.i+k][e.j]!=fa&&chessbored[e.i+k][e.j]!=side;k++)
        n++;
      if(n<5)b=0;
      if(n==5&&b==512)b=1024;
      s=s+b;

      b=1;b2=0;
      for(k=1;k<6;k++)
      {
            if(chessbored[e.i-k][e.j-k]==a)b*=4;
            else if(chessbored[e.i-k][e.j-k]<0)
            {
                b2++;
                if(b2>1)
                {
                    break;
                }
                b*=2;
            }
            else
                break;
      }
      b2=0;
      for(k=1;k<6;k++)
      {
            if(chessbored[e.i+k][e.j+k]==a)b*=4;
            else if(chessbored[e.i+k][e.j+k]<0)
            {
                b2++;
                if(b2>1)
                {
                    break;
                }
                b*=2;
            }
            else
                break;
      }
      n=0;
      for(k=1;k<6&&chessbored[e.i-k][e.j-k]!=fa&&chessbored[e.i-k][e.j-k]!=side;k++)
        n++;
      for(k=1;k<6&&chessbored[e.i+k][e.j+k]!=fa&&chessbored[e.i+k][e.j+k]!=side;k++)
        n++;
      if(n<5)b=0;
      if(n==5&&b==512)b=1024;
      s=s+b;

       b=1;b2=0;
      for(k=1;k<6;k++)
      {
            if(chessbored[e.i-k][e.j+k]==a)b*=4;
            else if(chessbored[e.i-k][e.j+k]<0)
            {
                b2++;
                if(b2>1)
                {
                    break;
                }
                b*=2;
            }
            else
                break;
      }
      b2=0;
      for(k=1;k<6;k++)
      {
            if(chessbored[e.i+k][e.j-k]==a)b*=4;
            else if(chessbored[e.i+k][e.j-k]<0)
            {
                b2++;
                if(b2>1)
                {
                    break;
                }
                b*=2;
            }
            else
                break;
      }
      n=0;
      for(k=1;k<6&&chessbored[e.i-k][e.j+k]!=fa&&chessbored[e.i-k][e.j+k]!=side;k++)
        n++;
      for(k=1;k<6&&chessbored[e.i+k][e.j-k]!=fa&&chessbored[e.i+k][e.j-k]!=side;k++)
        n++;
      if(n<5)b=0;
      if(n==5&&b==512)b=1024;
      s=s+b;

      return s;
}

int empty_value(node &e,int a)
{
    int my,you;
    my=empty_value_sub(e,a);
    you=empty_value_sub(e,player_color+computer_color-a);
    e.value=my+you;
    return my+you;
}
int empty_value2(node &e,int a)//评分函数
{
    int my,you;
    my=empty_value_sub(e,a);
    you=empty_value_sub(e,player_color+computer_color-a);
    e.value=my-you/2;
    return my-you/2;
}
int pingfen(int pc)//总评函数
{
    QVector<node>::iterator the_iterator;
    node e;
    int max3=fen_min;
    the_iterator = empty_node.begin();
    while( the_iterator != empty_node.end() )
    {
        e=*the_iterator;
        empty_value2(e,pc);
        if(e.value>max3)
            max3=e.value;
        the_iterator++;
   }
   return max3;
}

void before_move(int x,int y)
{
    if(chessbored[x][y]==nempty)
    {
        QVector<node>::iterator the_iterator;
        node e;
        the_iterator = empty_node.begin();
        while( the_iterator != empty_node.end() )
        {
            e=*the_iterator;
            if(e.i==x&&e.j==y)
            {
                empty_node.erase(the_iterator);
                break;
            }
            the_iterator++;
        }
    }
}

void updata_empty_node(int x,int y)//更新棋子周围的空点
{
    int i,j;
    for(i=-3;i<4;i++)
        for(j=-3;j<4;j++)
            if(x+i>0&&x+i<chessbored_size-1&&y+j>0&&y+j<chessbored_size-1&&chessbored[x+i][y+j]==empty)
            {
                node e;
                e.i=x+i;
                e.j=y+j;
                empty_node.push_back(e);
                //cout<<e.i<<" "<<e.j<<endl;
                chessbored[x+i][y+j]=nempty;
            }
}

int myfen(int pc,int depth2,int jz)//我的分数
{
    if(depth2>=depth)
    {
        int a=pingfen(pc);
        return a;
    }
    int fa=player_color+computer_color-pc,c;
    int n=empty_node.size();
    int i,j;
    QVector<node> en;
    en=empty_node;
    node e,e2;
    std::priority_queue< node ,QVector<node> ,std::less<node> >  pen;
    for(i=0;i<n;i++)
    {
        e=en.back();
        en.pop_back();
        empty_value(e,pc);
        pen.push(e);
    }
    int max_value=min2;
    int wide2=wide;
    if(wide2>n)wide2=n;
    node te[50];
    for(i=0;i<wide2;i++)
    {
        te[i]=pen.top();
        pen.pop();
    }
    sixnode se[20];
    int secnt=0;
    for(i=0;i<wide2;i++)
        for(j=i+1;j<wide2;j++)
        {
            se[secnt].x1=te[i].i;
            se[secnt].y1=te[i].j;
            se[secnt].x2=te[j].i;
            se[secnt].y2=te[j].j;
            secnt++;
        }
    int chessbored2[chessbored_size][chessbored_size];
    szfz(chessbored,chessbored2);
    for(i=0;i<secnt;i++)
    {
        QVector<node> empty_node2;
        empty_node2=empty_node;
        before_move(se[i].x1,se[i].y1);
        before_move(se[i].x2,se[i].y2);
        chessbored[se[i].x1][se[i].y1]=pc;
        chessbored[se[i].x2][se[i].y2]=pc;
        if(near_num(se[i].x1,se[i].y1)>5)
        {
            empty_node=empty_node2;
            szfz(chessbored2,chessbored);
            return fen_max;
        }
        if(near_num(se[i].x2,se[i].y2)>5)
        {
            empty_node=empty_node2;
            szfz(chessbored2,chessbored);
            return fen_max;
        }
        updata_empty_node(se[i].x1,se[i].y1);
        updata_empty_node(se[i].x2,se[i].y2);
        int fenshu;
        fenshu=youfen(pc,depth2+1,max_value);
        if(fenshu>max_value)
        {
            max_value=fenshu;
        }
        empty_node=empty_node2;
        szfz(chessbored2,chessbored);
    }
    return max_value;
}

int youfen(int pc,int depth2,int jz)//你的分数 ,jz剪枝
{
    int fa=player_color+computer_color-pc;
    int n=empty_node.size();
    int i,j;
    QVector<node> en;
    en=empty_node;
    node e;
    std::priority_queue< node ,QVector<node> ,std::less<node> >  pen;
    for(i=0;i<n;i++)
    {
        e=en.back();
        en.pop_back();
        empty_value(e,fa);
        pen.push(e);
    }
    int min_value=max2;
    int wide2=wide;
    if(wide2>n)wide2=n;
    node te[50];
    for(i=0;i<wide2;i++)
    {
        te[i]=pen.top();
        pen.pop();
    }
    sixnode se[20];
    int secnt=0;
    for(i=0;i<wide2;i++)
        for(j=i+1;j<wide2;j++)
        {
            se[secnt].x1=te[i].i;
            se[secnt].y1=te[i].j;
            se[secnt].x2=te[j].i;
            se[secnt].y2=te[j].j;
            secnt++;
        }
    int chessbored2[chessbored_size][chessbored_size];
    szfz(chessbored,chessbored2);
    for(i=0;i<secnt;i++)
    {
        QVector<node> empty_node2;
        empty_node2=empty_node;
        before_move(se[i].x1,se[i].y1);
        before_move(se[i].x2,se[i].y2);
        chessbored[se[i].x1][se[i].y1]=fa;
        chessbored[se[i].x2][se[i].y2]=fa;
        if(near_num(se[i].x1,se[i].y1)>5)
        {
            empty_node=empty_node2;
            szfz(chessbored2,chessbored);
            return fen_min;
        }
        if(near_num(se[i].x2,se[i].y2)>5)
        {
            empty_node=empty_node2;
            szfz(chessbored2,chessbored);
            return fen_min;
        }
        updata_empty_node(se[i].x1,se[i].y1);
        updata_empty_node(se[i].x2,se[i].y2);
        int fenshu;
        fenshu=myfen(pc,depth2+1,min_value);
        if(fenshu<min_value)
        {
            min_value=fenshu;
        }
        empty_node=empty_node2;
        szfz(chessbored2,chessbored);
    }
    return min_value;
}

sixnode get_bestnode(int pc)//得到最优点 ,pc表示以哪一方为自己
{
    int n=empty_node.size();
    int i,j,i2;
    QVector<node> en;
    en=empty_node;
    node e;
    std::priority_queue< node ,QVector<node> ,std::less<node> >  pen;
    for(i=0;i<n;i++)
    {
        e=en.back();
        en.pop_back();
        empty_value(e,pc);
        pen.push(e);
    }
    int max_value=min2;
    int wide2=wide;
    if(wide2>n)wide2=n;
    node te[50];
    for(i=0;i<wide2;i++)
    {
        te[i]=pen.top();
        pen.pop();
    }
    sixnode se[20];
    int secnt=0;
    for(i=0;i<wide2;i++)
        for(j=i+1;j<wide2;j++)
        {
            se[secnt].x1=te[i].i;
            se[secnt].y1=te[i].j;
            se[secnt].x2=te[j].i;
            se[secnt].y2=te[j].j;
            secnt++;
        }
    int chessbored2[chessbored_size][chessbored_size];
    szfz(chessbored,chessbored2);
    for(i=0;i<secnt;i++)
    {
        QVector<node> empty_node2;
        empty_node2=empty_node;
        before_move(se[i].x1,se[i].y1);
        before_move(se[i].x2,se[i].y2);
        chessbored[se[i].x1][se[i].y1]=pc;
        chessbored[se[i].x2][se[i].y2]=pc;
        if(near_num(se[i].x1,se[i].y1)>5)
        {
            empty_node=empty_node2;
            szfz(chessbored2,chessbored);
            return se[i];
        }
        if(near_num(se[i].x2,se[i].y2)>5)
        {
            empty_node=empty_node2;
            szfz(chessbored2,chessbored);
            return se[i];
        }
        updata_empty_node(se[i].x1,se[i].y1);
        updata_empty_node(se[i].x2,se[i].y2);
        int fenshu;
        fenshu=youfen(pc,1,max_value);
        if(fenshu>max_value)
        {
            i2=i;
            max_value=fenshu;
        }
        empty_node=empty_node2;
        szfz(chessbored2,chessbored);
    }
    return se[i2];
}

bool computer_move(int pc)
{
    sixnode se;
    se=get_bestnode(pc);
    before_move(se.x1,se.y1);
    before_move(se.x2,se.y2);
    chessbored[se.x1][se.y1]=pc;
    chessbored[se.x2][se.y2]=pc;
    int index1 = (se.x1 - 1) * (chessbored_size - 2) + (se.y1 - 1);
    int index2 = (se.x2 - 1) * (chessbored_size - 2) + (se.y2 - 1);
    QPushButton *btn1 = button_vec[index1];
    QPushButton *btn2 = button_vec[index2];
    if(computer_color == black){        //Black
        btn1->setStyleSheet("border-image: url(:/imsrc/src/Black.png);");
        btn2->setStyleSheet("border-image: url(:/imsrc/src/Black.png);");
    }
    else{               //White
        btn1->setStyleSheet("border-image: url(:/imsrc/src/White.png);");
        btn2->setStyleSheet("border-image: url(:/imsrc/src/White.png);");
    }
    if(near_num(se.x1,se.y1)>5)
        return true;
    if(near_num(se.x2,se.y2)>5)
        return true;
    updata_empty_node(se.x1,se.y1);
    updata_empty_node(se.x2,se.y2);
    return false;
}

bool player_move(int x, int y){
    before_move(x,y);
    chessbored[x][y] = player_color;
    if(near_num(x,y)>5)
        return true;
    updata_empty_node(x,y);
    return false;
}
