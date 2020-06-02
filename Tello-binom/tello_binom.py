#
# Tello Python3 SDK 2.0 Functions Extended 

import socket
import re
import sys
import cv2
import threading
import sys
import copy
import numpy as np
import tkinter as tk
from PIL import ImageTk, Image
import platform
import time
import contextlib

with contextlib.redirect_stdout(None):
    import pygame

host = ''
port = 9000
locaddr = (host, port)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = ('192.168.10.1', 8889)
sock.bind(locaddr)


def start():
    sock.sendto('command'.encode(encoding="utf-8"), tello_address)
    time.sleep(5)


# Takeoff
def takeoff():
    sock.sendto('takeoff'.encode(encoding="utf-8"), tello_address)
    time.sleep(10)


# Move forward
def forward(cm):
    """Moves forward by a set distance

    Arguments:
        int: cm (20-500) -- The distance to move by in cm
    """
    assert (cm >= 20), "Distance is less than 20cm (valid range is 20cm-500cm)."
    assert (cm <= 500), "Distance is more than 500cm (valid range is 20cm-500cm)."
    order = 'forward ' + str(cm)
    sock.sendto(order.encode(encoding="utf-8"), tello_address)
    time.sleep(5)


# Move backward
def backward(cm):
    """Moves back by a set distance

    Arguments:
        int: cm (20-500) -- The distance to move by in cm
    """
    assert (cm >= 20), "Distance is less than 20cm (valid range is 20cm-500cm)."
    assert (cm <= 500), "Distance is more than 500cm (valid range is 20cm-500cm)."
    order = 'back ' + str(cm)
    sock.sendto(order.encode(encoding="utf-8"), tello_address)
    time.sleep(5)


# Move leftward
def left(cm):
    """Moves left by a set distance

    Arguments:
        int: cm (20-500) -- The distance to move by in cm
    """
    assert (cm >= 20), "Distance is less than 20cm (valid range is 20cm-500cm)."
    assert (cm <= 500), "Distance is more than 500cm (valid range is 20cm-500cm)."
    order = 'left ' + str(cm)
    sock.sendto(order.encode(encoding="utf-8"), tello_address)
    time.sleep(5)


# Move rightward
def right(cm):
    """Moves right by a set distance

    Arguments:
        int: cm (20-500) -- The distance to move by in cm
    """
    assert (cm >= 20), "Distance is less than 20cm (valid range is 20cm-500cm)."
    assert (cm <= 500), "Distance is more than 500cm (valid range is 20cm-500cm)."
    order = 'right ' + str(cm)
    sock.sendto(order.encode(encoding="utf-8"), tello_address)
    time.sleep(5)


# Move upward
def up(cm):
    """Moves up by a set distance

    Arguments:
        int: cm (20-500) -- The distance to move by in cm
    """
    assert (cm >= 20), "Distance is less than 20cm (valid range is 20cm-500cm)."
    assert (cm <= 500), "Distance is more than 500cm (valid range is 20cm-500cm)."
    order = 'up ' + str(cm)
    sock.sendto(order.encode(encoding="utf-8"), tello_address)
    time.sleep(5)


# Move downward
def down(cm):
    """Moves down by a set distance

    Arguments:
        int: cm (20-500) -- The distance to move by in cm
    """
    assert (cm >= 20), "Distance is less than 20cm (valid range is 20cm-500cm)."
    assert (cm <= 500), "Distance is more than 500cm (valid range is 20cm-500cm)."
    order = 'down ' + str(cm)
    sock.sendto(order.encode(encoding="utf-8"), tello_address)
    time.sleep(5)


# Rotate CW
def clockwise(deg):
    """Rotates ClockWise by a set degrees

    Arguments:
        int: deg (1-360) -- To turn CW
    """
    # while executed != 'ok':
    order = 'cw ' + str(deg)
    sock.sendto(order.encode(encoding="utf-8"), tello_address)
    time.sleep(5)


# Rotate CCW
def anticlockwise(deg):
    """Rotates CounterClockWise by a set degrees

    Arguments:
        int: deg (1-360) -- To turn CW
    """
    # while executed != 'ok':
    order = 'ccw ' + str(deg)
    sock.sendto(order.encode(encoding="utf-8"), tello_address)
    time.sleep(5)


# Flips
def flip_forward():
    """Performs a forward flip."""
    order = 'flip f'
    sock.sendto(order.encode(encoding="utf-8"), tello_address)
    time.sleep(5)


def flip_backward():
    order = 'flip b'
    sock.sendto(order.encode(encoding="utf-8"), tello_address)
    time.sleep(5)


def flip_left():
    order = 'flip l'
    sock.sendto(order.encode(encoding="utf-8"), tello_address)
    time.sleep(5)


def flip_right():
    order = 'flip r'
    sock.sendto(order.encode(encoding="utf-8"), tello_address)
    time.sleep(5)


# Set speed
def speed(cm):
    """Sets speed in cm per sec

    Arguments:
        int: cm per sec (10-100) 
    """
    assert (cm >= 10), "Speed is less than 10cm/s (valid range is 20cm-500cm/s)."
    assert (cm <= 100), "Speed is more than 100cm/s (valid range is 10cm-100cm/s)."
    order = 'speed ' + str(cm)
    sock.sendto(order.encode(encoding="utf-8"), tello_address)
    time.sleep(2)


def get_tof():
    """Gets the TOF sensor value
    Returns: TOF value in millimeters
    """
    order = 'tof?'
    sock.sendto(order.encode(encoding="utf-8"), tello_address)
    time.sleep(5)


def get_battery():
    """Gets the battery value
    Returns:
        int: The percentage of battery remaining
    """
    order = "battery?"
    sock.sendto(order.encode(encoding="utf-8"), tello_address)
    time.sleep(2)


def get_mission_pad():
    """Gets the current marker id
    Returns:
        int: The current marker id
    """
    order = "mon"
    sock.sendto(order.encode(encoding="utf-8"), tello_address)
    time.sleep(1)
    order = "mid?"
    sock.sendto(order.encode(encoding="utf-8"), tello_address)
    time.sleep(2)


def pads_on():
    order = "mon"
    sock.sendto(order.encode(encoding="utf-8"), tello_address)
    time.sleep(1)


def pads_off():
    order = "moff"
    sock.sendto(order.encode(encoding="utf-8"), tello_address)
    time.sleep(1)


# Move to x y z on speed s
def go(cm_x, cm_y, cm_z, speed):
    """Move to x y z on speed s

    Arguments:
        int: cm (20-500), int: cm (20-500), int: cm (20-500), int: %% (10-100)
    """
    assert (cm_x >= 20 or cm_y >= 20 or cm_z >= 20), "Distance is less than 20cm (valid range is 20cm-500cm)."
    assert (cm_x <= 500 or cm_y <= 500 or cm_z <= 500), "Distance is more than 500cm (valid range is 20cm-500cm)."
    order = 'go ' + str(cm_x) + ' ' + str(cm_y) + ' ' + str(cm_z) + ' ' + str(speed)
    sock.sendto(order.encode(encoding="utf-8"), tello_address)
    time.sleep(7)


def arc(cm_x1, cm_y1, cm_z1, cm_x2, cm_y2, cm_z2, speed):
    """Curve from x1 y1 z1 to x2 y2 z2 on speed s

    Arguments:
        int: cm (20-500), int: cm (20-500), int: cm (20-500), cm (20-500), int: cm (20-500), int: cm (20-500), int: %% (10-100)
    """
    # assert(cm_x1 >= 20 or cm_y1 >= 20 or cm_z1 >= 20 or cm_x2 >= 20 or cm_y2 >= 20 or cm_z2 >= 20), "Distance is less than 20cm (valid range is 20cm-500cm)."
    # assert(cm_x1 <= 500 or cm_y1 <= 500 or cm_z1 <= 500 or cm_x2 <= 500 or cm_y2 <= 500 or cm_z2 <= 500), "Distance is more than 500cm (valid range is 20cm-500cm)."
    order = 'curve ' + str(cm_x1) + ' ' + str(cm_y1) + ' ' + str(cm_z1) + ' ' + str(cm_x2) + ' ' + str(
        cm_y2) + ' ' + str(cm_z2) + ' ' + str(speed)
    sock.sendto(order.encode(encoding="utf-8"), tello_address)
    time.sleep(7)


# Land
def land():
    sock.sendto('land'.encode(encoding="utf-8"), tello_address)
    time.sleep(5)


def recv():
    count = 0
    while True:
        try:
            global executed
            executed = ''
            data, server = sock.recvfrom(1518)
            executed = data.decode(encoding="utf-8")
            print(data.decode(encoding="utf-8"))
        except Exception:
            print(Exception)
            break


def circle(r):
    arc(r, r, 0, 0, 2 * r, 0, 50)
    arc(-r, -r, 0, 0, -2 * r, 0, 50)


def loop(r):
    arc(r, 0, r, 2 * r, 0, 0, 50)
    arc(-1 * r, 0, -1 * r, -2 * r, 0, 0, 50)


def polygon(sides, dist):
    for i in range(sides):
        forward(dist)
        clockwise(round(360 / sides))


# recvThread create
recvThread = threading.Thread(target=recv)
recvThread.start()


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
            if platform.system() in ("Darwin", "Linux"):
                self.thread = threading.Thread(target=self._pygame_video_loop, args=[self.kill_event])
                pygame.init()
                self.screen = pygame.display.set_mode([640, 480])
                pygame.display.set_caption("Video Stream")
            else:
                self.thread = threading.Thread(target=self._cv2_video_loop, args=[self.kill_event])
            self.thread.start()
            self.started = True

    def _tkinter_video_loop(self, stop_event):
        root = tk.Tk()
        root.title("Video Stream")
        root.protocol("WM_DELETE_WINDOW", lambda: stop_event.set())
        cap = cv2.VideoCapture("udp://0.0.0.0:11111", cv2.CAP_FFMPEG)
        label = None
        while not stop_event.is_set():
            ret, frame = cap.read()
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
        running = True
        while not stop_event.is_set() and running:
            for event in pygame.event.get(pygame.QUIT, pump=True):
                running = False
                break
            ret, frame = cap.read()
            if ret == True:
                self.frame = frame
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = np.rot90(frame)
                frame = np.flip(frame, 0)
                frame = pygame.surfarray.make_surface(frame)
                self.screen.blit(frame, (0, 0))
                pygame.display.update()
        pygame.quit()

    def _cv2_video_loop(self, stop_event):
        root = tk.Tk()
        cap = cv2.VideoCapture("udp://0.0.0.0:11111", cv2.CAP_FFMPEG)
        _moved = False
        while not stop_event.is_set():
            ret, frame = cap.read()
            if ret == True:
                self.frame = frame
                frame = cv2.resize(frame, (int(frame.shape[1] // (2 ** 0.5)), int(frame.shape[0] // (2 ** 0.5))))
                cv2.imshow("video out", frame)
                if not _moved:
                    width = root.winfo_screenwidth()
                    height = root.winfo_screenheight()
                    cv2.moveWindow("video out", width - frame.shape[1], 0)
                    _moved = True

                cv2.waitKey(1)
                if cv2.getWindowProperty('video out', 0) < 0:
                    self.stop()
        cap.release()
        cv2.destroyAllWindows()

    def stop(self):
        if self.started:
            cv2.destroyAllWindows()
            self.kill_event.set()
            if platform.system() in ("Darwin", "Linux"):
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
