#include "mainwindow.h"
#include <QApplication>
#include "sixchess.h"

QVector <QPushButton *> button_vec;
int chessbored[chessbored_size][chessbored_size];
QVector <node> empty_node;

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.setWindowTitle("六子棋");
    w.resize(QSize(800,600));
    QIcon icon(":/imsrc/src/ico.ico");
    w.setWindowIcon(icon);
    w.show();

    return a.exec();
}
