import pygetwindow as gw
import pyautogui as gui
import tkinter as tk
import time
import threading
from random import randint, random

from pprint import pprint

# it handles keyboard events even if gui is not focused on
from system_hotkey import SystemHotkey

from pynput import mouse
from pynput.mouse import Controller, Button


# https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread
class StoppableThread(threading.Thread):
    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        if self._stop_event.is_set():
            #print("stopped.")
            return True


def ShowWindow():
    print(gw.getAllTitles())

def GetWindow(name):
    if not (name in gw.getAllTitles()):
        print("[Error] No such a window exists")
        return -1
    
    return gw.getWindowsWithTitle(name)[0]

# GUI events
def event_1():
    print("1")

# kb_f1: get mouse position
def event_kb_f1():
    x, y = list(gui.position())
    e1["state"] = "normal"
    e2["state"] = "normal"

    e1.delete(0, 10)
    e2.delete(0, 10)
    e1.insert(0, string=x)
    e2.insert(0, string=y)

    e1["state"] = "disabled"
    e2["state"] = "disabled"

# kb_f2: click repeatedly
def event_kb_f2():
    global toggle_click
    global worker_thread

    if toggle_click:
        toggle_click = False
        worker_thread.stop()
        l3["text"] = "OFF"
        l3["background"] = "red"
        mbox.insert(1.0, "[INFO] Click macro disabled.\n")
        
    else:
        l3["text"] = "ON"
        l3["background"] = "green"

        toggle_click = True
        worker_thread = StoppableThread(target=worker_rep_click)
        worker_thread.start()
        mbox.insert(1.0, "[INFO] Click macro enabled.\n")

def event_kb_f3():
    global toggle_macro

    if toggle_macro:
        return

    mbox.insert(1.0, "[INFO] Macro started.\n")
    
    toggle_macro = True
    l4["text"] = "ON"
    l4["background"] = "green"
    
    try:
        repeat = int(e3.get())
    except:
        repeat = int(conf["PROSEKA_REPEAT"])
    
    try:
        repeat_rate = int(e4.get())
    except:
        repeat_rate = int(conf["PROSEKA_REPEAT"])

    if repeat_rate == 0:
        
        mbox.insert(1.0, "[INFO] Refill disabled.\n")


    e3["state"] = "disabled"
    e4["state"] = "disabled"

    for i in range(repeat): 
        msg = "[INFO] repeat: {}/{} ".format(i+1, repeat)

        if worker_thread.stopped():
            return
        start = time.time()

        time.sleep(randint(8, 10) + random())

        if worker_thread.stopped():
            return
        if repeat_rate != 0:
            macro_proseka(iter=i, refill=((i % repeat_rate == 0)))
        else:
            macro_proseka(iter=i)

        msg += "{} s.".format(time.time()-start)

        mbox.insert(1.0, msg + "\n")

    e3["state"] = "normal"
    e4["state"] = "normal"

    mbox.insert(1.0, "[INFO] Macro ended.\n")

    l4["text"] = "OFF"
    l4["background"] = "red"

    toggle_macro = False

def run_macro():
    global worker_thread
    
    worker_thread = StoppableThread(target=event_kb_f3)
    worker_thread.start()

# macro_once
# assumes 1280 x 720
def macro_proseka(iter=0, refill=False):
    a = GetWindow(conf["PLAYER_WINDOWNAME"])
    if a == -1:
        return

    x, y, w, h = a.left, a.top, a.width, a.height
    #print(x, y, w, h)
    
    notes_x = [x + a.left for x in [220, 400, 560, 720, 900, 1060]] # x offset: 220 | 400 | 560 | 720 | 900 | 1060
    note_y = 600 + a.top

    # coordinates
    button_yes = (1120 + a.left + randint(-50, 50), 700 + a.top + randint(-5, 5)) 
    button_goto_init = (880 + a.left + randint(-20, 20), 700 + a.top + randint(-5, 5))
    button_refill = (1130 + a.left + randint(-5, 5), 85 + a.top + randint(-5, 5))
    button_buy_crystal = (640 + a.left + randint(-50, 50), 480 + a.top + randint(-10, 10))
    button_buy = (800 + a.left + randint(-50, 50), 550 + a.top + randint(-10, 10))
    button_cancel = (500 + a.left + randint(-50, 50), 550 + a.top + randint(-10, 10))
    button_cancel_again = (440 + a.left + randint(-50, 50), 480 + a.top + randint(-10, 10))

    center = (640 + a.left + randint(-100, 100), 360 + a.top + randint(-30, 30))
    
   # print("> 곡 선택창...")
    time.sleep(random() + 2)
    move_and_click(button_yes)
    if worker_thread.stopped():
        return

    if refill:
        if worker_thread.stopped():
            return
        time.sleep(randint(3, 4) + random())
        move_and_click(button_refill)
        if worker_thread.stopped():
            return
        time.sleep(randint(3, 4) + random())
        move_and_click(button_buy_crystal)
        if worker_thread.stopped():
            return
        time.sleep(randint(3, 4) + random())
        move_and_click(button_buy)
        if worker_thread.stopped():
            return
        time.sleep(randint(3, 4) + random())
        move_and_click(button_buy_crystal)
        if worker_thread.stopped():
            return
        time.sleep(randint(3, 4) + random())
        move_and_click(button_cancel)
        if worker_thread.stopped():
            return
        time.sleep(randint(3, 4) + random())
        move_and_click(button_cancel_again)
        if worker_thread.stopped():
            return



    #print("> 최종 확인...")
    time.sleep(random()+randint(5, 8 ))
    move_and_click(button_yes)
    if worker_thread.stopped():
        return

    time.sleep(random() + randint(5, 8))

    runtime = 0
    while 1:
        t = random()/100 + 0.01
        time.sleep(t)
        move_and_click([notes_x[randint(0, 5)] + randint(-10, 10), 
                        note_y + randint(-30, 30)])
        if worker_thread.stopped():
            return
        runtime += t

        if runtime >= 90 + randint(0, 8) + random():
            break
    
   # print("> 연타 종료")
    

    time.sleep(randint(8, 10) + random())
   # print("> 아무 곳이나 클릭")
    move_and_click(center)
    if worker_thread.stopped():
        return
    
    time.sleep(randint(8, 10) + random())
   # print("> 보상 보러 가기")
    move_and_click(button_yes)
    if worker_thread.stopped():
        return
    
    time.sleep(randint(8, 10) + random())
   # print("> 라이브 보상 보러 가기")
    move_and_click(button_yes)
    if worker_thread.stopped():
        return

    time.sleep(randint(8, 10) + random())
   # print("> 이벤트 결과 보러 가기")
    move_and_click(button_yes)
    if worker_thread.stopped():
        return

    time.sleep(randint(8, 10) + random())
   # print("> 악곡 선택 가기")
    move_and_click(button_goto_init)
    if worker_thread.stopped():
        return

    time.sleep(randint(10, 12) + random())
    if worker_thread.stopped():
        return
   # print("> 러닝 종료. {}".format(str(iter) + "th run" if iter != 0 else ""))

    return
    time.sleep(int(s2.get()) / 10) # maybe 5.9 is optimal
    for note in tab:

        if note == "":
            print("skipped")
            pass
        else:
            n = int(note)
            if n < 10:
                move_and_click([notes_x[n-1]+randint(-10, 10), note_y+randint(-30, 30)])
                
                print("note {}".format(n-1))

            elif n >= 10:
                move_and_click([notes_x[(n-1)//10]+randint(-10, 10), note_y+randint(-30, 30)])
                move_and_click([notes_x[(n-1)%10]+randint(-10, 10), note_y+randint(-30, 30)])

                print("note {} {}".format((n-1)//10, (n-1)%10))
            else:
                print("what the...")

        time.sleep(0.5)

def move_and_click(pos, click=1):
    mouse_ctl.position = pos
    for i in range(click):
        mouse_ctl.click(Button.left)

# kb_esc: exit program
def event_kb_esc():
    win.destroy()

    if worker_thread:
        #print("worker stopped.")
        worker_thread.stop()

    exit()

def autoclick(pos):
    poses = [(0,0),
            (2440, 746),
            (2610, 746), 
            (2780, 746), 
            (2950, 746),
            (3110, 746),
            (3280, 746)]

    mouse_ctl.position = poses[pos]
    mouse_ctl.click(Button.left)
    



def update_click_rate(e):
    l1["text"] = s1.get()

def update_delay_rate(e):
    l2["text"] = str(int(s2.get()) / 10)


def worker_rep_click():
    while 1:
        tmp = time.time()
        while time.time() < tmp + 1/(s1.get() * 1.1):
            pass

        if worker_thread.stopped():
            break

        mouse_ctl.click(Button.left)


def SetHotkey():
    hk = SystemHotkey()
    hk.register(["f1",], callback=lambda event: event_kb_f1())
    hk.register(["f2",], callback=lambda event: event_kb_f2())
    hk.register(["f3",], callback=lambda event: run_macro())
    #hk.register(["t",], callback=lambda event: event_kb_f3()) # tmpt
    hk.register(["escape",], callback=lambda event: event_kb_esc())

    #hk.register(["a",], callback=lambda event: autoclick(1))
    #hk.register(["s",], callback=lambda event: autoclick(2))
    #hk.register(["d",], callback=lambda event: autoclick(3))
   # hk.register(["f",], callback=lambda event: autoclick(4))
   # hk.register(["g",], callback=lambda event: autoclick(5))
  #  hk.register(["h",], callback=lambda event: autoclick(6))

if __name__ == '__main__':
    ### Get conf ###
    conf = dict()

    try:
        with open("macro.config") as f: # TODO: pwd
            while 1:
                try:
                    k = f.readline().strip().split(' ')
                    conf[k[0]] = k[1]
                except:
                    break
    except:
        conf["PLAYER_WINDOWNAME"] = "proseka"
        conf["PROSEKA_REPEAT"] = 50
        conf["PROSEKA_REFILL_RATE"] = 2

    ### Global state ###
    toggle_click = False
    worker_thread = None
    toggle_macro = False

    ### hotkey init ###
    SetHotkey()

    ### controller init ###
    mouse_ctl = Controller()

    ### GUI init ###

    win = tk.Tk()
    win.geometry("250x500+200+200")
    win.title("macro")
    win.resizable(0, 0)

    tk.Label(win, text="Shortcuts", anchor="w").pack(fill="x")
    f0 = tk.Frame(win, relief="solid", bd=1)  

    tk.Label(f0, text="[F1]").grid(row=0, column=0, sticky=tk.W)
    tk.Label(f0, text="현재 마우스 위치 캡처").grid(row=0, column=1, sticky=tk.W)
    tk.Label(f0, text="[F2]").grid(row=1, column=0, sticky=tk.W)
    tk.Label(f0, text="반복 클릭 ON/OFF").grid(row=1, column=1, sticky=tk.W)
    tk.Label(f0, text="[F3]").grid(row=2, column=0, sticky=tk.W)
    tk.Label(f0, text="프로세카 매크로").grid(row=2, column=1, sticky=tk.W)
    tk.Label(f0, text="[ESC]").grid(row=3, column=0, sticky=tk.W)
    tk.Label(f0, text="프로그램 종료").grid(row=3, column=1, sticky=tk.W)
    
    b1 = tk.Button(f0, text="ON", command=run_macro)
    b1.grid(row=2, column=2, sticky=tk.W)
    #f0.columnconfigure(2, weight=1)

    f0.pack(fill="both")

    tk.Label(win, text="Mouse Position", anchor="w").pack(fill="x")
    f1 = tk.Frame(win, relief="solid", bd=1)

    e1 = tk.Entry(f1, width=5, state="disabled")
    e2 = tk.Entry(f1, width=5, state="disabled")
    tk.Label(f1, text="X", width=3).pack(side="left")
    e1.pack(side="left")
    tk.Label(f1, text="Y", width=3).pack(side="left")
    e2.pack(side="left")

    f1.pack(fill="both")

    tk.Label(win, text="Configuration", anchor="w").pack(fill="x")
    f2 = tk.Frame(win, relief="solid", bd=1)  

    s1 = tk.Scale(f2, from_=1, to=100, orient=tk.HORIZONTAL, showvalue=0, command=update_click_rate)
    s2 = tk.Scale(f2, from_=50, to=70, orient=tk.HORIZONTAL, showvalue=0, command=update_delay_rate)
    s1.set(50)

    l1 = tk.Label(f2, text="1")
    l2 = tk.Label(f2, text="5.0")

    e3 = tk.Entry(f2, width=5)
    e3.insert(0, string=conf["PROSEKA_REPEAT"])
    e4 = tk.Entry(f2, width=5)
    e4.insert(0, string=conf["PROSEKA_REFILL_RATE"])
    
    tk.Label(f2, text="클릭 속도").grid(row=0, column=0, sticky=tk.W)
    #tk.Label(f2, text="딜레이").grid(row=1, column=0, sticky=tk.W)
    tk.Label(f2, text="반복 횟수").grid(row=1, column=0, sticky=tk.W)
    tk.Label(f2, text="리필 주기").grid(row=2, column=0, sticky=tk.W)
    
    s1.grid(row=0, column=1)
    l1.grid(row=0, column=2)
    #s2.grid(row=1, column=1)
    #l2.grid(row=1, column=2)
    e3.grid(row=1, column=1, sticky=tk.W)
    e4.grid(row=2, column=1, sticky=tk.W)

    tk.Label(f2, text="clicks/s").grid(row=0, column=3, sticky=tk.W)
    #tk.Label(f2, text="s").grid(row=1, column=3, sticky=tk.W)

    f2.pack(fill='both')

    f3 = tk.Frame(win, relief="solid", bd=1)  
    tk.Label(win, text="Status", anchor="w").pack(fill="x")

    l3 = tk.Label(f3, text="OFF", background="red")
    l4 = tk.Label(f3, text="OFF", background="red")

    tk.Label(f3, text="반복 클릭 ").grid(row=0, column=0, sticky=tk.W)
    l3.grid(row=0, column=1, sticky=tk.W)
    tk.Label(f3, text="프로세카 매크로 ").grid(row=1, column=0, sticky=tk.W)
    l4.grid(row=1, column=1, sticky=tk.W)
    #tk.Label(f3, text="Message ").grid(row=2, column=0, sticky=tk.W)

    f3.pack(fill='both')

    tk.Label(win, text="Message", anchor="w").pack(fill="x")
    mbox = tk.Text(win, font=("Consolas", 8))
    mbox.pack(anchor="w")


    #win.bind("<Escape>", event_kb_esc)
    win.mainloop()
    #win.mainloop()
    #print("window terminated.")

    if worker_thread:
    #    print("worker stopped.")
        worker_thread.stop()

    #ShowWindow()
    #win = GetWindow("licking Speed Test - Riimu\'s Cookie Clicker Optimizer - Chrome")

    #test.get_wininfo(win)
    #test.click(500, 500)