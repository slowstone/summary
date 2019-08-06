#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "sixchess.h"

bool iswin = false;
bool flag = true;

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    //Set Layout
    QGridLayout *chess_gl = new QGridLayout();
    chess_gl->setMargin(0);
    chess_gl->setSpacing(0);
    ui->chess->setLayout(chess_gl);

    ui->state_label->adjustSize();
    ui->state_label->setWordWrap(true);
    ui->state_label->setAlignment(Qt::AlignCenter);

    /*
     * 棋盘的初始化
     */
    // 创建棋盘
    for (int i = 1; i < chessbored_size-1; i++) {
        for (int j = 1; j < chessbored_size-1; j++) {
            QPushButton *btn = new QPushButton();
            btn->setObjectName(QString::number((i-1)*(chessbored_size-2)+(j-1)));
            btn->setFixedSize(40,40);
            button_vec.push_back(btn);
            chess_gl->addWidget(btn,i,j);
            connect(btn, SIGNAL(clicked(bool)), this, SLOT(btnClick()));
        }
    }
    this->init_game();
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::btnClick() {
    // 拿到触发当前槽函数的信号源对象
    QPushButton *btn = qobject_cast<QPushButton*>(sender());
    int index = btn->objectName().toInt();
    int x = index / (chessbored_size-2) + 1;
    int y = index % (chessbored_size-2) + 1;
    iswin = player_move(x,y);
    if(player_color == black){        //Black
        btn->setStyleSheet("border-image: url(:/imsrc/src/Black.png)");
    }
    else{               //White
        btn->setStyleSheet("border-image: url(:/imsrc/src/White.png)");
    }
    btn->setEnabled(false);
    if (iswin) {
        int nRet = QMessageBox::question(NULL, "提示", "Player Win?\nContinue?", QMessageBox::Yes, QMessageBox::No);
        // 选择是
        if (QMessageBox::Yes == nRet) {
            this->init_game();
        }
        // 选择否
        if (QMessageBox::No == nRet) {
            this->close();
        }
    }
    if(isFirst || times == 1){
        isFirst = false;
        times = 0;
        this->setstatetext(false);
//        iswin = computer_move(computer_color);
        cthread = new ComputerThread();
        connect(cthread,SIGNAL(threadend(bool,int,int)),this,SLOT(computer_end(bool,int,int)));
        cthread->start();
        for(int i = 0;i < button_vec.size();i++){
            button_vec[i]->setEnabled(false);
        }
        QString ss = ui->state_label->text();
        QTime t(0,0,0);
        while(flag){
            ui->state_label->setText(ss + t.toString("hh,mm,ss"));
            QTime reachTime= QTime::currentTime().addSecs(1);
            while(QTime::currentTime() < reachTime)
                QCoreApplication::processEvents(QEventLoop::AllEvents,100);
            t = t.addSecs(1);
        }
        flag = true;
        for(int i = 0;i < button_vec.size();i++){
            button_vec[i]->setEnabled(true);
        }
        if (iswin) {
            int nRet = QMessageBox::question(NULL, "提示", "Computer Win\nContinue?", QMessageBox::Yes, QMessageBox::No);
            // 选择是
            if (QMessageBox::Yes == nRet) {
                this->init_game();
            }
            // 选择否
            if (QMessageBox::No == nRet) {
                this->close();
            }
        }
        else{
            this->setstatetext(true);
        }
    }
    else{
        times++;
        this->setstatetext(true);
    }
}

void MainWindow::start_game()//初始化棋盘
{
    for(int i = 0;i < chessbored_size;i++){
        for(int j = 0;j < chessbored_size;j++){
            chessbored[i][j] = -1;
        }
    }
    for(int i=0;i<chessbored_size;i++)
    {
        chessbored[i][0]=side;
        chessbored[0][i]=side;
        chessbored[chessbored_size-1][i]=side;
        chessbored[i][chessbored_size-1]=side;
    }
    for(int i = 0;i < button_vec.size();i++){
        button_vec[i]->setStyleSheet("");
        button_vec[i]->setEnabled(true);
    }
    isFirst = true;
    times = 0;
}

void MainWindow::init_game() {
    //Set Introduction
    ui->state_label->setText("Introduction\n"
                             "1. Using start/reset to start or reset the chess\n"
                             "2. Black first and only one step\n"
                             "3. After two step one by one");
    for(int i = 0;i < button_vec.size();i++){
        button_vec[i]->setStyleSheet("");
        button_vec[i]->setEnabled(false);
    }
}


void MainWindow::on_state_button_clicked()
{
    this->start_game();
    this->setstatetext(true);
}

void MainWindow::setstatetext(bool isPlayer){
    QString player_ss;
    switch(player_color){
    case black:
        player_ss = "Black";
        break;
    case white:
        player_ss = "White";
        break;
    }
    QString computer_ss;
    switch(computer_color){
    case black:
        computer_ss = "Black";
        break;
    case white:
        computer_ss = "White";
        break;
    }
    QString ss = "Player is " + player_ss +
                "\nComputer is " + computer_ss +
                 "\nNow\n";
    if(isPlayer){
        ss += "Player Step " + QString::number(times+1);
    }
    else{
        ss += "Computer Step!!!\n";
    }
    ui->state_label->setText(ss);
}

void MainWindow::computer_end(bool r,int index1,int index2){
    iswin = r;
    cthread->quit();
    cthread->wait();
    delete cthread;
    cthread = NULL;
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
    flag = false;
}
