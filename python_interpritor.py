import sys
import os
import io
from PyQt5.QtWidgets import QApplication, QMenuBar, QTabWidget, QTextEdit, QAction, QWidget, \
    QVBoxLayout, QFileDialog, QHBoxLayout, QPushButton, QSplitter
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QObject, pyqtSlot, QRunnable, QThreadPool
from tello_binom import *
import subprocess


def hook(*args):
    sys.stdout = sys.__stdout__
    print(*args)
    sys.exit(-1)


class CodeThread(QObject):
    def __init__(self, code, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = code

    @pyqtSlot()
    def run_code(self):
        try:
            exec(self.code, globals())
        except:
            print(sys.exc_info(), file=sys.stdout)
        finally:
            self.thread().finished.emit()


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.menu_font = QFont("Arial", 10)
        self.initUI()

    def initUI(self):
        self.last_line = ""
        menu_bar = QMenuBar()
        menu_bar.setFont(self.menu_font)

        file_menu = menu_bar.addMenu("File")
        options_bar = menu_bar.addMenu("options")
        add_function_bar = menu_bar.addMenu("add function")

        new_file_action = QAction("new file", self)
        file_menu.addAction(new_file_action)
        new_file_action.triggered.connect(self.create_and_open_new_file)

        save_file_action = QAction("save file", self)
        file_menu.addAction(save_file_action)
        save_file_action.triggered.connect(self.save_file)

        remove_tab_action = QAction("close current file", self)
        options_bar.addAction(remove_tab_action)
        remove_tab_action.triggered.connect(self.close_current_tab)

        start_function_action = QAction("start", self)
        add_function_bar.addAction(start_function_action)
        start_function_action.triggered.connect(self.add_start_function)

        take_off_action = QAction("take off", self)
        add_function_bar.addAction(take_off_action)
        take_off_action.triggered.connect(self.add_take_off_function)

        land_action = QAction("land", self)
        add_function_bar.addAction(land_action)
        land_action.triggered.connect(self.add_land_function)

        start_video_action = QAction("start video", self)
        add_function_bar.addAction(start_video_action)
        start_video_action.triggered.connect(self.add_start_video_function)

        self.files_tabs = QTabWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(menu_bar, 0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(1)

        self.run_button = QPushButton(self)
        self.run_button.setStyleSheet("background-color:green")
        self.run_button.setText("run")
        self.run_button.pressed.connect(self.run_file)

        self.end_button = QPushButton(self)
        self.end_button.setStyleSheet("background-color:red")
        self.end_button.setText("end")
        self.end_button.pressed.connect(self.terminate_thread)
        self.end_button.hide()

        sub_layout = QSplitter(Qt.Horizontal)
        self.input_text_edit = QTextEdit()
        self.output_text_edit = QTextEdit()
        self.output_text_edit.setReadOnly(True)

        sub_layout.addWidget(self.input_text_edit)
        sub_layout.addWidget(self.output_text_edit)

        main_splitter = QSplitter(Qt.Vertical)
        main_splitter.addWidget(self.files_tabs)
        main_splitter.addWidget(sub_layout)
        main_layout.addWidget(main_splitter)
        main_layout.addWidget(self.run_button)
        main_layout.addWidget(self.end_button)
        self.tabs = []
        self.setLayout(main_layout)

    def exec_ended(self):
        self.output_text_edit.setText(sys.stdout.getvalue())
        print("\nProcess finished with exit code 0")
        self.run_button.show()
        self.end_button.hide()

    def create_and_open_new_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "open/new file", "", "Py(*.py)")
        if file_path:
            with open(file_path, "rt", encoding="UTF-8") as file:
                text = file.read()
                self.create_new_tab(file_path, text)

    def create_new_tab(self, file_path, text):
        tab_layout = QVBoxLayout()
        text_widget = QTextEdit()
        text_widget.setText(text)
        tab_layout.addWidget(text_widget)
        widget = QWidget()
        widget.setLayout(tab_layout)
        widget.file_path = file_path
        self.tabs.append(widget)
        self.files_tabs.addTab(self.tabs[-1], file_path.split("/")[-1])

    def close_current_tab(self):
        self.files_tabs.removeTab(self.files_tabs.currentIndex())

    def save_file(self):
        with open(self.tabs[self.files_tabs.currentIndex()].file_path, mode="wt",
                  encoding="UTF-8") as file:
            file.write(self.tabs[self.files_tabs.currentIndex()].layout().itemAt(
                0).widget().toPlainText())

    def run_file(self):
        if self.tabs:
            self.input_text_edit.clear()
            self.run_button.hide()
            self.end_button.show()
            path = self.tabs[self.files_tabs.currentIndex()].file_path
            if os.path.exists(path):
                self.save_file()

            stdin = io.StringIO(self.input_text_edit.toPlainText())
            self.stdout = io.StringIO()
            sys.stdin, sys.stdout = stdin, self.stdout
            with open(path, encoding="utf-8") as file:
                data = file.read()

            self.thrd = CodeThread(data)
            thread = QThread()
            thread.started.connect(self.thrd.run_code)
            thread.finished.connect(self.exec_ended)
            self.thrd.moveToThread(thread)
            thread.start()



    def terminate_thread(self):
        if self.thrd.thread().isFinished():
            self.thrd.thread().setTerminationEnabled(True)
            self.thrd.thread().terminate()
            self.exec_ended()

    def add_start_function(self):
        try:
            text_edit = self.tabs[self.files_tabs.currentIndex()].layout().itemAt(0).widget()
            text_edit.insertPlainText("start()\n")
        except:
            pass

    def add_take_off_function(self):
        try:
            text_edit = self.tabs[self.files_tabs.currentIndex()].layout().itemAt(0).widget()
            text_edit.insertPlainText("take_off()\n")
        except:
            pass

    def add_land_function(self):
        try:
            text_edit = self.tabs[self.files_tabs.currentIndex()].layout().itemAt(0).widget()
            text_edit.insertPlainText("land()\n")
        except:

            pass
    def add_start_video_function(self):
        try:
            text_edit = self.tabs[self.files_tabs.currentIndex()].layout().itemAt(0).widget()
            text_edit.insertPlainText("start_video()\n")
        except:
            pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = hook
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
