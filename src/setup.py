import os
import sys
import time
import win32gui
import win32process
import json
import psutil
import ctypes
from pynput.keyboard import Key, Controller


SRC = sys.argv[0].split('src\\')[0] + 'src\\';

EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible

kbd = Controller()

file = open(SRC + 'config.json');
config = json.load(file);
process_name = "TouchDesigner.exe"

# Set the file paths
td_path = SRC + config['applications']['touchdesigner']
madmap_path = SRC + config['applications']['madmapper']

# Get the handle for the window with the desired process name
def setProcessForeground(hwnd):
    kbd.press(Key.alt)
    try:
        print(hwnd)
        win32gui.SetForegroundWindow(hwnd)
    except:
        return False
    finally:
        kbd.release(Key.alt)
        return True

def getProcessIDByName():
    global process_name
    pc_pids = []

    for proc in psutil.process_iter():
        if process_name in proc.name():
            pc_pids.append(proc.pid)

    return pc_pids

def get_hwnds_for_pid(pid):
    def callback(hwnd, hwnds):
        #if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)

        if found_pid == pid:
            hwnds.append(hwnd)
        return True
    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds 

def getWindowTitleByHandle(hwnd):
    length = GetWindowTextLength(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    GetWindowText(hwnd, buff, length + 1)
    return buff.value

def getProcessHandle():
    pids = getProcessIDByName()

    for i in pids:
        hwnds = get_hwnds_for_pid(i)
        for hwnd in hwnds:
            if IsWindowVisible(hwnd):
                return hwnd

# Open the files
os.startfile(td_path)
os.startfile(madmap_path)

# Wait for the files to open
time.sleep(1)

for i in range(12):
    tdHandle = getProcessHandle()
    if(tdHandle):
        setProcessForeground(tdHandle)
    time.sleep(5)


