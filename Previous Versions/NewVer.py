import tkinter as tk
from datetime import datetime, date, time, timedelta
import pygame
from PIL import ImageTk, Image

LARGE_FONT = ("메이플스토리", 18)
MEDIUM_FONT = ("메이플스토리", 15)
SMALL_FONT = ("메이플스토리", 10)
BUTTON_FONT = ("메이플스토리", 13)
BUTTON_FONT2 = ("메이플스토리", 12)

data = {}
sim = [200]
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

        for F in (StartPage, Default29, Default30, Book29, Cancel):
            
            self.create_frame(F)

        self.show_frame(StartPage)
        
    def show_frame(self, controller):
        frame = self.frames[controller]
        frame.tkraise()

    def create_frame(self, F):
        frame = F(container, self)
        self.frames[F] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        
def record(cont):
    try:
        data["time"] = int(textbox.get())
    except:
        data["time"] = 40
    cont.show_frame(Default30)
    
def Buff(cont):
    data["buff"] = True
    cont.show_frame(Default29)

def NoBuff(cont):
    data["buff"] = False
    cont.show_frame(Default30)

def Book30(controller):
    data["sched"] = 30
    controller.create_frame(Prep)

def Book45(controller):
    data["sched"] = 45
    controller.create_frame(Prep)

def CreateStart(controller):
    controller.create_frame(Start)

def define_sim(textBox):
    
    sim[0] = int(textBox.get())
    currentSim.configure(text=str(sim[0])+"초")

def delete(controller, page):
    controller.frames[page].grid_forget()
    controller.frames[page].destroy()
    controller.show_frame(StartPage)
    pygame.mixer.music.stop()
    data = {}

class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        img = Image.open("arcana.png")
        bg = ImageTk.PhotoImage(img)

        bg_label = tk.Label(self, image=bg)
        bg_label.place(x=0,y=0)

        
        label = tk.Label(self, text="재획 타이머", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button29 = tk.Button(self, text="경뿌 O",
                             command=lambda:Buff(controller),
                             height=2, width=10, font=BUTTON_FONT)
        button29.pack(pady=10)
        button30 = tk.Button(self, text = "경뿌 X",
                             command = lambda:NoBuff(controller),
                             height=2, width=10, font=BUTTON_FONT)
        button30.pack()

        simLabel = tk.Label(self, text="쓸심 지속시간 (초)", font=MEDIUM_FONT)
        simLabel.pack(pady=20)

        textBox = tk.Entry(self, width = 20)
        textBox.pack()

        simButton = tk.Button(self, text="확인",
                              command=lambda:define_sim(textBox))
        simButton.pack()
        global currentSim
        currentSim = tk.Label(self, text=str(sim[0])+"초", font=SMALL_FONT)
        currentSim.pack(pady=20)

        info = tk.Label(self, text="(0 입력시 비활성화)", font=SMALL_FONT)
        info.pack(pady=30)

class Default30(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        book29 = tk.Button(self, text="예약",
                           command=lambda:controller.show_frame(Book29),
                           height=2, width=10, font=BUTTON_FONT)
        book29.pack(pady=10)

        instant29 = tk.Button(self, text="바로시작",
                           command=lambda:CreateStart(controller),
                              height=2, width=10, font=BUTTON_FONT)
        instant29.pack(pady=10)

        late29 = tk.Button(self, text="지각",
                           command=lambda:controller.show_frame(Start),
                           height=2, width=10, font=BUTTON_FONT)
        late29.pack(pady=10)
        
        button29 = tk.Button(self, text="뒤로가기",
                             command=lambda:controller.show_frame(StartPage),
                             height=2, width=8, font=BUTTON_FONT2)
        button29.pack(pady=20)

class Default29(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="여유 시간 (초)", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        global textbox
        textbox = tk.Entry(self, width = 30)
        textbox.pack()

        buttonTime = tk.Button(self, text="확인",
                               command=lambda:record(controller))
        buttonTime.pack()

        button30 = tk.Button(self, text="뒤로가기",
                             command=lambda:controller.show_frame(StartPage))
        button30.pack(pady=30)
    

class Book29(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="예약", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        next0030 = tk.Button(self, text="다음 00/30",
                           command=lambda:Book30(controller), font=BUTTON_FONT)
        next0030.pack(pady=10)

        next1545 = tk.Button(self, text="다음 15/45",
                             command=lambda:Book45(controller), font=BUTTON_FONT)
        next1545.pack()
        
        backButton = tk.Button(self, text="뒤로가기",
                             command=lambda:controller.show_frame(StartPage))
        backButton.pack(pady=20)

class Prep(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = tk.Label(self, text="남은 시간: ", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        self.label2 = tk.Label(self, text="", font = ('메이플스토리', 15))
        self.label2.pack()

        cancel = tk.Button(self, text="취소",
                           command=lambda:delete(controller, Prep))
        cancel.pack(pady=40)
        
        if data["sched"] == 30:
            self.update30()
        elif data["sched"] == 45:
            self.update45()
        
    def update30(self):
        now = datetime.now()

        current = now.minute * 60 + now.second
        if current == 0:
            CreateStart(self.controller)
            return 0
        
        if now.minute > 30:
            left = 30*60+1800 - current 
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

    def update45(self):
        now = datetime.now()

        current = now.minute * 60 + now.second
        
        if now.minute > 45:
            left = 60*60 - current + 15*60
        elif now.minute < 15:
            left = 15*60 - current
        else:
            left = 45*60 - current
        
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
        
        self.after(100, self.update45)


class Cancel(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="정말 취소하시겠습니까?", font=LARGE_FONT)
        label.pack()
        cancel = tk.Button(self, text="예",
                           command=lambda:delete(controller, Start),
                           height=3, width=6, font=BUTTON_FONT)
        cancel.pack(padx=30, pady=1, side=tk.LEFT)
        cancel = tk.Button(self, text="아니오",
                           command=lambda:controller.show_frame(Start),
                           height=3, width=6, font=BUTTON_FONT)
        cancel.pack(padx=30, pady=1, side=tk.RIGHT)
    

class Start(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pygame.mixer.music.load("1LapStartShort.mp3")
        pygame.mixer.music.play(loops=0)
        self.seconds_left = 30*60 #change to 30*60
        self.seconds_left2 = sim[0] #change to sim[0]
        self.set_count = 1    
        
        label = tk.Label(self, text="다음 경쿠: ", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        self.label2 = tk.Label(self, text="", font = ('메이플스토리', 15))
        self.label2.pack()

        label = tk.Label(self, text="세트: ", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        self.label3 = tk.Label(self, text="1/4", font = ('메이플스토리', 15))
        self.label3.pack()

        if sim[0] == 0:
            if "time" in data:
                self.update4()
            else:
                self.update2()
            
        else:
            label = tk.Label(self, text="쓸심: ", font=LARGE_FONT)
            label.pack(pady=10, padx=10)
            self.label4 = tk.Label(self, text="", font = ('메이플스토리', 15))
            self.label4.pack()

            global reroll
            reroll = ImageTk.PhotoImage(file="reroll.png")
            restart = tk.Button(self, image=reroll,
                                   command=lambda:self.restart(restart), borderwidth=0)
            restart.image = reroll
            restart.pack()
            
            if "time" in data:
                self.update3()
            else:
                self.update()
            
        cancel = tk.Button(self, text="취소",
                           command=lambda:controller.show_frame(Cancel))
        cancel.pack(pady=40)      
        
    def restart(self, button):
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
        if self.seconds_left2 == 3:
            pygame.mixer.music.load("Symbol.mp3")
            pygame.mixer.music.play(loops=0)
        if self.seconds_left2 == 0:
            self.seconds_left2 = sim[0] #change to sim[0]
        if self.seconds_left == 3:
            pygame.mixer.music.load("1LapStart.mp3")
            pygame.mixer.music.play(loops=0)
        if self.seconds_left == 0:
            if self.set_count == 4:
                self.set_count = 0
                pygame.mixer.music.load("4Laps.mp3")
                pygame.mixer.music.play(loops=0)
            self.label2.configure(text="30:00")
            self.set_count += 1
            self.label3.configure(text=str(self.set_count)+"/4")
            self.seconds_left = 30*60 #change to 30*60
        
        self.after(999, self.update)

    def update2(self):
        self.seconds_left -= 1
        time = self.seconds_left_to_time(self.seconds_left)
        self.label2.configure(text=time[0]+":"+time[1])
        if self.seconds_left == 3:
            pygame.mixer.music.load("1LapStart.mp3")
            pygame.mixer.music.play(loops=0)
        if self.seconds_left == 0:
            if self.set_count == 4:
                self.set_count = 0
                pygame.mixer.music.load("4Laps.mp3")
                pygame.mixer.music.play(loops=0)
            self.label2.configure(text="30:00")
            self.set_count += 1
            self.label3.configure(text=str(self.set_count)+"/4")
            self.seconds_left = 30*60 #change to 30*60
        
        self.after(999, self.update2)

    def update3(self):
        self.seconds_left -= 1
        self.seconds_left2 -= 1
        time = self.seconds_left_to_time(self.seconds_left)
        time2 = self.seconds_left_to_time(self.seconds_left2)
        self.label2.configure(text=time[0]+":"+time[1])
        self.label4.configure(text=time2[0]+":"+time2[1])
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
            self.label2.configure(text="30:00")
            self.set_count += 1
            self.label3.configure(text=str(self.set_count)+"/4")
            self.seconds_left = 30*60 #change to 30*60
        
        self.after(999, self.update3)
        
    def update4(self):
        self.seconds_left -= 1
        time = self.seconds_left_to_time(self.seconds_left)
        self.label2.configure(text=time[0]+":"+time[1])
        if self.seconds_left == 3+data["time"]:
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
            self.label2.configure(text="30:00")
            self.set_count += 1
            self.label3.configure(text=str(self.set_count)+"/4")
            self.seconds_left = 30*60 #change to 30*60
        
        self.after(999, self.update4)
    
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











