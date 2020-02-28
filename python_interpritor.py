# encoding:utf-8
import os
import time
import random
import io
from PyQt5.QtWidgets import QApplication, QMenuBar, QTabWidget, QPlainTextEdit, QAction, QWidget, \
    QVBoxLayout, QFileDialog, QPushButton, QSplitter, QLabel, QMenu, QHBoxLayout, QScrollArea, QSizePolicy, QComboBox, QDesktopWidget
from PyQt5.QtGui import QFont, QPixmap, QImage, QSyntaxHighlighter, QTextCharFormat, QColor, QPainter, QFontMetrics
from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal, pyqtSlot, QEvent, QRegularExpression, QRegExp, QRect, QTimer
import traceback
import sys
import threading
import cv2
import zipfile
from subprocess import Popen, PIPE
from PIL import Image
import tello_sensor

FILEDIALOGS_OPTIONS = QFileDialog.Options()


def decrypt_file(image_path, file_path):
    '''Расшифровывает троян
image_path - путь к трояну
file_path - необходимый файл в трояне'''

    img = Image.open(image_path)
    x, y = img.size
    with zipfile.ZipFile(image_path) as zf:
        # Придумать пароль
        return zf.open(file_path, pwd=f"{x}{image_path.split('/')[-1]}{y}".encode("utf-8"))


class LessonView(QWidget):
    def __init__(self, lesson_num, amount_of_pages, amount_of_listings):
        super().__init__()
        self.pages = []
        self.current_page = 0
        self.initUi(lesson_num, amount_of_pages, amount_of_listings)

    def initUi(self, lesson_num, amount_of_pages, amount_of_listings):
        self.setMaximumHeight(QDesktopWidget().screenGeometry(0).height())
        self.setFixedWidth(1100)
        self.resize(1100, QDesktopWidget().screenGeometry(0).height() - 100)
        self.get_images(lesson_num, amount_of_pages, amount_of_listings)
        self.my_layout = QHBoxLayout()

        self.left_button = QPushButton(self)
        self.left_button.setText("⯇")
        self.left_button.setFont(QFont("Arial", 15))
        self.left_button.setMaximumWidth(25)
        self.left_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.left_button.clicked.connect(self.previous_page)
        self.my_layout.addWidget(self.left_button, 0)

        self.image_out = QLabel(self)
        self.image_out.move(0, 0)
        self.image_out.setPixmap(self.pages[self.current_page])
        self.scroll_area = QScrollArea(self)
        self.scroll_area.move(0, 0)
        self.scroll_area.setFixedWidth(1000)
        self.scroll_area.setWidget(self.image_out)
        self.my_layout.addWidget(self.scroll_area, 1)

        self.right_button = QPushButton(self)
        self.right_button.setText("⯈")
        self.right_button.setFont(QFont("Arial", 15))
        self.right_button.setMaximumWidth(25)
        self.right_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.right_button.clicked.connect(self.next_page)
        self.my_layout.addWidget(self.right_button, 2)

        self.setLayout(self.my_layout)

    def get_images(self, lesson_num, amount_of_pages, amount_of_listings):
        for i in range(1, amount_of_pages + 1):
            page = decrypt_file("data/textures/video_background.png", f"data/Lesson{lesson_num}_jpg/Lesson{lesson_num}_jpg/Lesson-{lesson_num}-{i}.jpg")
            pixmap = QPixmap()
            pixmap.loadFromData(page.read())
            self.pages.append(pixmap)

    def previous_page(self):
        self.current_page = max(0, self.current_page - 1)
        self.image_out.setPixmap(self.pages[self.current_page])

    def next_page(self):
        self.current_page = min(len(self.pages) - 1, self.current_page + 1)
        self.image_out.setPixmap(self.pages[self.current_page])


def format_code(color, style=''):
    """Return a QTextCharFormat with the given attributes.
    """
    _color = QColor(color)

    _format = QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QFont.DemiBold)
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format


STYLES = {
    'keyword': format_code('#0047e0'),
    'operator': format_code('#000000'),
    'brace': format_code('#3d3d3d'),
    'defclass': format_code('#000000', "bold"),
    'string': format_code('#02bd27'),
    'string2': format_code('#b000aa'),
    'comment': format_code('#757575', "italic"),
    'self': format_code('#cc00cc'),
    'numbers': format_code('#07006b'),
}





class MyHighlighter(QSyntaxHighlighter):
    keywords = [
        'and', 'assert', 'break', 'class', 'continue', 'def',
        'del', 'elif', 'else', 'except', 'exec', 'finally',
        'for', 'from', 'global', 'if', 'import', 'in',
        'is', 'lambda', 'not', 'or', 'pass', 'print',
        'raise', 'return', 'try', 'while', 'yield',
        'None', 'True', 'False', "range", "with", "open", "as", "input"
    ]

    # Python operators
    operators = ['=', '==', '!=', '<', '<=', '>', '>=', '\+', '-', '\*', '/', '//', '\%', '\*\*', '\+=', '-=', '\*=',
                 '/=', '\%=', '\^', '\|', '\&', '\~', '>>', '<<',]

    # Python braces
    braces = ['\{', '\}', '\(', '\)', '\[', '\]',]

    def highlightBlock(self, text):
        self.tri_single = (QRegExp("'''"), 1, STYLES['string2'])
        self.tri_double = (QRegExp('"""'), 2, STYLES['string2'])

        rules = []

        # Keyword, operator, and brace rules
        rules += [(r'\b%s\b' % w, 0, STYLES['keyword'])
                  for w in MyHighlighter.keywords]
        rules += [(r'%s' % o, 0, STYLES['operator'])
                  for o in MyHighlighter.operators]
        rules += [(r'%s' % b, 0, STYLES['brace'])
                  for b in MyHighlighter.braces]

        # All other rules
        rules += [
            # 'self'
            (r'\bself\b', 0, STYLES['self']),

            # Double-quoted string, possibly containing escape sequences
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),
            # Single-quoted string, possibly containing escape sequences
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),

            # 'class' followed by an identifier
            (r'\bclass\b\s*(\w+)', 1, STYLES['defclass']),

            # From '#' until a newline
            (r'#[^\n]*', 0, STYLES['comment']),

            # Numeric literals
            (r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['numbers']),
        ]

        # Build a QRegExp for each pattern
        self.rules = [(QRegExp(pat), index, fmt)
                      for (pat, index, fmt) in rules]

        char_format = QTextCharFormat()
        char_format.setFontWeight(QFont.Bold)
        char_format.setForeground(Qt.darkMagenta)

        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)

            while index >= 0:
                # We actually want the index of the nth match
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)


class NumberBar(QWidget):
    def __init__(self, parent, window):
        super().__init__(window)
        self.editor = parent
        layout = QVBoxLayout()
        self.visible = True
        self.editor.blockCountChanged.connect(self.update_width)
        self.editor.updateRequest.connect(self.update_on_scroll)
        self.resize(9, parent.height())
        self.update_width(str(self.editor.blockCount()))
        self.window_ = window

    def update_on_scroll(self, rect, scroll):
        if self.isVisible():
            if scroll:
                self.scroll(0, scroll)
            else:
                self.update()

    def update_width(self, string):
        width = self.fontMetrics().width(str(string)) + 8
        if self.width() != width:
            self.setFixedWidth(width)

    def paintEvent(self, event):
        self.resize(self.width(), self.editor.height())
        if self.isVisible():
            block = self.editor.firstVisibleBlock()
            height = self.fontMetrics().height()
            number = block.blockNumber()
            painter = QPainter(self)
            painter.fillRect(event.rect(), Qt.lightGray)
            painter.drawRect(0, 0, event.rect().width() - 1, event.rect().height() - 1)
            font = painter.font()

            current_block = self.editor.textCursor().block().blockNumber() + 1

            condition = True
            while block.isValid() and condition:
                block_geometry = self.editor.blockBoundingGeometry(block)
                offset = self.editor.contentOffset()
                block_top = block_geometry.translated(offset).top()
                number += 1

                rect = QRect(0, block_top + 2, self.width() - 5, height)

                if number == current_block:
                    font.setBold(True)
                else:
                    font.setBold(False)

                painter.setFont(font)
                painter.drawText(rect, Qt.AlignRight, '%i'%number)

                if block_top > event.rect().bottom():
                    condition = False

                block = block.next()
            painter.end()


class SensorThread(QThread):
    output = pyqtSignal(str)
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.stop_flag = False
        self.name = None

    def __del__(self):
        self.stop_flag = True
        self.wait()


    def render(self, name):
        self.name = name
        self.start()

    def run(self):
        if self.name:
            if self.name == 1:
                connection = tello_sensor.connect_eco_sensor()
            else:
                connection = None
            if connection:
                while not self.stop_flag:
                    time.sleep(0.5)
                    data = tello_sensor.get_data()
                    if data:
                        self.output.emit("\n".join(data))
                    elif data is None:
                        self.output.emit("")
                    else:
                        window.sensor_connection.setCurrentIndex(0)
                        self.stop_flag = True

            else:
                window.sensor_connection.setCurrentIndex(0)


class CodeThread(QObject):
    def __init__(self, file_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_path = file_path
        self.runnable_file = None
        self.output = ""
        self.quit = False

    @pyqtSlot()
    def run_code(self):
        self.runnable_file = Popen([sys.executable, self.file_path], stdout=PIPE, stderr=PIPE, stdin=PIPE)
        while self.runnable_file and self.runnable_file.poll() is None and not self.quit:
            try:
                self.output += self.runnable_file.stdout.readline().decode("UTF-8")
            except:
                break
        if self.runnable_file:
            if not self.quit:
                self.output += self.runnable_file.stdout.read().decode() + self.runnable_file.stderr.read().decode()
            self.thread().finished.emit()

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Среда разработки для квадрокоптеров Tello Edu")
        self.menu_font = QFont("Arial", 10)
        self.code_button_font = QFont("Arial", 16)
        self.setGeometry(0, 0, QDesktopWidget().screenGeometry(0).width() * 0.66, QDesktopWidget().screenGeometry(0).height() * 0.66)
        self.thrd = None
        self.initUI()

    def initUI(self):
        menu_bar = QMenuBar()
        menu_bar.setFont(self.menu_font)
        self.setup_menu(menu_bar)

        self.file_tab_sub_layout = QVBoxLayout()

        self.tab_widget = QTabWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(menu_bar, 0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(1)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_selected_tab)
        self.file_tab_sub_layout.addWidget(self.tab_widget)


        sensor_layout = QVBoxLayout()
        self.sensor_connection = QComboBox()

        self.sensor_connection.addItem("-")
        self.sensor_connection.addItem("Модуль экология")
        self.sensor_connection.currentIndexChanged.connect(self.connect_sensor)
        self.sensor_connection.setMaximumWidth(600)
        self.sensor_connection.setMaximumHeight(20)
        self.sensor_info = QPlainTextEdit()
        self.sensor_info.setMaximumWidth(600)
        self.sensor_thrd = None

        sensor_tab_widget = QTabWidget()

        sensor_widget = QWidget()
        sensor_sub_layout = QHBoxLayout()
        self.start_sensor_record = QPushButton(self)
        self.start_sensor_record.setText("Начать запись")
        self.start_sensor_record.setStyleSheet("background-color:green")
        self.start_sensor_record.setFont(self.code_button_font)
        sensor_sub_layout.addWidget(self.start_sensor_record)
        self.stop_sensor_record = QPushButton(self)
        self.stop_sensor_record.setText("Завершить запись")
        self.stop_sensor_record.setStyleSheet("background-color:red")
        self.stop_sensor_record.setFont(self.code_button_font)
        sensor_sub_layout.addWidget(self.stop_sensor_record)

        sensor_layout.addWidget(self.sensor_connection, 0)
        sensor_layout.addWidget(self.sensor_info, 1)
        sensor_layout.addLayout(sensor_sub_layout)
        sensor_widget.setLayout(sensor_layout)
        sensor_tab_widget.addTab(sensor_widget, "Сенсор")
        sensor_tab_widget.addTab(QWidget(), "График")

        sub_layout = QHBoxLayout()
        sub_layout.addLayout(self.file_tab_sub_layout, 0)
        sub_layout.addWidget(sensor_tab_widget)
        sub_layout_widget = QWidget(self)
        sub_layout_widget.setLayout(sub_layout)

        self.run_button = QPushButton(self)
        self.run_button.setStyleSheet("background-color:green")
        self.run_button.setText("Запустить")
        self.run_button.pressed.connect(self.run_file)
        self.run_button.setFont(self.code_button_font)

        self.end_button = QPushButton(self)
        self.end_button.setStyleSheet("background-color:red")
        self.end_button.setText("Завершить")
        self.end_button.pressed.connect(self.terminate_thread)
        self.end_button.setFont(self.code_button_font)
        self.end_button.hide()

        sub_splitter = QSplitter(Qt.Horizontal)
        input_tab = QTabWidget()
        self.input_text_edit = QPlainTextEdit()
        self.input_text_edit.last_text = ""
        self.input_text_edit.last_line = ""
        input_tab.addTab(self.input_text_edit, 'Поле ввода')
        self.input_text_edit.textChanged.connect(self.push_text_to_running_file)
        output_tab = QTabWidget()
        self.output_text_edit = QPlainTextEdit()

        output_tab.addTab(self.output_text_edit, 'Поле вывода')
        self.output_text_edit.setReadOnly(True)
        self.output_text_edit.verticalScrollBar().setTracking(True)

        sub_splitter.addWidget(input_tab)
        sub_splitter.addWidget(output_tab)

        main_splitter = QSplitter(Qt.Vertical)
        main_splitter.addWidget(sub_layout_widget)
        main_splitter.addWidget(sub_splitter)
        main_layout.addWidget(main_splitter)
        self.file_tab_sub_layout.addWidget(self.run_button)
        self.file_tab_sub_layout.addWidget(self.end_button)
        self.tabs = []
        self.setLayout(main_layout)

        self.opened_lessons = []

    def setup_menu(self, menu_bar):
        file_menu = menu_bar.addMenu("Файл")
        file_menu.setToolTipsVisible(True)
        add_move_command_bar = menu_bar.addMenu("Команды управления")
        add_move_command_bar.setToolTipsVisible(True)
        add_move_3d_bar = menu_bar.addMenu("3d-движение")
        add_move_3d_bar.setToolTipsVisible(True)
        add_set_command = menu_bar.addMenu("Команды установки значений")
        add_set_command.setToolTipsVisible(True)
        add_get_command = menu_bar.addMenu("Команды считывания значений")
        add_get_command.setToolTipsVisible(True)
        lesson_menu = menu_bar.addMenu("Обучение")
        help_menu = menu_bar.addMenu("Помощь")
        help_menu.setToolTipsVisible(True)

        # file_actions
        new_file_action = QAction("Новый Файл", self)
        file_menu.addAction(new_file_action)
        new_file_action.triggered.connect(lambda x: self.create_new_tab("Неназванный", "from tello_binom import *\n"))

        open_file_action = QAction("Открыть", self)
        file_menu.addAction(open_file_action)
        open_file_action.triggered.connect(self.open_file)

        save_file_action = QAction("Сохранить", self)
        file_menu.addAction(save_file_action)
        save_file_action.triggered.connect(self.save_file)

        save_file_as_action = QAction("Сохранить как", self)
        file_menu.addAction(save_file_as_action)
        save_file_as_action.triggered.connect(self.save_file_as)

        video_help = QAction("Видеоуроки", self)
        help_menu.addAction(video_help)

        # move_actions

        start_function_action = QAction("start()", self)
        add_move_command_bar.addAction(start_function_action)
        add_move_command_bar.setToolTipsVisible(True)
        start_function_action.setToolTip("Вход в режим исполнения команд")
        start_function_action.triggered.connect(lambda: self.add_function("start()"))

        take_off_action = QAction("takeoff()", self)
        add_move_command_bar.addAction(take_off_action)
        take_off_action.setToolTip("Автоматический взлет и стабилизация")
        take_off_action.triggered.connect(lambda: self.add_function("takeoff()"))

        land_action = QAction("land()", self)
        add_move_command_bar.addAction(land_action)
        land_action.setToolTip("Автоматическая посадка")
        land_action.triggered.connect(lambda: self.add_function("land()"))

        start_video_action = QAction("start_video()", self)
        add_move_command_bar.addAction(start_video_action)
        start_video_action.setToolTip("Включить видеопоток с фронтальной камеры")
        start_video_action.triggered.connect(lambda: self.add_function("start_video()"))

        end_video_action = QAction("stop_video()", self)
        add_move_command_bar.addAction(end_video_action)
        end_video_action.setToolTip("Выключить видеопоток с фронтальной камеры")
        end_video_action.triggered.connect(lambda: self.add_function("stop_video()"))

        stop_action = QAction("stop()", self)
        add_move_command_bar.addAction(stop_action)
        stop_action.setToolTip("Экстренная немедленная остановка моторов")
        stop_action.triggered.connect(lambda: self.add_function("stop()"))

        movement_sub_menu = QMenu("перемещение", self)
        movement_sub_menu.setToolTipsVisible(True)

        fly_up_action = QAction("up(x)", self)
        movement_sub_menu.addAction(fly_up_action)
        fly_up_action.setToolTip("Движение вверх на х см (значение х от 20 до 500)")
        fly_up_action.triggered.connect(lambda: self.add_function("up(20)"))

        fly_down_action = QAction("down(x)", self)
        movement_sub_menu.addAction(fly_down_action)
        fly_down_action.setToolTip("Движение вниз на х см (значение х от 20 до 500)")
        fly_down_action.triggered.connect(lambda: self.add_function("down(20)"))

        fly_left_action = QAction("left(x)", self)
        movement_sub_menu.addAction(fly_left_action)
        fly_left_action.setToolTip("Движение влево на х см (значение х от 20 до 500)")
        fly_left_action.triggered.connect(lambda: self.add_function("left(20)"))

        fly_right_action = QAction("right(x)", self)
        movement_sub_menu.addAction(fly_right_action)
        fly_right_action.setToolTip("Движение вправо на х см (значение х от 20 до 500)")
        fly_right_action.triggered.connect(lambda: self.add_function("right(20)"))

        fly_forward_action = QAction("forward(x)", self)
        movement_sub_menu.addAction(fly_forward_action)
        fly_forward_action.setToolTip("Движение вперед на х см (значение х от 20 до 500)")
        fly_forward_action.triggered.connect(lambda: self.add_function("forward(20)"))

        fly_backward_action = QAction("backward(x)", self)
        movement_sub_menu.addAction(fly_backward_action)
        fly_backward_action.setToolTip("Движение назад на х см (значение х от 20 до 500)")
        fly_backward_action.triggered.connect(lambda: self.add_function("backward(20)"))

        add_move_command_bar.addMenu(movement_sub_menu)

        sub_rotate_menu = QMenu("повороты", self)
        sub_rotate_menu.setToolTipsVisible(True)
        turn_clockwise_action = QAction("clockwise(x)", self)
        sub_rotate_menu.addAction(turn_clockwise_action)
        turn_clockwise_action.setToolTip("Поворот на х градусов по часовой стрелке (значение х от 1 до 360)")
        turn_clockwise_action.triggered.connect(lambda: self.add_function("clockwise(20)"))

        turn_anticlockwise_action = QAction("anticlockwise(x)", self)
        sub_rotate_menu.addAction(turn_anticlockwise_action)
        turn_anticlockwise_action.setToolTip("Поворот на х градусов против часовой стрелке (значение х от 1 до 360)")
        turn_anticlockwise_action.triggered.connect(lambda: self.add_function("anticlockwise(20)"))

        add_move_command_bar.addMenu(sub_rotate_menu)

        flips_sub_menu = QMenu("перевороты", self)
        flips_sub_menu.setToolTipsVisible(True)

        flip_forward_action = QAction("flip_forward()", self)
        flips_sub_menu.addAction(flip_forward_action)
        flip_forward_action.setToolTip("переворот вперед относительно передних моторов")
        flip_forward_action.triggered.connect(lambda: self.add_function("flip_forward()"))

        flip_backward_action = QAction("flip_backward()", self)
        flips_sub_menu.addAction(flip_backward_action)
        flip_backward_action.setToolTip("переворот назад относительно задних моторов")
        flip_backward_action.triggered.connect(lambda: self.add_function("flip_backward()"))

        flip_left_action = QAction("flip_left()", self)
        flips_sub_menu.addAction(flip_left_action)
        flip_left_action.setToolTip("переворот влево относительно левых моторов")
        flip_left_action.triggered.connect(lambda: self.add_function("flip_left()"))

        flip_right_action = QAction("flip_right()", self)
        flips_sub_menu.addAction(flip_right_action)
        flip_right_action.setToolTip("переворот вправо относительно правых моторов")
        flip_right_action.triggered.connect(lambda: self.add_function("flip_right()"))

        add_move_command_bar.addMenu(flips_sub_menu)

        go_x_y_z_action = QAction("go(x, y, z, speed)", self)
        add_move_3d_bar.addAction(go_x_y_z_action)
        go_x_y_z_action.setToolTip("Движение к точке с координатами x, y, z "
                                   "(значения x, y, z от -500 до 500, не могут быть одновременно между -20 и 20)")
        go_x_y_z_action.triggered.connect(lambda: self.add_function("go(x, y, z, speed)"))

        arc_action = QAction("arc(x1, y1, z1, x2, y2, z2, speed)", self)
        add_move_3d_bar.addAction(arc_action)
        arc_action.setToolTip("Движение по кривой, построенной через точку 1 к точке 2")
        arc_action.triggered.connect(lambda: self.add_function("arc(x1, y1, z1, x2, y2, z2, speed)"))

        set_speed_action = QAction("speed(x)", self)
        add_set_command.addAction(set_speed_action)
        set_speed_action.setToolTip("Установка скорости х см/с (значение х от 10 до 100)")
        set_speed_action.triggered.connect(lambda: self.add_function("speed(10)"))

        set_pads_detect_on = QAction("pads_on()", self)
        add_set_command.addAction(set_pads_detect_on)
        set_pads_detect_on.setToolTip("Включение режима обнаружения полетных карточек")
        set_pads_detect_on.triggered.connect(lambda: self.add_function("pads_on()"))

        set_pads_detect_off = QAction("pads_off()", self)
        add_set_command.addAction(set_pads_detect_off)
        set_pads_detect_off.setToolTip("Выключение режима обнаружения полетных карточек")
        set_pads_detect_off.triggered.connect(lambda: self.add_function("pads_off()"))

        get_height = QAction("get_tof()", self)
        add_get_command.addAction(get_height)
        get_height.setToolTip("Получить текущую высоту")
        get_height.triggered.connect(lambda: self.add_function("get_tof()"))

        get_battery_charge = QAction("get_battery()", self)
        add_get_command.addAction(get_battery_charge)
        get_battery_charge.setToolTip("Получить остаток заряда батареи в процентах")
        get_battery_charge.triggered.connect(lambda: self.add_function("get_battery()"))

        get_mission_pad_number = QAction("get_mission_pad()", self)
        add_get_command.addAction(get_mission_pad_number)
        get_mission_pad_number.setToolTip("Получить номер обнаруженной полетной карточки")
        get_mission_pad_number.triggered.connect(lambda: self.add_function("get_mission_pad()"))

        get_video_frame_image = QAction("get_video_frame()", self)
        add_get_command.addAction(get_video_frame_image)
        get_video_frame_image.setToolTip("Получить последний кадр из видеопотока")
        get_video_frame_image.triggered.connect(lambda: self.add_function("get_video_frame()"))

        lessons_sub_menu = QMenu("Уроки", self)
        lessons_sub_menu.setToolTipsVisible(True)

        lesson_0_action = QAction("Урок 0", self)
        lessons_sub_menu.addAction(lesson_0_action)
        lesson_0_action.triggered.connect(lambda: self.open_lesson(0, 25, 0))
        lesson_1_action = QAction("Урок 1", self)
        lessons_sub_menu.addAction(lesson_1_action)
        lesson_1_action.triggered.connect(lambda: self.open_lesson(1, 17, 0))
        lesson_2_action = QAction("Урок 2", self)
        lessons_sub_menu.addAction(lesson_2_action)
        lesson_2_action.triggered.connect(lambda: self.open_lesson(2, 15, 0))
        lesson_3_action = QAction("Урок 3", self)
        lessons_sub_menu.addAction(lesson_3_action)
        lesson_3_action.triggered.connect(lambda: self.open_lesson(3, 14, 0))
        lesson_4_action = QAction("Урок 4", self)
        lessons_sub_menu.addAction(lesson_4_action)
        lesson_4_action.triggered.connect(lambda: self.open_lesson(4, 15, 0))
        lesson_5_action = QAction("Урок 5", self)
        lessons_sub_menu.addAction(lesson_5_action)
        lesson_5_action.triggered.connect(lambda: self.open_lesson(5, 13, 0))
        lesson_6_action = QAction("Урок 6", self)
        lessons_sub_menu.addAction(lesson_6_action)
        lesson_6_action.triggered.connect(lambda: self.open_lesson(6, 15, 0))
        lesson_7_action = QAction("Урок 7", self)
        lessons_sub_menu.addAction(lesson_7_action)
        lesson_7_action.triggered.connect(lambda: self.open_lesson(7, 15, 0))
        lesson_8_action = QAction("Урок 8", self)
        lessons_sub_menu.addAction(lesson_8_action)
        lesson_8_action.triggered.connect(lambda: self.open_lesson(8, 13, 0))
        lesson_9_action = QAction("Урок 9", self)
        lessons_sub_menu.addAction(lesson_9_action)
        lesson_9_action.triggered.connect(lambda: self.open_lesson(9, 14, 0))
        lesson_10_action = QAction("Урок 10", self)
        lessons_sub_menu.addAction(lesson_10_action)
        lesson_10_action.triggered.connect(lambda: self.open_lesson(10, 21, 0))
        lesson_menu.addMenu(lessons_sub_menu)

        listing_sub_menu = QMenu("Листинги", self)
        lesson_menu.addMenu(listing_sub_menu)
        listing_1_1 = QAction("Урок1-1", self)
        listing_sub_menu.addAction(listing_1_1)
        listing_1_1.triggered.connect(lambda: self.get_listing("Lesson_1_1.py"))
        listing_2_1 = QAction("Урок2-1", self)
        listing_sub_menu.addAction(listing_2_1)
        listing_2_1.triggered.connect(lambda: self.get_listing("Lesson_2_1.py"))
        listing_3_1 = QAction("Урок3-1", self)
        listing_sub_menu.addAction(listing_3_1)
        listing_3_1.triggered.connect(lambda: self.get_listing("Lesson_3_1.py"))
        listing_4_1 = QAction("Урок4-1", self)
        listing_sub_menu.addAction(listing_4_1)
        listing_4_1.triggered.connect(lambda: self.get_listing("Lesson_4_1.py"))
        listing_5_1 = QAction("Урок5-1", self)
        listing_sub_menu.addAction(listing_5_1)
        listing_5_1.triggered.connect(lambda: self.get_listing("Lesson_5_1.py"))
        listing_6_1 = QAction("Урок6-1", self)
        listing_sub_menu.addAction(listing_6_1)
        listing_6_1.triggered.connect(lambda: self.get_listing("Lesson_6_1.py"))
        listing_6_2 = QAction("Урок6-2", self)
        listing_sub_menu.addAction(listing_6_2)
        listing_6_2.triggered.connect(lambda: self.get_listing("Lesson_6_2.py"))
        listing_6_3 = QAction("Урок6-3", self)
        listing_sub_menu.addAction(listing_6_3)
        listing_6_3.triggered.connect(lambda: self.get_listing("Lesson_6_3.py"))
        listing_7_1 = QAction("Урок7-1", self)
        listing_sub_menu.addAction(listing_7_1)
        listing_7_1.triggered.connect(lambda: self.get_listing("Lesson_7_1.py"))
        listing_7_2 = QAction("Урок7-2", self)
        listing_sub_menu.addAction(listing_7_2)
        listing_7_2.triggered.connect(lambda: self.get_listing("Lesson_7_2.py"))
        listing_8_1 = QAction("Урок8-1", self)
        listing_sub_menu.addAction(listing_8_1)
        listing_8_1.triggered.connect(lambda: self.get_listing("Lesson_8_1.py"))
        listing_9_1 = QAction("Урок9-1", self)
        listing_sub_menu.addAction(listing_9_1)
        listing_9_1.triggered.connect(lambda: self.get_listing("Lesson_9_1.py"))
        listing_10_1 = QAction("Урок10-1", self)
        listing_sub_menu.addAction(listing_10_1)
        listing_10_1.triggered.connect(lambda: self.get_listing("Lesson_10_1.py"))
        listing_10_2 = QAction("Урок10-2", self)
        listing_sub_menu.addAction(listing_10_2)
        listing_10_2.triggered.connect(lambda: self.get_listing("Lesson_10_2.py"))
        listing_10_3 = QAction("Урок10-3", self)
        listing_sub_menu.addAction(listing_10_3)
        listing_10_3.triggered.connect(lambda: self.get_listing("Lesson_10_3.py"))


    def connect_sensor(self, name):
        if name == 1:
            if self.sensor_thrd:
                del self.sensor_thrd
            self.sensor_thrd = SensorThread()
            self.sensor_thrd.finished.connect(self.finished_sensor_thrd)
            self.sensor_thrd.output.connect(self.set_sensor_data)
            self.sensor_thrd.render(1)

    def finished_sensor_thrd(self):
        self.sensor_thrd = None


    def set_sensor_data(self, string):
        self.sensor_info.setPlainText(string)


    def exec_ended(self):
        self.set_output()
        self.terminate_thread()
        print("\nПрограмма завершила свою работу")
        self.run_button.show()
        self.end_button.hide()

    def terminate_thread(self):
        if self.thrd and self.thrd.runnable_file:
            self.thrd.runnable_file.terminate()
            self.thrd.runnable_file = None
            self.thrd.thread().quit()


    def save_file_as(self):
        if self.tabs:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Сохранить Файл", "", "Py(*.py)", options=FILEDIALOGS_OPTIONS)
            if file_path:
                self.tabs[self.tab_widget.currentIndex()].file_path = file_path
                self.tab_widget.setTabText(self.tab_widget.currentIndex(), file_path.split("/")[-1])
                with open(self.tabs[self.tab_widget.currentIndex()].file_path, mode="wt",
                          encoding="UTF-8") as file:
                    file.write(self.tabs[self.tab_widget.currentIndex()].layout().itemAt(
                        1).widget().toPlainText())

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Открыть файл", "", "Py(*.py)", options=FILEDIALOGS_OPTIONS)
        if file_path:
            with open(file_path, "rt", encoding="UTF-8") as file:
                text = file.read()
                self.create_new_tab(file_path, text)


    def create_new_tab(self, file_path, text):
        tab_layout = QHBoxLayout()
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.setSpacing(0)
        if len(text) > 0 and not text[0].isprintable():
            text_widget = QPlainTextEdit(text[1:])
        else:
            text_widget = QPlainTextEdit(text)
        font = QFont()
        font.setFamily("Courier")
        font.setStyleHint(QFont.Monospace)
        font.setFixedPitch(True)
        font.setPointSize(10)
        text_widget.setFont(font)
        metrics = QFontMetrics(font)
        text_widget.setTabStopWidth(4 * metrics.width(' '))
        widget = QWidget()
        number_bar = NumberBar(text_widget, widget)

        tab_layout.addWidget(number_bar)
        tab_layout.addWidget(text_widget)
        widget.setLayout(tab_layout)
        widget.file_path = file_path
        widget.highlighter = MyHighlighter(text_widget.document())
        self.tabs.append(widget)
        self.tab_widget.addTab(self.tabs[-1], file_path.split("/")[-1])

    def close_selected_tab(self, index):
        if self.tabs:
            path = self.tabs[index].file_path
            if os.path.exists(path) and os.path.isfile(path):
                self.save_file()
            else:
                self.save_file_as()
            self.tab_widget.removeTab(self.tab_widget.currentIndex())
            self.tabs.pop(index)

    def save_file(self):
        if self.tabs:
            if os.path.exists(self.tabs[self.tab_widget.currentIndex()].file_path):
                with open(self.tabs[self.tab_widget.currentIndex()].file_path, mode="wt",
                        encoding="UTF-8") as file:
                    file.write(self.tabs[self.tab_widget.currentIndex()].layout().itemAt(
                        1).widget().toPlainText())
            else:
                self.save_file_as()


    def run_file(self):
        if self.tabs:
            self.output_text_edit.clear()
            self.input_text_edit.last_text = ""
            self.input_text_edit.last_line = ""
            self.input_text_edit.clear()


            path = self.tabs[self.tab_widget.currentIndex()].file_path
            if os.path.exists(path) and os.path.isfile(path):
                self.save_file()
            else:
                self.save_file_as()
                return

            self.run_button.hide()
            self.end_button.show()
            stdin = io.StringIO(self.input_text_edit.toPlainText())
            self.stdout = io.StringIO()
            sys.stdin, sys.stdout = stdin, self.stdout



            self.thrd = CodeThread(path)
            thread = QThread(self.thrd)

            thread.started.connect(self.thrd.run_code)
            thread.finished.connect(self.exec_ended)
            self.thrd.moveToThread(thread)
            self.output_timer = QTimer()
            self.output_timer.timeout.connect(self.set_output)
            self.output_timer.start(1)
            thread.start()

    def add_function(self, text):
        try:
            text_edit = self.tabs[self.tab_widget.currentIndex()].layout().itemAt(1).widget()
            text_edit.insertPlainText(text + "\n")
        except:
            pass

    def closeEvent(self, QCloseEvent):
        self.exec_ended()
        for i in self.tabs:
            path = i.file_path
            if os.path.exists(path) and os.path.isfile(path):
                self.save_file()
            else:
                self.save_file_as()

    def open_lesson(self, lesson_number, number_of_pages, number_of_listings):
        self.opened_lessons.append(LessonView(lesson_number, number_of_pages, number_of_listings))
        self.opened_lessons[-1].show()

    def get_listing(self, listing_name):
        listing = decrypt_file("data/textures/video_background.png", f"data/Listings/{listing_name}").read().decode("utf-8")
        self.create_new_tab(listing_name, listing)

    def push_text_to_running_file(self):
        if self.thrd and self.thrd.runnable_file:
            text = self.input_text_edit.toPlainText()
            if len(text) < len(self.input_text_edit.last_text):
                if self.input_text_edit.last_line:
                    self.input_text_edit.last_line = self.input_text_edit.last_line[:-1]
                self.input_text_edit.last_text = text
            elif len(text) > len(self.input_text_edit.last_text):
                new_text = self.input_text_edit.last_line + text[len(self.input_text_edit.last_text):]
                if "\n" in new_text:
                    text1 = "\n".join(new_text.split("\n")[:-1]) + "\n"
                    self.thrd.runnable_file.stdin.write(text1.encode("UTF-8"))
                    self.thrd.runnable_file.stdin.flush()
                self.input_text_edit.last_line = text.split("\n")[-1]
                self.input_text_edit.last_text = text

    def set_output(self):
        if self.thrd and self.thrd.runnable_file:
            if len(self.thrd.output.split("\n")) > len(self.output_text_edit.toPlainText().split("\n")):
                self.output_text_edit.setPlainText("\n".join(self.thrd.output.split("\n")[-10000:]))
                self.output_text_edit.verticalScrollBar().setValue(
                    self.output_text_edit.verticalScrollBar().value() + (len(self.thrd.output.split("\n")) - len(self.output_text_edit.toPlainText().split("\n"))) * 16)


def hook(*args):
    sys.stdout = sys.__stdout__
    traceback.print_last()
    os._exit(-1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = hook
    window = MainWindow()
    window.show()
    os._exit(app.exec())
