#include "utils.h"
#include <fstream>


void readfromfile(string filename, vector<task> &task_vec, int &start_t, int &end_t){
    ifstream f(filename);
    if(!f.is_open()){
        cout << "Error opening file" << endl;
        exit(1);
    }
    bool flag = true;
    while(!f.eof()){
        string ss;
        getline(f,ss);
        if(ss.size() == 0 || ss[0] == '#')
            continue;
        vector<string> ss_vec = SplitString(ss," ");
        if(flag){
            start_t = stoi(ss_vec[0]);
            end_t = stoi(ss_vec[1]);
            flag = false;
        }
        else{
            task t;
            t.pid = stoi(ss_vec[0]);
            t.arrival_time = stoi(ss_vec[1]);
            t.CPU_burst = stoi(ss_vec[2]);
            t.deadline = stoi(ss_vec[3]);
            t.period = stoi(ss_vec[4]);
            t.state = READY;
            t.run_t = 0;
            task_vec.push_back(t);
        }
    }
}

void printvector(vector<task> task_vec){
    cout << setw(15) << "pid"
         << setw(15) << "arrival_time"
         << setw(15) << "CPU_burst"
         << setw(15) << "deadline"
         << setw(15) << "period"
         << setw(15) << "STATE"
         << setw(15) << "run_time"
         << endl;
    for(auto t:task_vec){
        cout << setw(15) << t.pid
             << setw(15) << t.arrival_time
             << setw(15) << t.CPU_burst
             << setw(15) << t.deadline
             << setw(15) << t.period;
        switch(t.state){
            case READY:
                cout << setw(15) << "READY";
                break;
            case RUNNING:
                cout << setw(15) << "RUNNING";
            default:
                break;
        }
        cout << setw(15) << t.run_t << endl;
    }
}

bool comparebyperiod(task a, task b){
    if(a.period < b.period)
        return true;
    else if(a.period == b.period){
        if(a.pid < b.pid)
            return true;
    }
    return false;
}

bool comparebydeadline(task a, task b){
    if(a.deadline < b.deadline)
        return true;
    else if(a.deadline == b.deadline){
        if(a.pid < b.pid)
            return true;
    }
    return false;
}

vector<string> SplitString(const string& s, const string& c) {
    string::size_type pos1, pos2;
    vector<string> v;
    pos2 = s.find(c);
    pos1 = 0;
    while(string::npos != pos2)
    {
        v.push_back(s.substr(pos1, pos2-pos1));

        pos1 = pos2 + c.size();
        pos2 = s.find(c, pos1);
    }
    if(pos1 != s.length())
        v.push_back(s.substr(pos1));
    return v;
}