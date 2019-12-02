import os
import io
from PyQt5.QtWidgets import QApplication, QMenuBar, QTabWidget, QTextEdit, QAction, QWidget, \
    QVBoxLayout, QFileDialog, QPushButton, QSplitter, QLabel, QMenu, QHBoxLayout
from PyQt5.QtGui import QFont, QPixmap, QImage
from PyQt5.QtCore import Qt, QThread, QObject, pyqtSlot, QEvent
from tello_binom import *
from tello_binom import _VideoStream, _video, start_video, stop_video, get_video_frame
import traceback
import sys
import threading
import cv2
from win32api import GetSystemMetrics


class _VideoStream:
    started = False
    thread = None
    kill_event = None
    frame = None
    windows = {}
    screen = None

    def start(self):
        if not self.started:
            sock.sendto('streamon'.encode(encoding="utf-8"), tello_address)
            time.sleep(1)
            self.kill_event = threading.Event()
            if platform.system() == "Darwin":
                self.thread = threading.Thread(target=self._pyqt5_video_loop, args=[self.kill_event])
                pygame.init()
                self.screen = pygame.display.set_mode([640, 480])
                pygame.display.set_caption("Video Stream")
            else:
                self.thread = threading.Thread(target=self._pyqt5_video_loop, args=[self.kill_event])
            self.thread.start()
            self.started = True

    def _tkinter_video_loop(self, stop_event):
        root = tk.Tk()
        root.title("Video Stream")
        root.protocol("WM_DELETE_WINDOW", lambda: stop_event.set())
        cap = cv2.VideoCapture("udp://@0.0.0.0:11111")
        label = None
        while not stop_event.is_set():
            ret, frame = cap.read()
            print(frame)
            if ret == True:
                self.frame = frame
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img = ImageTk.PhotoImage(img)
                if label is None:
                    label = tk.Label(image=img)
                    label.image = img
                    label.pack()
                else:
                    label.configure(image=img)
                    label.image = img
            root.update()
        root.destroy()

    def _pygame_video_loop(self, stop_event):
        cap = cv2.VideoCapture("udp://0.0.0.0:11111", cv2.CAP_FFMPEG)
        while not stop_event.is_set():
            ret, frame = cap.read()
            if ret == True:
                self.frame = frame
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = np.rot90(frame)
                frame = np.flip(frame, 0)
                frame = pygame.surfarray.make_surface(frame)
                self.screen.blit(frame, (0, 0))

                pygame.display.update()

    def _pyqt5_video_loop(self, stop_event):
        cap = cv2.VideoCapture("udp://0.0.0.0:11111", cv2.CAP_FFMPEG)
        while not stop_event.is_set():
            ret, frame = cap.read()
            if ret == True:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, channel = frame.shape
                cv2.resize(frame, (640, 480), frame)
                window.video_out.setPixmap(QPixmap.fromImage(QImage(frame, width, height, QImage.Format_RGB888).rgbSwapped()))


    def stop(self):
        if self.started:
            self.kill_event.set()
            if platform.system() == "Darwin":
                pygame.quit()
            self.started = False
            sock.sendto('streamoff'.encode(encoding="utf-8"), tello_address)
            time.sleep(1)

    def get_frame(self):
        return copy.deepcopy(self.frame)

    def __del__(self):
        if self.started:
            self.stop()


# Global video instance
_video = None


def start_video():
    """ Starts the video stream """
    global _video
    if _video is None:
        _video = _VideoStream()
    _video.start()


def stop_video():
    """ Stops the video stream """
    global _video
    if _video is not None:
        _video.stop()
        del _video
        _video = None


def get_video_frame():
    """ Gets the last video frame from the video stream

        Returns:
            numpy.ndarray: The last frame the video stream reads
    """
    global _video
    if _video is not None:
        return _video.get_frame()


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
        global _end_flag
        try:
            _end_flag = True
            exec(self.code, globals())
        except AssertionError:
            _end_flag = True
        except:
            traceback.print_exc(file=sys.stdout)
        finally:
            self.thread().finished.emit()

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.menu_font = QFont("Arial", 10)
        self.setGeometry(0, 0, GetSystemMetrics(0) * 0.66, GetSystemMetrics(1) * 0.66)
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
        self.files_tabs.setTabsClosable(True)
        self.files_tabs.tabCloseRequested.connect(self.close_current_tab)
        self.files_tabs.resize(self.size().width(), 500)

        self.video_out = QLabel(self)
        self.video_out.setMaximumHeight(480)
        self.video_out.setMinimumHeight(480)
        self.video_out.setMaximumWidth(640)
        self.video_out.setMinimumWidth(640)
        self.video_out.setPixmap(QPixmap.fromImage(QImage("video_background.png")))

        sub_layout = QHBoxLayout()
        sub_layout.addWidget(self.files_tabs, 0)
        sub_layout.addWidget(self.video_out, 1)
        sub_layout.setSpacing(1)

        widget1 = QWidget()
        widget1.setLayout(sub_layout)

        self.run_button = QPushButton(self)
        self.run_button.setStyleSheet("background-color:green")
        self.run_button.setText("run")
        self.run_button.pressed.connect(self.run_file)

        self.end_button = QPushButton(self)
        self.end_button.setStyleSheet("background-color:red")
        self.end_button.setText("end")
        self.end_button.pressed.connect(self.terminate_thread)
        self.end_button.hide()

        sub_splitter = QSplitter(Qt.Horizontal)
        self.input_text_edit = QTextEdit()
        self.output_text_edit = QTextEdit()
        self.output_text_edit.setReadOnly(True)

        sub_splitter.addWidget(self.input_text_edit)
        sub_splitter.addWidget(self.output_text_edit)

        main_splitter = QSplitter(Qt.Vertical)
        main_splitter.addWidget(widget1)
        main_splitter.addWidget(sub_splitter)
        main_layout.addWidget(main_splitter)
        main_layout.addWidget(self.run_button)
        main_layout.addWidget(self.end_button)
        self.tabs = []
        self.setLayout(main_layout)

    def exec_ended(self):
        self.thrd.thread().quit()
        self.output_text_edit.setText(sys.stdout.getvalue())
        print("\nProcess finished with exit code 0")
        self.run_button.show()
        self.end_button.hide()

    def create_and_open_new_file(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "open/new file", "", "Py(*.py)")
        if file_path:
            with open(file_path, "w", encoding="UTF-8") as file:
                pass
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
        if self.tabs:
            with open(self.tabs[self.files_tabs.currentIndex()].file_path, mode="wt",
                    encoding="UTF-8") as file:
                file.write(self.tabs[self.files_tabs.currentIndex()].layout().itemAt(
                    0).widget().toPlainText())

    def run_file(self):
        if self.tabs:
            self.output_text_edit.clear()
            self.run_button.hide()
            self.end_button.show()
            path = self.tabs[self.files_tabs.currentIndex()].file_path
            if os.path.exists(path):
                self.save_file()

            stdin = io.StringIO(self.input_text_edit.toPlainText())
            self.stdout = io.StringIO()
            sys.stdin, sys.stdout = stdin, self.stdout

            data = self.reformat_code(path)

            self.thrd = CodeThread(data)
            thread = QThread(self.thrd)
            thread.started.connect(self.thrd.run_code)
            thread.finished.connect(self.exec_ended)
            self.thrd.moveToThread(thread)
            thread.start()

    def reformat_code(self, path):
        res = ""
        with open(path, encoding="utf-8") as file:
            for i in file:
                srng = i.rstrip() + "\n"
                if srng.lstrip().startswith('from') or srng.lstrip().startswith('import'):
                    continue
                elif srng.endswith(":\n"):
                    res += srng + " " * (len(
                        srng) - len(
                        srng.lstrip()) + 4) + "assert _end_flag, ('Остановленно пользователем')\n"
                else:
                    res += srng + " " * (len(
                        srng) - len(
                        srng.lstrip())) + "assert _end_flag, ('Остановленно пользователем')\n"
        print(res)
        return res

    def terminate_thread(self):
        global _end_flag
        _end_flag = False

    def add_start_function(self):
        try:
            text_edit = self.tabs[self.files_tabs.currentIndex()].layout().itemAt(0).widget()
            text_edit.insertPlainText("start()\n")
        except:
            pass

    def add_take_off_function(self):
        try:
            text_edit = self.tabs[self.files_tabs.currentIndex()].layout().itemAt(0).widget()
            text_edit.insertPlainText("takeoff()\n")
        except:
            pass

    def add_land_function(self):
        try:
            text_edit = self.tabs[self.files_tabs.currentIndex()].layout().itemAt(0).widget()
            text_edit.insertPlainText("land()\n")
        except:

            pass

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
