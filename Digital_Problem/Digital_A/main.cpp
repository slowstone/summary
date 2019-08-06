#include <iostream>
#include <cmath>
using namespace std;

const int Digital_num = 16;
const int w_h_num = 4;

typedef struct Node
{//节点结构体
    int data[Digital_num];
	double f,g;
	struct Node * parent;
}Node,*Lnode;

typedef struct Stack
{//OPEN CLOSED 表结构体
	Node * npoint;
	struct Stack * next;
}Stack,* Lstack;

Node * Minf(Lstack * Open)
{//选取OPEN表上f值最小的节点，返回该节点地址
	Lstack temp = (*Open)->next,min = (*Open)->next,minp = (*Open);
	Node * minx;
    while(temp->next != NULL)
	{
		if((temp->next ->npoint->f) < (min->npoint->f))
		{
			min = temp->next;
			minp = temp;
		}
		temp = temp->next;
	}
	minx = min->npoint;
	temp = minp->next;
	minp->next = minp->next->next;
	free(temp);
	return minx;
}

int Canslove(Node * suc, Node * goal)
{//判断是否可解
	int a = 0,b = 0,i,j;
	for(i = 1; i< Digital_num;i++)
		for(j = 0;j < i;j++)
		{
			if((suc->data[i] > suc->data[j]) && suc->data[j] != 0)a++;
			if((goal->data[i] > goal->data[j]) && goal->data[j] != 0)b++;
		}
	if(a%2 == b%2)return 1;
	else return 0;
}

int Equal(Node * suc,Node * goal)
{//判断节点是否相等，相等，不相等
	for(int i = 0; i < Digital_num; i ++ )
		if(suc->data[i] != goal->data[i])return 0;
    return 1;
}

Node * Belong(Node * suc,Lstack * list)
{//判断节点是否属于OPEN表或CLOSED表，是则返回节点地址，否则返回空地址
	Lstack temp = (*list) -> next ;
	if(temp == NULL)return NULL;
	while(temp != NULL)
	{
		if(Equal(suc,temp->npoint))return temp -> npoint;
		temp = temp->next;
	}
	return NULL;
}

void Putinto(Node * suc,Lstack * list)
{//把节点放入OPEN 或CLOSED 表中
    Stack * temp;
	temp =(Stack *) malloc(sizeof(Stack));
	temp->npoint = suc;
	temp->next = (*list)->next;
	(*list)->next = temp;
}

///////////////计算f值部分-开始//////////////////////////////
double Fvalue(Node suc, Node goal, int m)
{//计算f值
	switch(m)
	{
	case 1:{
			int error(Node,Node);
			int w=0;
			w=error(suc,goal);
			return w+suc.g;

		   }
	case 2:{
			double Distance(Node,Node,int);
			double p = 0;
			for(int i = 1; i < Digital_num; i++)
				p = p + Distance(suc, goal, i);
			return p + suc.g; //f = h + g;

		   }
	default:
		break;
	}

}

int error(Node suc,Node goal)
{//计算错位个数
	int w,i;
	w=0;
	for(i=0;i<Digital_num;i++){
		if(suc.data[i]!=goal.data[i])
			w++;
	}
	return w;

}
double Distance(Node suc, Node goal, int i)
{//计算方格的错位距离
	int k,h1,h2;
	for(k = 0; k < Digital_num; k++)
	{
		if(suc.data[k] == i)h1 = k;
		if(goal.data[k] == i)h2 = k;
	}
	return double(fabs(h1/w_h_num - h2/w_h_num) + fabs(h1%w_h_num - h2%w_h_num));
}
///////////////计算f值部分-结束//////////////////////////////

///////////////////////扩展后继节点部分的函数-开始/////////////////
int BelongProgram(Lnode * suc ,Lstack * Open ,Lstack * Closed ,Node goal ,int m)
{//判断子节点是否属于OPEN或CLOSED表并作出相应的处理
	Node * temp = NULL;
	int flag = 0;
	if((Belong(*suc,Open) != NULL) || (Belong(*suc,Closed) != NULL))
	{
		if(Belong(*suc,Open) != NULL) temp = Belong(*suc,Open);
		else temp = Belong(*suc,Closed);
		if(((*suc)->g) < (temp->g))
		{
			temp->parent = (*suc)->parent;
			temp->g = (*suc)->g;
			temp->f = (*suc)->f;
		    flag = 1;
		}
	}
	else
	{
		Putinto(* suc, Open);
		(*suc)->f = Fvalue(**suc, goal, m);
	}
	return flag;
}

int Canspread(Node suc, int n)
{//判断空格可否向该方向移动，表示空格向上向下向左向右移
	int i,flag = 0;
	for(i = 0;i < Digital_num;i++)
		if(suc.data[i] == 0)break;
	switch(n)
	{
	case 1:
		if(i/w_h_num != 0)flag = 1;break;
	case 2:
		if(i/w_h_num != w_h_num-1)flag = 1;break;
	case 3:
		if(i%w_h_num != 0)flag = 1;break;
	case 4:
		if(i%w_h_num != w_h_num-1)flag = 1;break;
	default:break;
	}
	return flag ;
}

void Spreadchild(Node * child,int n)
{//扩展child节点的字节点n表示方向，，，表示空格向上向下向左向右移
	int i,loc,temp;
	for(i = 0;i < Digital_num;i++)
		child->data[i] = child->parent->data[i];
	for(i = 0;i < Digital_num;i++)
		if(child->data[i] == 0)break;
	if(n==0)
		loc = i%w_h_num+(i/w_h_num - 1)*w_h_num;
	else if(n==1)
		loc = i%w_h_num+(i/w_h_num + 1)*w_h_num;
	else if(n==2)
		loc = i%w_h_num-1+(i/w_h_num)*w_h_num;
	else
		loc = i%w_h_num+1+(i/w_h_num)*w_h_num;
	temp = child->data[loc];
	child->data[i] = temp;
	child->data[loc] = 0;
}

void Spread(Lnode * suc, Lstack * Open, Lstack * Closed, Node goal, int m)
{//扩展后继节点总函数
	int i;
	Node * child;
	for(i = 0; i < 4; i++)
	{
		if(Canspread(**suc, i+1))                               //判断某个方向上的子节点可否扩展
		{
				child = (Node *) malloc(sizeof(Node));          //扩展子节点
	            child->g = (*suc)->g +1;                        //算子节点的g值
	            child->parent = (*suc);                         //子节点父指针指向父节点
	            Spreadchild(child, i);                          //向该方向移动空格生成子节点
              	if(BelongProgram(&child, Open, Closed, goal, m)) //	判断子节点是否属于OPEN或CLOSED表并作出相应的处理
					free(child);
		}
	}
}
///////////////////////扩展后继节点部分的函数-结束//////////////////////////////////

Node * Process(Lnode * org, Lnode * goal, Lstack * Open, Lstack * Closed, int m)
{//总执行函数
	while(1)
	{
		if((*Open)->next == NULL)return NULL;                    //判断OPEN表是否为空，为空则失败退出
    	Node * minf = Minf(Open);                                //从OPEN表中取出f值最小的节点
		Putinto(minf, Closed);                                   //将节点放入CLOSED表中
    	if(Equal(minf, *goal))return minf;                       //如果当前节点是目标节点，则成功退出
        Spread(&minf, Open, Closed, **goal, m);                 //当前节点不是目标节点时扩展当前节点的后继节点
	}
}

int Shownum(Node * result)
{//递归显示从初始状态到达目标状态的移动方法
	if(result == NULL)return 0;
	else
	{
		int n = Shownum(result->parent);
		printf("第%d步：",n);
		for(int i = 0; i < w_h_num; i++)
			{
				printf("\n");
				for(int j = 0; j < w_h_num; j++)
				{
					if(result->data[i*w_h_num+j] != 0)
						printf(" %d ",result->data[i*w_h_num+j]);
					else printf(" 0 ");
				}
			}
		printf("\n");
		return n+1;
	}
}

bool Checkinput(Node *suc){
    char c;
    int i = 0;
    int pre_num = 0;
    bool flag[Digital_num] = {false};
    while(i < Digital_num){
        c = getchar();
        if(c >= '0' && c <= '9' && c < '0' + Digital_num){
            pre_num = pre_num*10 + c-'0';
        }
        else if(c == ' ' || c == '\n'){
            if(flag[pre_num]) {
                cout << "含有重复输入!\n";
                return false;
            }
            else{
                suc->data[i] = pre_num;
                flag[pre_num] = true;
                i++;
            }
            pre_num = 0;
        }
        else{
            cout << "非法输入\n";
            return false;
        }
    }
    return true;
}

int meassure(Lstack  s)
{
	int k=0;
	while((s->next)!=NULL)
	{
		k++;
		s=s->next;
	}
	return k;
}

int main()
{//主函数                                                             //初始操作，建立open和closed表
	Lstack Open = (Stack *) malloc(sizeof(Stack));
	Open->next = NULL;
	Lstack Closed = (Stack *) malloc(sizeof(Stack));
	Closed->next = NULL;
	Node * org = (Node *) malloc(sizeof(Node));
	org->parent = NULL;                                        //初始状态节点
	org->f =1;
	org->g =1;
    Node * goal = (Node *) malloc(sizeof(Node));               //目标状态节点
	Node * result;
	int m;
	int k;
    for(int i = 0;i < Digital_num;i++){
        goal->data[i] = (i+1) % Digital_num;
    }
	cout << "=================================\n";
	cout << "说明：状态矩阵由" << Digital_num;
    cout << "个数字表示.\n请依次按照行列顺序输入,每个数字间用空格隔开。\n";
    cout << "=================================\n";
	cout << "请输入初始状态,数字以空格隔开回车表示输入结束):\n";
	if(!Checkinput(org))
        return 0;
	if(Canslove(org, goal))
	{//A*算法开始，先将初始状态放入OPEN表
		 cout << "请选择：1.按w(n)搜索 2.按p(n)搜索 \n";
		 cin >> m;
		 cout << "搜索中，请耐心等待...\n";
	     Putinto(org,&Open);
       	 result = Process(&org, &goal, &Open, &Closed, m);  //进行剩余的操作
		 cout << "总步数:" << Shownum(result)-1 << endl;
		 k=meassure(Closed);
		 cout << "扩展节点数：" << k << endl;
	}
	else
		cout << "程序认定该起始状态无法道达目标状态!\n";
    return 0;
}