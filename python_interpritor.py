from PyQt5.QtWidgets import QMainWindow, QApplication, QGridLayout, QMenuBar, QTabWidget, QTextEdit, QAction, QWidget, QSpacerItem, QSizePolicy, QVBoxLayout
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
        file_menu = menu_bar.addMenu("File")
        menu_bar.setFont(self.menu_font)
        new_file_action = QAction("new file", self)
        options_bar = menu_bar.addMenu("options")
        file_menu.addAction(new_file_action)


        self.files_tabs = QTabWidget()
        main_layout = QGridLayout()
        main_layout.addWidget(self.files_tabs, 1, 0)
        main_layout.addWidget(menu_bar, 0, 0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(1)

        new_tab = QWidget()
        tab_1_layout = QVBoxLayout()
        tab_1_layout.addWidget(QTextEdit())
        new_tab.setLayout(tab_1_layout)

        self.setLayout(main_layout)
        self.files_tabs.addTab(new_tab, "Tab 1")

        play_file_action = QAction("run", self)
        options_bar.addAction(play_file_action)
        play_file_action.triggered.connect(self.do_smt)

    def do_smt(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()