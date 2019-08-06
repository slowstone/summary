#include "RMS.h"

void RMS(vector<task>& task_vector, int start_t, int end_t){
    sort(task_vector.begin(),task_vector.end(),comparebyperiod);
    //printvector(task_vector);
    int cur_t = 0;
    task * cur_process = NULL;  //Store pointers to running processes
    bool flag = false;
    while(cur_t < end_t){
        //whether print
        if(cur_t >= start_t && cur_t <= end_t)
            flag = true;
        else
            flag = false;
        //print arrive info
        for(int i = 0;i < task_vector.size();i++){
            task &t = task_vector[i];
            if(t.arrival_time == cur_t){
                if(flag)
                    cout << cur_t << " p" << t.pid << " arrives" << endl;
            }
        }
        //whether cur_process end
        if(cur_process != NULL && cur_process->run_t == cur_process->CPU_burst){
            if(flag)
                cout << cur_t << " p" << cur_process->pid << " end" << endl;
            cur_process->arrival_time += cur_process->period;
            cur_process->deadline = cur_process->arrival_time + cur_process->period;
            cur_process->run_t = 0;
            cur_process->state = READY;
            cur_process = NULL;
            sort(task_vector.begin(),task_vector.end(),comparebyperiod);
        }
        //whether deadline miss
        for(int i = 0;i < task_vector.size();i++){
            task &t = task_vector[i];
            if(t.deadline < cur_t){
                if(t.state == READY){
                    t.arrival_time += t.period;
                    t.deadline = t.arrival_time + t.period;
                    t.state = READY;
                    t.run_t = 0;
                }
                if(t.state == RUNNING){
                    if(flag)
                        cout << cur_t << " p" << t.pid << " stop" << endl;
                    t.arrival_time += t.period;
                    t.deadline = t.arrival_time + t.period;
                    t.state = READY;
                    t.run_t = 0;
                    cur_process = NULL;
                }
                cout << cur_t << " p" << t.pid << " miss deadline" << endl;
                cout << "MISS DEADLINE, ALL END" << endl;
                exit(1);
            }
        }
        sort(task_vector.begin(),task_vector.end(),comparebyperiod);
        //whether cur_process change
        for(int i = 0;i < task_vector.size();i++){
            task &t = task_vector[i];
            if(cur_process == NULL){
                if(t.arrival_time <= cur_t && t.state == READY) {
                    cur_process = &t;
                    t.state = RUNNING;
                    if(flag)
                        cout << cur_t << " p" << cur_process->pid << " start" << endl;
                    break;
               }
            }
            else{
                if(cur_process->pid == t.pid)
                    break;
                if(t.arrival_time <= cur_t && t.state == READY) {
                    if(flag)
                        cout << cur_t << " p" << cur_process->pid << " stop" << endl;
                    cur_process->state = READY;
                    cur_process = &t;
                    t.state = RUNNING;
                    if(flag)
                        cout << cur_t << " p" << cur_process->pid << " start" << endl;
                    break;
                }
            }
        }
        //running process
        if(cur_process != NULL)
            cur_process->run_t++;
        //running time
        cur_t++;
        //printvector(task_vector);
    }
}