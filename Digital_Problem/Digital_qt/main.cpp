#include "mainwindow.h"
#include <QApplication>
#include <QMetaType>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    qRegisterMetaType<std::vector<int>>("std::vector<int>");
    w.setWindowTitle("十五数码问题");
    QIcon icon(":/imsrc/src/ico.ico");
    w.setWindowIcon(icon);
    w.show();

    return a.exec();
}
