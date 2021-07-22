import tkinter as tk
from datetime import datetime, date, time, timedelta
import pygame

from PIL import ImageTk, Image
import keyboard

LARGE_FONT = ("Arial", 18, "bold")
BOLD_FONT = ("Arial", 18, "bold")
MEDIUM_FONT = ("Arial", 15)
SMALL_FONT = ("Arial", 10)
BUTTON_FONT = ("Arial", 13)
BUTTON_FONT2 = ("Arial", 12)

data = {}

f = open("data.txt", "r")
save = f.readlines()
for item in save:
    separator_index = item.find("=")
    label = item[:separator_index].strip()
    value = item[separator_index+1:].strip()
    if value.isnumeric():
        value = int(value)

    data[label] = value
f.close()

data["15min"] = 0
data["late"] = False
data["union"] = 0 #union = union_w = 20 min coupon
data["interval"] = (0, 30)
if data["start_sound"] == "True":
    data["start_sound"] = True
else:
    data["start_sound"] = False

pygame.mixer.init()

class TimerApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        global container
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, Cancel, Settings, Select):
            self.create_frame(F)
        self.show_frame(StartPage)

    def show_frame(self, controller):
        frame = self.frames[controller]
        frame.tkraise()

    def create_frame(self, F):
        frame = F(container, self)
        self.frames[F] = frame
        frame.grid(row=0, column=0, sticky="nsew")          


def inverse_mute():
    data["start_sound"] = not(data["start_sound"])
    if data["start_sound"] == True:
        mute_img = ImageTk.PhotoImage(file="sound_on.png")
    else:
        mute_img = ImageTk.PhotoImage(file="sound_off.png")
    rewrite("start_sound")
    mute.config(image=mute_img)
    mute.image=mute_img

def CreateStart(controller, t):
    data["rest_time"] = t
    controller.create_frame(Start)
    controller.create_frame(m15screen)
    controller.create_frame(m20screen)
    controller.show_frame(Start)

def late_start(controller, t):
    data["late"] = True
    CreateStart(controller, t)

def delete_timer(controller):
    delete_page(controller, Start)
    delete_page(controller, m15screen)
    delete_page(controller, m20screen)
    data["late"] = False
    data["15min"] = 0
    m15coupons.configure(text="15 min coupons: 0")

def define_time_diff(textBox):
    try:
        data["timediff"] = int(textBox.get())
        textBox.delete(0, "end")
        rewrite("timediff") #updating value in data.txt
    except:
        pass
    
    timediff.configure(text="Time difference: "+str(data["timediff"])+"시간")

def rewrite(keyword):
    f = open("data.txt", "r")
    save = f.readlines()
    lines = []
    for line in save:
        sline = line.strip().split("=")

        if sline[0].startswith(keyword):
            sline[1] = " "+str(data[keyword])+"\n"

            line = "=".join(sline)

        
        lines.append(line)
    f.close()
    f = open("data.txt", "w")
    for line in lines:
        f.write(line)
    f.close()

def define_coupon_num(textBox):
    try:
        data["15min"] = int(textBox.get())
        couponBox.delete(0, "end")
    except:
        pass
    m15coupons.configure(text="15 min coupons: "+str(data["15min"]))

def define_rest_time(textBox):
    try:
        data["rest_time"] = int(textBox.get())
        rest_time_box.delete(0, "end")
        rewrite("rest_time") #updating value in data.txt
    except:
        pass
    rest_time.configure(text="Rest time (sec): "+str(data["rest_time"]))

def define_union_w(textBox):
    try:
        data["union"] = int(textBox.get())
        union_w_box.delete(0, "end")
    except:
        pass
    union_w.configure(text="20 min coupons: "+str(data["union"]))

def delete_page(controller, page):
    controller.frames[page].grid_forget()
    controller.frames[page].destroy()
    controller.show_frame(StartPage)
    pygame.mixer.music.stop()
    data = {}

def delete_page2(event):
    #deletes page upon key press
    controller2.frames[Prep].grid_forget()
    controller2.frames[Prep].destroy()
    controller2.show_frame(StartPage)
    pygame.mixer.music.stop()
    data = {}

def define_interval(controller, textBox):
    try:
        n1 = int(textBox.get())
        n2 = n1+30
        data["interval"] = (n1, n2)
        interval_box.delete_page(0, "end")
    except:
        pass
    int_tuple = data["interval"]
    interval.configure(text="Intervals: "+str(int_tuple[0])+"/"+str(int_tuple[1]))

    controller.create_frame(PrepOrLate)

def test_start(controller):
    CreateStart(controller, data["rest_time"])

class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
       
        label = tk.Label(self, text="WAP timer", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
                
        global check
        check = tk.IntVar(value=data["event_map_buff"])
        check_button = tk.Checkbutton(self, text="event map buff", variable = check)
        check_button.place(x=0, y=420)

        quick_start_button = tk.Button(self, text="Quick Start",
                             command=lambda:controller.create_frame(Prep),
                             height=2, width=10, font=BUTTON_FONT)
        quick_start_button.pack(pady=40)

        start_button = tk.Button(self, text="Start",
                                 command=lambda:controller.show_frame(Select),
                                 height=2, width=10, font=BUTTON_FONT)
        start_button.pack(pady=20)

        test = tk.Button(self, text="test",
                             command=lambda:test_start(controller),
                             height=1, width=5, font=BUTTON_FONT)
        test.place(x=120, y=400)

        global m15coupons
        global couponBox

        m15coupons = tk.Label(self, text="15 min coupons: 0", font=MEDIUM_FONT)
        m15coupons.pack(pady=10, padx=10)
        
        couponBox = tk.Entry(self, width = 20) #Enter number of 15 min coupons
        couponBox.pack()
        
        couponButton = tk.Button(self, text="Enter",
                               command=lambda:define_coupon_num(couponBox))
        couponButton.pack()

        settings = ImageTk.PhotoImage(file="settings.png")
        settings_button = tk.Button(self, image=settings,
                                command=lambda:controller.show_frame(Settings),
                                borderwidth=0)
        settings_button.image=settings
        settings_button.place(x=245, y=395, height=50, width=50)

class Select(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        default_interval = tk.Button(self, text="00/30",
                                 command=lambda:controller.create_frame(PrepOrLate),
                                 height=2, width=10, font=BUTTON_FONT)
        default_interval.pack(pady=20)

        custom_interval = tk.Button(self, text="Custom Interval",
                                 command=lambda:controller.create_frame(Custom),
                                 height=2, width=15, font=BUTTON_FONT)
        custom_interval.pack(pady=20)
        
        
        start_button = tk.Button(self, text="Start Now",
                                 command=lambda:CreateStart(controller, 0),
                                 height=2, width=10, font=BUTTON_FONT)
        start_button.pack(pady=20)

        union_w = tk.Label(self, text="(no rest time)", font=SMALL_FONT)
        union_w.pack(padx=10)

        back_img = ImageTk.PhotoImage(file="back.png")
        leave_button = tk.Button(self, image=back_img,
                                command=lambda:controller.show_frame(StartPage),
                                borderwidth=0)
        leave_button.image = back_img
        leave_button.pack(pady=40)

class Settings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global timediff
        global rest_time
        global rest_time_box
        global union_w
        global union_w_box
        
        timediff = tk.Label(self, text="Time difference: "+str(data["timediff"])+" Hours", font=MEDIUM_FONT)
        timediff.pack(pady=10, padx=10)
        
        textBox = tk.Entry(self, width = 20)
        textBox.pack()
        
        buttonTime = tk.Button(self, text="Enter",
                               command=lambda:define_time_diff(textBox))
        buttonTime.pack()

        rest_time = tk.Label(self, text="Rest time (sec): "+str(data["rest_time"]), font=MEDIUM_FONT)
        rest_time.pack(pady=10, padx=10)
        
        rest_time_box = tk.Entry(self, width = 20)
        rest_time_box.pack()
        
        enter_rest_time = tk.Button(self, text="Enter",
                               command=lambda:define_rest_time(rest_time_box))
        enter_rest_time.pack()

        union_w = tk.Label(self, text="20 min coupons: 0", font=MEDIUM_FONT)
        union_w.pack(pady=10, padx=10)
        
        union_w_box = tk.Entry(self, width = 20)
        union_w_box.pack()
        
        enter_union_w = tk.Button(self, text="Enter",
                               command=lambda:define_union_w(union_w_box))
        enter_union_w.pack()
        
        global mute
        
        if data["start_sound"] == True:
            mute_img = ImageTk.PhotoImage(file="sound_on.png")
        else:
            mute_img = ImageTk.PhotoImage(file="sound_off.png")
        mute = tk.Button(self, image=mute_img,
                                command=lambda:inverse_mute(),
                                borderwidth=0) #button for mute/unmute of starting sound
        mute.image=mute_img
        mute.pack(pady=20)

        back_img = ImageTk.PhotoImage(file="back.png")
        leave_button = tk.Button(self, image=back_img,
                                command=lambda:controller.show_frame(StartPage),
                                borderwidth=0)
        leave_button.image = back_img

        leave_button.pack(pady=10)

class Custom(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        global interval
        interval = tk.Label(self, text="Interval (the smaller number):", font=MEDIUM_FONT)
        interval.pack(pady=10, padx=10)
        
        global interval_box
        interval_box = tk.Entry(self, width = 20)
        interval_box.pack()

        enter_rest_time = tk.Button(self, text="Enter",
                               command=lambda:define_interval(controller, interval_box))
        enter_rest_time.pack()

class PrepOrLate(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        start_button = tk.Button(self, text="Preset",
                                 command=lambda:controller.create_frame(Prep),
                                 height=2, width=10, font=BUTTON_FONT)
        start_button.pack(pady=40)

        start_button = tk.Button(self, text="Late",
                                 command=lambda:late_start(controller, data["rest_time"]),
                                 height=2, width=10, font=BUTTON_FONT)
        start_button.pack(pady=20)

class Prep(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        global controller2
        controller2 = controller
        
        label = tk.Label(self, text="Time left: ", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        self.label2 = tk.Label(self, text="", font = ('Arial', 15))
        self.label2.pack()

        back_img = ImageTk.PhotoImage(file="back.png")
        leave_button = tk.Button(self, image=back_img,
                                command=lambda:controller.show_frame(StartPage),
                                borderwidth=0)
        leave_button.image = back_img
        leave_button.pack(pady=40)

        self.bind("<Escape>", delete_page2)
        self.focus_set()

        self.count_down()
        
    def count_down(self):
        now = datetime.now()
        inter = data["interval"]

        current = now.minute * 60 + now.second
        if current == inter[0]*60 or current == inter[1]*60:
            CreateStart(self.controller, data["rest_time"])
            return 0
        
        if now.minute > inter[1]:
            left = (60+inter[0])*60-current
            
        if now.minute < inter[0] and now.minute >= 0:
            left = inter[0]*60 - current

        if now.minute > inter[0] and now.minute < inter[1]:
            left = inter[1]*60-current

        mins = str(left // 60)
        secs = str(left % 60)

        if len(mins) == 1:
            mins = "0"+mins
        if len(secs) == 1:
            secs = "0"+secs
        rem = mins+":"+secs
        
        self.label2.configure(text=rem)
        
        self.after(100, self.count_down)

class Cancel(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Terminate timer?", font=LARGE_FONT)
        label.pack()
        cancel = tk.Button(self, text="Yes",
                           command=lambda:delete_timer(controller),
                           height=3, width=6, font=BUTTON_FONT)
        cancel.place(x=60, y=160, height=80, width=80)
        cancel = tk.Button(self, text="No",
                           command=lambda:controller.show_frame(Start),
                           height=3, width=6, font=BOLD_FONT)
        cancel.place(x=160, y=160, height=80, width=80)

class m20screen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        if data["union"] > 0:
            self.seconds_left = 20*60
            data["union"] -= 1
        
        now = datetime.now()
        if data["late"] == True:
            inter = data["interval"]
            current = now.minute * 60 + now.second

            if now.minute > inter[1]: #working out time left to the next interval
                self.background = (60+inter[0])*60-current
            if now.minute < inter[0] and now.minute >= 0:
                self.background = inter[0]*60 - current
            if now.minute > inter[0] and now.minute < inter[1]:
                self.background = inter[1]*60-current
        else:
            self.background = 30*60 

        right_arrow = tk.Button(self, text=">",
                                command=lambda:controller.show_frame(Start), font=LARGE_FONT)
        right_arrow.place(x=250, y=160, height=80, width=50)

        left_arrow = tk.Button(self, text="<",
                                command=lambda:controller.show_frame(m15screen), font=LARGE_FONT)
        left_arrow.place(x=0, y=160, height=80, width=50)

        home = ImageTk.PhotoImage(file="home.png")
        home_button = tk.Button(self, image=home,
                                command=lambda:controller.show_frame(Start),
                                borderwidth=0)
        home_button.image=home
        home_button.place(x=130, y=400, height=50, width=50)

        union_label = tk.Label(self, text="Next 20 min:", font = LARGE_FONT)
        union_label.pack(padx=10, pady=10)
        self.label = tk.Label(self, text="", font = ('Arial', 15))
        self.label.pack()

        label_num = tk.Label(self, text="20 min coupons left:", font = LARGE_FONT)
        label_num.pack(padx=10, pady=10)
        self.label2 = tk.Label(self, text=data["union"], font = ('Arial', 15))
        self.label2.pack()

        plus = tk.Button(self, text="+",
                         command=lambda:self.add20(), font=BUTTON_FONT)
        plus.place(x=115, y=170, height=30, width=30)

        minus = tk.Button(self, text="-",
                         command=lambda:self.minus20(), font=BUTTON_FONT)
        minus.place(x=155, y=170, height=30, width=30)

        preset_img = ImageTk.PhotoImage(file="hourglass.png")
        preset = tk.Button(self, image=preset_img, command=lambda:self.preset())
        preset.place(x=75, y=230, height=70, width=70)
        preset.image = preset_img

        preset_desc = tk.Label(self, text="preset", font = ('Arial', 13))
        preset_desc.place(x=85, y=310)

        arrow_img = ImageTk.PhotoImage(file="arrow.png")
        start = tk.Button(self, image=arrow_img, command=lambda:self.start_now())
        start.place(x=155, y=230, height=70, width=70)
        start.image = arrow_img

        start_desc = tk.Label(self, text="start", font = ('Arial', 13))
        start_desc.place(x=170, y=310)

        cancel = tk.Button(self, text="X",
                           command=lambda:controller.show_frame(Cancel), font=BUTTON_FONT)
        cancel.place(x=0, y=0)

        self.update()

    def start_now(self):
        if data["union"] > 0:
            data["union"] -= 1
            self.label2.configure(text=str(data["union"]))
            self.seconds_left = 20*60
    
    def preset(self):
        if data["union"] > 0:
            self.seconds_left = self.background % (20 * 60)
    
    def add20(self):
        data["union"] += 1
        self.label2.configure(text=str(data["union"]))

    def minus20(self):
        if data["union"] > 0:
            data["union"] -= 1
            self.label2.configure(text=str(data["union"]))

    def seconds_left_to_time(self, seconds_left):
        time = []
        
        if seconds_left//60 >= 10:
            time.append(str(seconds_left//60))
        else:
            time.append("0"+str(seconds_left//60))
        if seconds_left%60 >= 10:
            time.append(str(seconds_left%60))
        else:
            time.append("0"+str(seconds_left%60))
        return time

    def update(self):
        try:
            self.background -= 1
            if self.background == 0:
                self.background = 30*60

            if self.seconds_left > 0:
                self.seconds_left -= 1
                time = self.seconds_left_to_time(self.seconds_left)
                self.label.configure(text=time[0]+":"+time[1])

            if self.seconds_left == 1:
                pygame.mixer.music.load("coffin.mp3")
                pygame.mixer.music.play(loops=0)

            if self.seconds_left == 0:
                if data["union"] > 0:
                    self.seconds_left = 20*60
                    data["union"] -= 1
                    self.label2.configure(text=data["union"])

        except:
            self.label.configure(text="null")
        
        self.after(999, self.update)
            
class m15screen(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        if data["15min"] > 0:
            self.seconds_left = 15*60
            data["15min"] -= 1
        
        now = datetime.now()
        if data["late"] == True:
            inter = data["interval"]
            current = now.minute * 60 + now.second

            if now.minute > inter[1]: #working out time left to the next interval
                self.background = (60+inter[0])*60-current
            if now.minute < inter[0] and now.minute >= 0:
                self.background = inter[0]*60 - current
            if now.minute > inter[0] and now.minute < inter[1]:
                self.background = inter[1]*60-current
        else:
            self.background = 30*60 

        label_15 = tk.Label(self, text="Next 15 min:", font = LARGE_FONT)
        label_15.pack(padx=10, pady=10)
        self.label5 = tk.Label(self, text="", font = ('Arial', 15))
        self.label5.pack()

        label_num = tk.Label(self, text="15 min coupons left:", font = LARGE_FONT)
        label_num.pack(padx=10, pady=10)
        self.label6 = tk.Label(self, text=data["15min"], font = ('Arial', 15))
        self.label6.pack()

        self.labelb = tk.Label(self, text="", font = ('Arial', 15))
        self.labelb.pack(pady=45)

        plus = tk.Button(self, text="+",
                         command=lambda:self.add15(), font=BUTTON_FONT)
        plus.place(x=115, y=170, height=30, width=30)

        minus = tk.Button(self, text="-",
                         command=lambda:self.minus15(), font=BUTTON_FONT)
        minus.place(x=155, y=170, height=30, width=30)

        #여기에 15분 예약/지각 기능 추가
        #anchor
        preset_img = ImageTk.PhotoImage(file="hourglass.png")
        preset = tk.Button(self, image=preset_img, command=lambda:self.preset())
        preset.place(x=75, y=230, height=70, width=70)
        preset.image = preset_img

        preset_desc = tk.Label(self, text="preset", font = ('Arial', 13))
        preset_desc.place(x=85, y=310)

        arrow_img = ImageTk.PhotoImage(file="arrow.png")
        start = tk.Button(self, image=arrow_img, command=lambda:self.start_now())
        start.place(x=155, y=230, height=70, width=70)
        start.image = arrow_img

        start_desc = tk.Label(self, text="start", font = ('Arial', 13))
        start_desc.place(x=170, y=310)

        left_arrow = tk.Button(self, text="<",
                                command=lambda:controller.show_frame(Start), font=LARGE_FONT)
        left_arrow.place(x=0, y=160, height=80, width=50)

        right_arrow = tk.Button(self, text=">",
                                command=lambda:controller.show_frame(m20screen), font=LARGE_FONT)
        right_arrow.place(x=250, y=160, height=80, width=50)

        home = ImageTk.PhotoImage(file="home.png")
        home_button = tk.Button(self, image=home,
                                command=lambda:controller.show_frame(Start),
                                borderwidth=0)
        home_button.image=home
        home_button.place(x=130, y=400, height=50, width=50)

        cancel = tk.Button(self, text="X",
                           command=lambda:controller.show_frame(Cancel), font=BUTTON_FONT)
        cancel.place(x=0, y=0)

        self.update()
    
    def start_now(self):
        if data["15min"] > 0:
            data["15min"] -= 1
            self.label6.configure(text=str(data["15min"]))
            self.seconds_left = 15*60

    def preset(self):
        if data["15min"] > 0:
            self.seconds_left = self.background % (15*60)

    def add15(self):
        data["15min"] += 1
        self.label6.configure(text=str(data["15min"]))

    def minus15(self):
        if data["15min"] > 0:
            data["15min"] -= 1
            self.label6.configure(text=str(data["15min"]))

    def seconds_left_to_time(self, seconds_left):
        time = []
        
        if seconds_left//60 >= 10:
            time.append(str(seconds_left//60))
        else:
            time.append("0"+str(seconds_left//60))
        if seconds_left%60 >= 10:
            time.append(str(seconds_left%60))
        else:
            time.append("0"+str(seconds_left%60))
        return time

    def update(self):
        try:
            self.background -= 1
            if self.background == 0:
                self.background = 30*60

            if self.seconds_left > 0:
                self.seconds_left -= 1
                time = self.seconds_left_to_time(self.seconds_left)
                self.label5.configure(text=time[0]+":"+time[1])

            if self.seconds_left == 3:
                pygame.mixer.music.load("SadRomance.mp3")
                pygame.mixer.music.play(loops=0)

            if self.seconds_left == 0:
                if data["15min"] > 0:
                    self.seconds_left = 15*60
                    data["15min"] -= 1
                    self.label6.configure(text=data["15min"])

        except:
            self.label5.configure(text="null")
        
        self.after(999, self.update)

class Start(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        if data["start_sound"] == True:
            pygame.mixer.music.load("1LapStartShort.mp3")
            pygame.mixer.music.play(loops=0)
        now = datetime.now()

        if data["late"] == True:
            inter = data["interval"]
            current = now.minute * 60 + now.second

            if now.minute > inter[1]: #working out time left to the next interval
                self.seconds_left = (60+inter[0])*60-current
            if now.minute < inter[0] and now.minute >= 0:
                self.seconds_left = inter[0]*60 - current
            if now.minute > inter[0] and now.minute < inter[1]:
                self.seconds_left = inter[1]*60-current
        else:
            self.seconds_left = 30*60 

        self.seconds_left2 = data["booster"] 
        self.set_count = 1       
        
        label = tk.Label(self, text="Next 30 min: ", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        self.label2 = tk.Label(self, text="", font = ('Arial', 15))
        self.label2.pack()

        label = tk.Label(self, text="Set: ", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        self.label3 = tk.Label(self, text="1/4", font = ('Arial', 15))
        self.label3.pack()
            
        label = tk.Label(self, text="Booster: ", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        self.label4 = tk.Label(self, text="", font = ('Arial', 15))
        self.label4.pack()

        global reroll
        reroll = ImageTk.PhotoImage(file="reroll.png")
        reroll_button = tk.Button(self, image=reroll,
                            command=lambda:self.restart(), borderwidth=0)
        reroll_button.image = reroll
        reroll_button.pack()

        right_arrow = tk.Button(self, text=">",
                                command=lambda:controller.show_frame(m15screen), font=LARGE_FONT)
        right_arrow.place(x=250, y=160, height=80, width=50)

        left_arrow = tk.Button(self, text="<",
                                command=lambda:controller.show_frame(m20screen), font=LARGE_FONT)
        left_arrow.place(x=0, y=160, height=80, width=50)
        
        cancel = tk.Button(self, text="Exit",
                           command=lambda:controller.show_frame(Cancel), font=LARGE_FONT,
                           height = 10, width = 10)
        cancel.pack(pady=40)

        cancel = tk.Button(self, text="X",
                           command=lambda:controller.show_frame(Cancel), font=BUTTON_FONT)
        cancel.place(x=0, y=0)

        self.update()
        if check.get() == 1:
            self.event_map_alert()
    
    def restart(self, event=None):
        self.seconds_left2 = data["booster"] 
        time2 = self.seconds_left_to_time(self.seconds_left2)
        
        self.label4.configure(text=time2[0]+":"+time2[1])
        pygame.mixer.music.load("SymbolRestart.mp3")
        pygame.mixer.music.play(loops=0)
    
    def update(self):
        self.seconds_left -= 1
        self.seconds_left2 -= 1
        
        time = self.seconds_left_to_time(self.seconds_left)
        time2 = self.seconds_left_to_time(self.seconds_left2)
        if self.seconds_left <= data["rest_time"] and data["rest_time"] > 0:
            self.label2.configure(text=time[0]+":"+time[1], fg="red")
        elif self.seconds_left <= 3:
            self.label2.configure(text=time[0]+":"+time[1], fg="red")
        else:
            self.label2.configure(text=time[0]+":"+time[1], fg="black")
        self.label4.configure(text=time2[0]+":"+time2[1])

        now = datetime.now()
            
        if self.seconds_left2 == 3:
            pygame.mixer.music.load("Symbol.mp3")
            pygame.mixer.music.play(loops=0)
        if self.seconds_left2 == 0:
            self.seconds_left2 = data["booster"] 
        if self.seconds_left == data["rest_time"]+3:
            pygame.mixer.music.load("1LapBreak.mp3")
            pygame.mixer.music.play(loops=0)
        if self.seconds_left == 3:
            pygame.mixer.music.load("1LapStart.mp3")
            pygame.mixer.music.play(loops=0)
        if self.seconds_left == 0:
            if self.set_count == 4:
                self.set_count = 0
                pygame.mixer.music.load("4Laps.mp3")
                pygame.mixer.music.play(loops=0)
            if now.hour-data["timediff"] in (11, 6, 8) and now.minute==30:
                self.seconds_left = 29*60
                self.label2.configure(text="29:00")
            else:
                self.label2.configure(text="30:00", fg="black")
                self.seconds_left = 30*60 
            
            self.set_count += 1
            self.label3.configure(text=str(self.set_count)+"/4")

        self.after(999, self.update)
        
    def seconds_left_to_time(self, seconds_left):
        time = []
        
        if seconds_left//60 >= 10:
            time.append(str(seconds_left//60))
        else:
            time.append("0"+str(seconds_left//60))
        if seconds_left%60 >= 10:
            time.append(str(seconds_left%60))
        else:
            time.append("0"+str(seconds_left%60))
        return time
    
    def event_map_alert(self):
        now = datetime.now()
        if now.hour % 2 == 1:
           if now.minute == 29 or now.minute == 39:
               if now.second == 20:
                    pygame.mixer.music.load("dingdong.mp3")
                    pygame.mixer.music.play(loops=0)
                    

        self.after(999, self.event_map_alert)
                   
def main():
    app = TimerApp()
    app.title('WAP timer')
    app.iconbitmap("icon.ico")
    app.geometry('300x450+475+150')
    app.mainloop()    

main()













