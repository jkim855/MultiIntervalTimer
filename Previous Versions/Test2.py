import tkinter as tk
from PIL import ImageTk, Image

root = tk.Tk()

bg = ImageTk.PhotoImage(file="arcana.png")

c = tk.Canvas(root, width=300, height=465)
c.pack(expand="yes", fill="both")
c.create_image(0, 0, image=bg, anchor="nw")
c.create_text(150, 30, fill="white", font = "메이플스토리 25 bold", text="재획 타이머")

root.mainloop()
