#ifndef SCHEDULE_UTILS_H
#define SCHEDULE_UTILS_H

#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <iomanip>
using namespace std;

enum STATE{READY,RUNNING};

typedef struct Task{
    int pid;
    int arrival_time;
    int CPU_burst;
    int deadline;
    int period;
    STATE state;
    int run_t;
}task;

void readfromfile(string filename, vector<task> &task_vec, int &start_t, int &end_t);
void printvector(vector<task> task_vec);
bool comparebyperiod(task a, task b);
bool comparebydeadline(task a, task b);
vector<string> SplitString(const string& s, const string& c);
#endif //SCHEDULE_UTILS_H
