#include "utils.h"
#include "RMS.h"
#include "EDF.h"

int main(int argc, char* argv[]){
    if(argc != 3){
        cout << "Input error" << endl;
        return 0;
    }
    string select(argv[1]);
    string filename(argv[2]);
//    string select = "edf";
//    string filename = "data.txt";
//    cout << select << " " << filename << endl;
    vector<task> task_vec;
    int start_t,end_t;
    readfromfile(filename,task_vec,start_t,end_t);
//    printvector(task_vec);
    if(select == "rms"){
        RMS(task_vec,start_t,end_t);
    }
    else if(select == "edf"){
        EDF(task_vec,start_t,end_t);
    }
    else{
        cout << "Input error" << endl;
    }
    return 0;
}

