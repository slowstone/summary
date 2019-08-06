#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QTime>

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
    void on_random_clicked();

    void on_compute_clicked();

    void on_show_clicked();

    void on_commit_clicked();

    void compute_end(std::vector<int> out_path);

private:
    Ui::MainWindow *ui;
};

#endif // MAINWINDOW_H
