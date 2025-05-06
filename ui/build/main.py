


from pathlib import Path
from redirect import open_adminlogin,open_signin,open_signup

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,font


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Soham\Desktop\RAMDOM PROJECTS\cricket_league_management\ui\build\assets\assets_main\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1368x720")
window.title="Home page"
window.configure(bg = "#FFFFFF")
custom_font = font.Font(family="Iceland", size=30)
custom_font20 = font.Font(family="Iceland", size=60)


def signin():
    window.destroy()
    open_signin()

def adminsignin():
    window.destroy()
    open_adminlogin()

def signup():

    open_signup()
   
    

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 720,
    width = 1368,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    684.0,
    360.0,
    image=image_image_1
)

canvas.create_text(
    64.0,
    64.0,
    anchor="nw",
    text="CRICKET LEAGUE MANAGEMENT SYSTEM",
    fill="#000000",
    font=custom_font20
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    343.0,
    457.0,
    image=image_image_2
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=signin,
    relief="flat"
)
button_1.place(
    x=860.0,
    y=262.0,
    width=407.0,
    height=82.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=signup,
    relief="flat"
)
button_2.place(
    x=862.0,
    y=396.0,
    width=407.0,
    height=82.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=adminsignin,
    relief="flat"
)
button_3.place(
    x=860.0,
    y=530.0,
    width=407.0,
    height=82.0
)
window.resizable(False, False)
window.mainloop()
