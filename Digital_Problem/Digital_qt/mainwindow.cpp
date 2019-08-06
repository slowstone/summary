#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "digital.h"
#include "computerthread.h"

std::vector<int> ori_chess(Digital_num,0);
std::vector<int> chess(Digital_num,0);
std::vector<int> path;
int sx,sy;

std::vector<QFrame*> place;
std::vector<QLabel*> text;
std::vector<QString> frame_name;

bool solved_flag = false;
bool answer_flag = false;

bool flag = true;

void swap_pixmap(int z,int g){
    QPixmap gp = *text[g]->pixmap();
    text[z]->setPixmap(gp);
    text[g]->clear();
}

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    this->move(100,100);
    ui->answer->setAlignment(Qt::AlignCenter);
    ui->answer->setText("QLabel#answer{font: 15pt;color: black}");
    ui->solve_label->setAlignment(Qt::AlignCenter);
    ui->solve_label->setStyleSheet("QLabel#solve_label{font: 20pt;color: red}");
    ui->solve_label->setText("Instruction");
    ui->answer->setWordWrap(true);
    ui->answer->setText("Random: Random the chess\n"
                        "Compute: If can solve, Compute the answer\n"
                        "Show: If can solve, Show the answer\n"
                        "Commit: Commit your own chess");
    ui->centralWidget->setToolTip("十五数码问题");
    ui->chess->setStyleSheet("QFrame#chess{border:1px solid black;}");
    place.push_back(ui->place_01);frame_name.push_back("01");text.push_back(ui->text_01);
    place.push_back(ui->place_02);frame_name.push_back("02");text.push_back(ui->text_02);
    place.push_back(ui->place_03);frame_name.push_back("03");text.push_back(ui->text_03);
    place.push_back(ui->place_04);frame_name.push_back("04");text.push_back(ui->text_04);
    place.push_back(ui->place_05);frame_name.push_back("05");text.push_back(ui->text_05);
    place.push_back(ui->place_06);frame_name.push_back("06");text.push_back(ui->text_06);
    place.push_back(ui->place_07);frame_name.push_back("07");text.push_back(ui->text_07);
    place.push_back(ui->place_08);frame_name.push_back("08");text.push_back(ui->text_08);
    place.push_back(ui->place_09);frame_name.push_back("09");text.push_back(ui->text_09);
    place.push_back(ui->place_10);frame_name.push_back("10");text.push_back(ui->text_10);
    place.push_back(ui->place_11);frame_name.push_back("11");text.push_back(ui->text_11);
    place.push_back(ui->place_12);frame_name.push_back("12");text.push_back(ui->text_12);
    place.push_back(ui->place_13);frame_name.push_back("13");text.push_back(ui->text_13);
    place.push_back(ui->place_14);frame_name.push_back("14");text.push_back(ui->text_14);
    place.push_back(ui->place_15);frame_name.push_back("15");text.push_back(ui->text_15);
    place.push_back(ui->place_16);frame_name.push_back("16");text.push_back(ui->text_16);
    for(int i = 0;i < Digital_num;i++){
        ori_chess[i] = (i+1)%Digital_num;
    }
    while(!path.empty()){
        path.pop_back();
    }
    for(int i = 0;i < Digital_num;i++){
//        QString ss = "QFrame#place_" + frame_name[i] + "{border-image: url(:/imsrc/src/"+QString::number(i)+".png)}";
        QString ss = "QFrame#place_" + frame_name[i] + "{border:1px solid black;}";
        place[i]->setStyleSheet(ss);

        text[i]->setScaledContents(true);
        if(ori_chess[i]!=0){
            ss = ":/imsrc/src/" + QString::number(ori_chess[i]) + ".png";
            text[i]->setPixmap(QPixmap(ss));
        }
        else{
            text[i]->clear();
        }
    }
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_random_clicked()
{
    ui->answer->clear();
    unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
    std::shuffle(ori_chess.begin(),ori_chess.end(),std::default_random_engine(seed));
    solved_flag = Canslove(ori_chess);
    if(solved_flag){
        ui->solve_label->setText("Can Solve");
    }
    else{
        ui->solve_label->setText("Can't Solve");
    }
    while(!path.empty()){
        path.pop_back();
    }
    for(int i = 0;i < Digital_num;i++){
//        QString ss = "QFrame#place_" + frame_name[i] + "{border-image: url(:/imsrc/src/"+QString::number(i)+".png)}";
        chess[i] = ori_chess[i];
        if(chess[i] == 0){
            sx = i/chess_size;
            sy = i%chess_size;
        }

        text[i]->setScaledContents(true);
        if(ori_chess[i]!=0){
            QString ss = ":/imsrc/src/" + QString::number(ori_chess[i]) + ".png";
            text[i]->setPixmap(QPixmap(ss));
        }
        else{
            text[i]->clear();
        }
    }
}

void MainWindow::on_compute_clicked()
{
    if(!solved_flag){
        ui->solve_label->setText("Warming");
        ui->answer->setText("The chess isn't compute\n"
                            "Please random the chess\n");
        return;
    }
    int limit = hv(chess);
    ui->show->setEnabled(false);
    ui->commit->setEnabled(false);
    ui->random->setEnabled(false);
    ui->compute->setEnabled(false);
    ui->inputs->setEnabled(false);
    while(!path.empty()){
        path.pop_back();
    }
    ComputerThread *cthread = new ComputerThread(limit,chess,sx,sy);
    connect(cthread,SIGNAL(threadend(std::vector<int>)),this,SLOT(compute_end(std::vector<int>)));
    cthread->start();
    ui->answer->clear();
    QString sss = "Comupting..";
    QTime t(0,0,0);
    while(flag){
        ui->solve_label->setText(sss);
        ui->answer->setText(t.toString("hh,mm,ss"));
        if(sss.size() > 20)
            sss = "Comupting..";
        else{
            sss += "..";
        }
        QTime reachTime= QTime::currentTime().addSecs(1);
        while(QTime::currentTime() < reachTime)
            QCoreApplication::processEvents(QEventLoop::AllEvents,100);
        t = t.addSecs(1);
    }
    flag = true;
    cthread->quit();
    cthread->wait();
    delete cthread;
//    while(!bfs(sx,sy,0,limit,path,chess)){
//        limit ++;
//    }
    ui->solve_label->setText("The Answer");
    QString ss;
    for(auto p:path){
        ss = ss + " " + QString::fromStdString(direction[p]);
    }
    ui->answer->setText(ss);
    answer_flag = true;
}

void MainWindow::on_show_clicked()
{
    if(!solved_flag){
        ui->solve_label->setText("Warming");
        ui->answer->setText("The chess isn't compute\n"
                            "Please random the chess\n");
        return;
    }
    if(!answer_flag){
        ui->solve_label->setText("Warming");
        ui->answer->setText("Please conpute the chess first\n");
        return;
    }
    ui->solve_label->setText("Showing");
    ui->show->setEnabled(false);
    ui->commit->setEnabled(false);
    ui->random->setEnabled(false);
    ui->compute->setEnabled(false);
    ui->inputs->setEnabled(false);
    for(int i = 0;i < path.size();i++){
        int p = path[i];
        int z = sx * chess_size + sy;
        sx = sx + offset[p][0];
        sy = sy + offset[p][1];
        int g = sx * chess_size + sy;
        swap_pixmap(z,g);
        QString ss;
        for(int j = i+1;j < path.size();j++){
            ss = ss + " " + QString::fromStdString(direction[path[j]]);
        }
        ui->answer->setText(ss);
        QTime reachTime= QTime::currentTime().addSecs(1);
        while(QTime::currentTime() < reachTime)
            QCoreApplication::processEvents(QEventLoop::AllEvents,100);
    }
    while(!path.empty()){
        path.pop_back();
    }
    ui->solve_label->setText("Show End");
    ui->answer->setText("Please click rondom\n"
                        "or"
                        "Inputs chess and Commit");
    ui->show->setEnabled(true);
    ui->commit->setEnabled(true);
    ui->random->setEnabled(true);
    ui->compute->setEnabled(true);
    ui->inputs->setEnabled(true);
    solved_flag = false;
    answer_flag = false;
}

void MainWindow::on_commit_clicked()
{
    ui->answer->clear();
    QString ss = ui->inputs->toPlainText();
    QList<QString> inputs = ss.split(' ',QString::SkipEmptyParts);
    if(inputs.size()!=Digital_num){
        ui->solve_label->setText("Warming");
        ui->answer->setText("Please inputs " + QString::number(inputs.size()) + " numbers\n");
        return;
    }
    else{
        for(int i = 0;i < Digital_num;i++){
            ori_chess[i] = inputs[i].toInt();
            if(ori_chess[i] < 0 || ori_chess[i] >= Digital_num){
                ui->solve_label->setText("Warming");
                ui->answer->setText("Please inputs 0 - " + QString::number(Digital_num) + "\n");
                return;
            }
        }
        solved_flag = Canslove(ori_chess);
        answer_flag = false;
        if(solved_flag){
            ui->solve_label->setText("Can Solve");
        }
        else{
            ui->solve_label->setText("Can't Solve");
        }
        while(!path.empty()){
            path.pop_back();
        }
        for(int i = 0;i < Digital_num;i++){
            chess[i] = ori_chess[i];
            if(chess[i] == 0){
                sx = i/chess_size;
                sy = i%chess_size;
            }
            text[i]->setScaledContents(true);
            if(ori_chess[i]!=0){
                QString ss = ":/imsrc/src/" + QString::number(ori_chess[i]) + ".png";
                text[i]->setPixmap(QPixmap(ss));
            }
            else{
                text[i]->clear();
            }
        }
    }
}

void MainWindow::compute_end(std::vector<int> out_path)
{
    flag = false;
    ui->show->setEnabled(true);
    ui->commit->setEnabled(true);
    ui->random->setEnabled(true);
    ui->compute->setEnabled(true);
    ui->inputs->setEnabled(true);
    for(auto p :out_path){
        path.push_back(p);
    }
}
