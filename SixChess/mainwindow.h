#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QTime>
#include <QMessageBox>
#include "computerthread.h"

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private slots:
    void btnClick();

    void on_state_button_clicked();

    void computer_end(bool iswin, int index1,int index2);

private:
    Ui::MainWindow *ui;
    void setstatetext(bool isPlayer);
    void start_game();
    void init_game();
    ComputerThread *cthread;
};

#endif // MAINWINDOW_H
