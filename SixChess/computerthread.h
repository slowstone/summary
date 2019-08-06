#ifndef COMPUTERTHREAD_H
#define COMPUTERTHREAD_H

#include <QThread>
#include "sixchess.h"

class ComputerThread : public QThread
{
    Q_OBJECT

public:
    ComputerThread() : QThread(){};
protected:
    virtual void run(){
        sixnode se;
        se=get_bestnode(computer_color);
        before_move(se.x1,se.y1);
        before_move(se.x2,se.y2);
        chessbored[se.x1][se.y1]=computer_color;
        chessbored[se.x2][se.y2]=computer_color;
        int index1 = (se.x1 - 1) * (chessbored_size - 2) + (se.y1 - 1);
        int index2 = (se.x2 - 1) * (chessbored_size - 2) + (se.y2 - 1);
        if(near_num(se.x1,se.y1)>5){
            emit threadend(true,index1,index2);
        }
        else if(near_num(se.x2,se.y2)>5){
            emit threadend(true,index1,index2);
        }
        else{
            updata_empty_node(se.x1,se.y1);
            updata_empty_node(se.x2,se.y2);
            emit threadend(false,index1,index2);
        }
    }
signals:
    void threadend(bool iswin,int index1,int index2);
};

#endif // COMPUTERTHREAD_H
