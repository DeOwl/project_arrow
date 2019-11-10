from PyQt5.QtWidgets import QApplication, QMenuBar, QTabWidget, QTextEdit, QAction, QWidget, QVBoxLayout, QFileDialog, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys


# Гы
class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.menu_font = QFont("Arial", 10)
        self.initUI()

    def initUI(self):
        menu_bar = QMenuBar()
        menu_bar.setFont(self.menu_font)
        file_menu = menu_bar.addMenu("File")
        options_bar = menu_bar.addMenu("options")

        new_file_action = QAction("new file", self)
        file_menu.addAction(new_file_action)
        new_file_action.triggered.connect(self.create_and_open_new_file)
        save_file_action = QAction("save file", self)
        file_menu.addAction(save_file_action)
        save_file_action.triggered.connect(self.save_file)

        play_file_action = QAction("run", self)
        options_bar.addAction(play_file_action)
        #play_file_action.triggered.connect(self.do_smt)
        remove_tab_action = QAction("close current file", self)
        options_bar.addAction(remove_tab_action)
        remove_tab_action.triggered.connect(self.close_current_tab)


        self.files_tabs = QTabWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(menu_bar, 0)
        main_layout.addWidget(self.files_tabs, 1)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(1)

        sub_layout = QHBoxLayout()
        self.input_text_edit = QTextEdit()
        self.output_text_edit = QTextEdit()
        sub_layout.addWidget(self.input_text_edit)
        sub_layout.addWidget(self.output_text_edit)
        main_layout.addLayout(sub_layout)

        self.tabs = []
        self.setLayout(main_layout)

    def create_and_open_new_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "open/new file", "", "Py(*.py)")
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
        with open(self.tabs[self.files_tabs.currentIndex()].file_path, mode="wt", encoding="UTF-8") as file:
            file.write(self.tabs[self.files_tabs.currentIndex()].layout().itemAt(0).widget().toPlainText())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()