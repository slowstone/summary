#ifndef COMPUTERTHREAD_H
#define COMPUTERTHREAD_H

#include <QThread>
#include "digital.h"

class ComputerThread : public QThread
{
    Q_OBJECT

private:
    int limit = 0;
    std::vector<int> ori_chess;
    std::vector<int> chess;
    std::vector<int> path;
    int sx;
    int sy;
public:
    ComputerThread(int limit,
                   std::vector<int> chess,
                   int sx,int sy) : QThread(){
        this->limit = limit;
        this->ori_chess = ori_chess;
        this->chess = chess;
        this->sx = sx;
        this->sy = sy;
        while(!this->path.empty()){
            this->path.pop_back();
        }
    }
protected:
    virtual void run(){
        while(!bfs(sx,sy,0,limit,path,chess)){
            limit ++;
        }
        emit threadend(path);
    }
signals:
    void threadend(std::vector<int> path);
};

#endif // COMPUTERTHREAD_H
