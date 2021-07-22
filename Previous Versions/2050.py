import tkinter as tk
from datetime import datetime, date, time, timedelta
import pygame
from PIL import ImageTk, Image

LARGE_FONT = ("메이플스토리", 18)
BOLD_FONT = ("메이플스토리", 18, "bold")
MEDIUM_FONT = ("메이플스토리", 15)
SMALL_FONT = ("메이플스토리", 10)
BUTTON_FONT = ("메이플스토리", 13)
BUTTON_FONT2 = ("메이플스토리", 12)

data = {}
sim = [200]
data["timediff"] = 4
data["time"] = 40
data["15min"] = 0
data["late"] = False
data["union"] = 0
pygame.mixer.init()

from datetime import datetime

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
        

def CreateStart(controller, t):
    data["time"] = t
    controller.create_frame(Start)
    controller.create_frame(m15screen)
    controller.create_frame(control_room)
    controller.show_frame(Start)

def late(controller):
    data["late"] = True
    CreateStart(controller, 40)

def delete_timer(controller):
    delete(controller, Start)
    delete(controller, m15screen)
    delete(controller, control_room)
    data["late"] = False
    data["15min"] = 0
    m15coupons.configure(text="15분 갯수: 0")

def define_time_diff(textBox):
    try:
        data["timediff"] = int(textBox.get())
        textBox.delete(0, "end")
    except:
        pass
    timediff.configure(text="시차: "+str(data["timediff"])+"시간")

def define_coupon_num(textBox):
    try:
        data["15min"] = int(textBox.get())
        couponBox.delete(0, "end")
    except:
        pass
    m15coupons.configure(text="15분 갯수: "+str(data["15min"]))

def define_rest_time(textBox):
    try:
        data["time"] = int(textBox.get())
        rest_time_box.delete(0, "end")
    except:
        pass
    rest_time.configure(text="경뿌 여유 시간(초): "+str(data["time"]))

def define_union_w(textBox):
    try:
        data["union"] = int(textBox.get())
        union_w_box.delete(0, "end")
    except:
        pass
    union_w.configure(text="유부 쿠폰 갯수: "+str(data["union"]))

def delete(controller, page):
    controller.frames[page].grid_forget()
    controller.frames[page].destroy()
    controller.show_frame(StartPage)
    pygame.mixer.music.stop()
    data = {}


class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        """
        bg = ImageTk.PhotoImage(file="arcana.png")

        bg_label = tk.Label(self, image=bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.image = bg
        """
        
        label = tk.Label(self, text="재획 타이머", font=LARGE_FONT
                         )
        label.pack(pady=10, padx=10)

        """
        bg_img = Image.open("arcana.png").convert("RGBA")
        title_img = Image.open("title2.png").convert("RGBA")
        c = Image.alpha_composite(bg_img, title_img)
        title = ImageTk.PhotoImage(c)
        title_label = tk.Label(self, image=title)
        title_label.image=title
        title_label.pack()
        """


        button29 = tk.Button(self, text="빠른 시작",
                             command=lambda:controller.create_frame(Prep),
                             height=2, width=10, font=BUTTON_FONT)
        button29.pack(pady=40)

        start_button = tk.Button(self, text="시작",
                                 command=lambda:controller.show_frame(Select),
                                 height=2, width=10, font=BUTTON_FONT)
        start_button.pack(pady=20)

        test = tk.Button(self, text="test",
                             command=lambda:CreateStart(controller, 40),
                             height=1, width=5, font=BUTTON_FONT)
        test.place(x=120, y=400)

        global m15coupons
        global couponBox

        m15coupons = tk.Label(self, text="15분 갯수: 0", font=MEDIUM_FONT)
        m15coupons.pack(pady=10, padx=10)
        
        couponBox = tk.Entry(self, width = 20)
        couponBox.pack()
        
        couponButton = tk.Button(self, text="확인",
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
        
        start_button = tk.Button(self, text="예약",
                                 command=lambda:controller.create_frame(Prep),
                                 height=2, width=10, font=BUTTON_FONT)
        start_button.pack(pady=40)

        start_button = tk.Button(self, text="지각",
                                 command=lambda:late(controller),
                                 height=2, width=10, font=BUTTON_FONT)
        start_button.pack(pady=20)

        start_button = tk.Button(self, text="바로 시작",
                                 command=lambda:CreateStart(controller, 0),
                                 height=2, width=10, font=BUTTON_FONT)
        start_button.pack(pady=20)

        start_button = tk.Button(self, text="뒤로가기",
                                 command=lambda:controller.show_frame(StartPage),
                                 height=2, width=10, font=BUTTON_FONT)
        start_button.pack(pady=40)

class Settings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global timediff
        global rest_time
        global rest_time_box
        global union_w
        global union_w_box
        
        timediff = tk.Label(self, text="시차: 4시간", font=MEDIUM_FONT)
        timediff.pack(pady=10, padx=10)
        
        textBox = tk.Entry(self, width = 20)
        textBox.pack()
        
        buttonTime = tk.Button(self, text="확인",
                               command=lambda:define_time_diff(textBox))
        buttonTime.pack()

        rest_time = tk.Label(self, text="경뿌 여유 시간(초): 40", font=MEDIUM_FONT)
        rest_time.pack(pady=10, padx=10)
        
        rest_time_box = tk.Entry(self, width = 20)
        rest_time_box.pack()
        
        enter_rest_time = tk.Button(self, text="확인",
                               command=lambda:define_rest_time(rest_time_box))
        enter_rest_time.pack()

        union_w = tk.Label(self, text="유부 쿠폰 갯수: 0", font=MEDIUM_FONT)
        union_w.pack(pady=10, padx=10)
        
        union_w_box = tk.Entry(self, width = 20)
        union_w_box.pack()
        
        enter_union_w = tk.Button(self, text="확인",
                               command=lambda:define_union_w(union_w_box))
        enter_union_w.pack()


        leave_button = tk.Button(self, text="나가기",
                             command=lambda:controller.show_frame(StartPage),
                             height=2, width=10, font=BUTTON_FONT)
        leave_button.pack(pady=40)
        

class Prep(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #self.bind("<c>", print("hi"))
        
        label = tk.Label(self, text="남은 시간: ", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        self.label2 = tk.Label(self, text="", font = ('메이플스토리', 15))
        self.label2.pack()

        cancel = tk.Button(self, text="취소", font=BUTTON_FONT,
                           command=lambda:delete(controller, Prep))
        cancel.pack(pady=40)
        
        self.update30()
        
    def update30(self):
        now = datetime.now()

        current = now.minute * 60 + now.second
        if current == 0:
            CreateStart(self.controller, 40)
            return 0
        
        if now.minute >= 30:
            left = 60*60 - current 
        else:
            left = 30*60 - current 
        mins = str(left // 60)
        secs = str(left % 60)
        if len(mins) == 1:
            mins = "0"+mins
        if len(secs) == 1:
            secs = "0"+secs
        rem = mins+":"+secs
        
        self.label2.configure(text=rem)
        
        if left == 0:
            CreateStart(self.controller)
            return 0
        
        self.after(100, self.update30)


class Cancel(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="정말 취소하시겠습니까?", font=LARGE_FONT)
        label.pack()
        cancel = tk.Button(self, text="예",
                           command=lambda:delete_timer(controller),
                           height=3, width=6, font=BUTTON_FONT)
        cancel.pack(padx=30, pady=1, side=tk.LEFT)
        cancel = tk.Button(self, text="아니오",
                           command=lambda:controller.show_frame(Start),
                           height=3, width=6, font=BUTTON_FONT)
        cancel.pack(padx=30, pady=1, side=tk.RIGHT)

class control_room(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        if data["union"] > 0:
            self.seconds_left = 20*60
            data["union"] -= 1
        
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

        union_label = tk.Label(self, text="다음 유부:", font = LARGE_FONT)
        union_label.pack(padx=10, pady=10)
        self.label = tk.Label(self, text="", font = ('메이플스토리', 15))
        self.label.pack()

        label_num = tk.Label(self, text="남은 유부:", font = LARGE_FONT)
        label_num.pack(padx=10, pady=10)
        self.label2 = tk.Label(self, text=data["union"], font = ('메이플스토리', 15))
        self.label2.pack()

        exit_button = tk.Button(self, text="종료", font=BUTTON_FONT,
                                command=lambda:controller.show_frame(Cancel))
        exit_button.place(x=130, y=200, height=50, width=50)

        self.update()

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
        
        label_15 = tk.Label(self, text="다음 15경쿠:", font = LARGE_FONT)
        label_15.pack(padx=10, pady=10)
        self.label5 = tk.Label(self, text="", font = ('메이플스토리', 15))
        self.label5.pack()

        label_num = tk.Label(self, text="남은 15경쿠:", font = LARGE_FONT)
        label_num.pack(padx=10, pady=10)
        self.label6 = tk.Label(self, text=data["15min"], font = ('메이플스토리', 15))
        self.label6.pack()

        plus = tk.Button(self, text="+",
                         command=lambda:self.add15(), font=BUTTON_FONT)
        plus.place(x=115, y=170, height=30, width=30)

        minus = tk.Button(self, text="-",
                         command=lambda:self.minus15(), font=BUTTON_FONT)
        minus.place(x=155, y=170, height=30, width=30)

        #여기에 15분 예약/지각 기능 추가

        left_arrow = tk.Button(self, text="<",
                                command=lambda:controller.show_frame(Start), font=LARGE_FONT)
        left_arrow.place(x=0, y=160, height=80, width=50)

        right_arrow = tk.Button(self, text=">",
                                command=lambda:controller.show_frame(control_room), font=LARGE_FONT)
        right_arrow.place(x=250, y=160, height=80, width=50)

        home = ImageTk.PhotoImage(file="home.png")
        home_button = tk.Button(self, image=home,
                                command=lambda:controller.show_frame(Start),
                                borderwidth=0)
        home_button.image=home
        home_button.place(x=130, y=400, height=50, width=50)

        self.update()

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
        pygame.mixer.music.load("1LapStartShort.mp3")
        pygame.mixer.music.play(loops=0)
        now = datetime.now()

        if data["late"] == True:
            if now.minute > 50:
                self.seconds_left = 80*60-now.minute*60
            if now.minute < 20 and now.minute > 0:
                self.seconds_left = 20*60 - now.minute*60
            else:
                self.seconds_left = 50*60-now.minute*60
            
        
        else:
            self.seconds_left = 30*60 #change to 30*60

        self.seconds_left2 = sim[0] #change to sim[0]
        self.set_count = 1
        """
        bg = ImageTk.PhotoImage(file="arcana2.png")

        bg_label = tk.Label(self, image=bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.image = bg
        """
        
        label = tk.Label(self, text="다음 경쿠: ", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        self.label2 = tk.Label(self, text="", font = ('메이플스토리', 15))
        self.label2.pack()

        label = tk.Label(self, text="세트: ", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        self.label3 = tk.Label(self, text="1/4", font = ('메이플스토리', 15))
        self.label3.pack()
            
        label = tk.Label(self, text="쓸심: ", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        self.label4 = tk.Label(self, text="", font = ('메이플스토리', 15))
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
                                command=lambda:controller.show_frame(control_room), font=LARGE_FONT)
        left_arrow.place(x=0, y=160, height=80, width=50)
        
        cancel = tk.Button(self, text="취소",
                           command=lambda:controller.show_frame(Cancel))
        cancel.pack(pady=40)

        parent.bind("r", self.restart)

        self.update()

    
    
    def restart(self, event=None):
        self.seconds_left2 = sim[0] #change to sim[0]
        time2 = self.seconds_left_to_time(self.seconds_left2)
        
        self.label4.configure(text=time2[0]+":"+time2[1])
        pygame.mixer.music.load("SymbolRestart.mp3")
        pygame.mixer.music.play(loops=0)
        """
        reroll2=ImageTk.PhotoImage(file="reroll2.png")
        button.config(image=reroll2)
        button.pack()
        self.after(1000, button.config(image=reroll))
        button.pack()
        """

    def update(self):
        self.seconds_left -= 1
        self.seconds_left2 -= 1
        
        time = self.seconds_left_to_time(self.seconds_left)
        time2 = self.seconds_left_to_time(self.seconds_left2)
        self.label2.configure(text=time[0]+":"+time[1])
        self.label4.configure(text=time2[0]+":"+time2[1])

        now = datetime.now()
        """
        if self.seconds_left == data["time"]+3+60:
            if now.hour-data["timediff"] in (11, 6, 8):
                pygame.mixer.music.load("1LapBreak.mp3")
                pygame.mixer.music.play(loops=0)

        if self.seconds_left == 3+60:
            if now.hour-data["timediff"] in (11, 6, 8):
                pygame.mixer.music.load("1LapStart.mp3")
                pygame.mixer.music.play(loops=0)
        """
            
        if self.seconds_left2 == 3:
            pygame.mixer.music.load("Symbol.mp3")
            pygame.mixer.music.play(loops=0)
        if self.seconds_left2 == 0:
            self.seconds_left2 = sim[0] #change to sim[0]
        if self.seconds_left == data["time"]+3:
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
                self.label2.configure(text="30:00")
                self.seconds_left = 30*60 #change to 30*60
            
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

def main():
    #splash.destroy()
    app = TimerApp()
    app.title('재획 타이머')
    app.iconbitmap("icon.ico")
    app.geometry('300x450+475+150')
    #app.protocol("WM_DELETE_WINDOW", print("hi"))
    app.mainloop()
    #size and position was  300x580+475+150

"""
splash = tk.Tk()
splash.title("Splash screen")
splash.geometry("360x180+450+300")
splash.overrideredirect(True)
img = ImageTk.PhotoImage(Image.open("Splash.png"))
label = tk.Label(image=img)
label.pack()
splash.after(1500, main)
"""
main()











