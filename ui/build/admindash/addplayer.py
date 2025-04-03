
from pathlib import Path
from tkinter import ttk 
from dbconnectionadmin import add_user,send_verification_email,verify_email_code,emailalreadyexist,usernamealreadyexist,fetch_teams,add_player,is_team_full
import re
import tkinter as tk
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,font,StringVar, OptionMenu,messagebox,Toplevel, Label



OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Soham\Desktop\RAMDOM PROJECTS\cricket_league_management\ui\build\admindash\assets1\assets_signup\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("516x350")
window.configure(bg = "#FFFFFF")
custom_font = font.Font(family="Iceland", size=20)
custom_font20 = font.Font(family="Iceland", size=25)
role_var = StringVar()
role_var.set("Select Role")
window.lift()          # Bring the window to the front
window.focus_force()
window.grab_set() 
    


def add(username):
    add_window = tk.Toplevel()
    add_window.title("Player Details")
    add_window.geometry("300x250")
    add_window.lift()          # Bring the window to the front
    add_window.focus_force()
    add_window.grab_set() 

    tk.Label(add_window, text="Player Name:").pack(pady=5)
    entry_name = tk.Entry(add_window)
    entry_name.pack(pady=5)

    tk.Label(add_window, text="Role:").pack(pady=5)
    role_var = tk.StringVar()
    role_dropdown = ttk.Combobox(add_window, textvariable=role_var, values=["Batsman", "Bowler", "WicketKeeper"], state="readonly")
    role_dropdown.pack(pady=5)
    role_dropdown.current(0)  # Set default selection

    tk.Label(add_window, text="Team:").pack(pady=5)
    teams = fetch_teams()  # Fetch team list from database
    team_dict = {team[1]: team[0] for team in teams}  # Map team name to team ID
    team_var = tk.StringVar()
    team_dropdown = ttk.Combobox(add_window, textvariable=team_var, values=list(team_dict.keys()), state="readonly")
    team_dropdown.pack(pady=5)

    def submit():
        player_name = entry_name.get().strip()
        role = role_var.get().strip()
        team_name = team_var.get().strip()
        team_id = team_dict.get(team_name, None)

        # **Validation Checks**
        if not player_name:
            messagebox.showwarning("Input Error", "Player name is required.")
            return  
        if not team_id:
            messagebox.showwarning("Input Error", "Please select a team.")
            return  
        if is_team_full(team_id):  
            messagebox.showwarning("Team Error", "Team already has 11 players.")
            return 

        # **Only close the window if the player is successfully added**
        if add_player(player_name, role, team_id, username):  
            messagebox.showinfo("Success", "Player added successfully!")
            add_window.destroy()  # ✅ Now we can close it
        else:
            messagebox.showerror("Error", "Failed to add player.")  
            return  

    tk.Button(add_window, text="Add Player", command=submit).pack(pady=10)
   


def register():
    username = entry_2.get()
    password = entry_1.get()
    email = entry_3.get()
    role = "player"
    if username == "" or password == "" or email=="":
        messagebox.showerror("Error", "All fields are required")
        return
    if add_user(username, password,email,role)=="username_error":
        messagebox.showinfo("Error","Username already taken")
        return

    if add_user(username, password,email,role):
        messagebox.showinfo("Success", "user Added add player details")
        add(username)
        window.destroy()
        
    
    else:
        messagebox.showerror("Error", "Invalid Username or Password")


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)


def open_otp_window():
    username = entry_2.get()
    global otp_window, entry_3
    email = entry_3.get()  # Get email from signup form
    if usernamealreadyexist(username):
        messagebox.showerror("Error", "Username already taken")
        return
    if emailalreadyexist(email):
        messagebox.showerror("Error", "Email already taken")
        return

    
    
    if not is_valid_email(email):
        messagebox.showerror("Invalid Email", "Please enter a valid email address.")
        return


    if send_verification_email(email):
        messagebox.showinfo("OTP Sent", "A verification code has been sent to your email.")
    elif send_verification_email(email)=='error':
         messagebox.showerror("Error", "Please enter correct Email Address")

    else:
        messagebox.showerror("Error", "Failed to send OTP. Try again.")
        return

    # Create a new OTP window
    otp_window = Toplevel(window)
    otp_window.title("Email Verification")
    otp_window.geometry("350x200")

    Label(otp_window, text="Enter OTP:", font=("Inter", 16)).pack(pady=10)
    
    entry_otp = Entry(otp_window, font=("Inter", 16))
    entry_otp.pack(pady=5)

    def verify_otp():
        otp = entry_otp.get()
        if verify_email_code(email, otp):
            register()  # Register user after verification
            otp_window.destroy()
        else:
            messagebox.showerror("Verification Failed", "Invalid OTP. Please try again.")

    Button(otp_window, text="Verify OTP", command=verify_otp, font=("Inter", 14)).pack(pady=10)


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 497,
    width = 516,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    258.0,
    360.0,
    image=image_image_1
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    338.0,
    130.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    font=custom_font,
    highlightthickness=0
)
entry_1.place(
    x=215.5,
    y=102.0,
    width=245.0,
    height=55.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    338.0,
    51.5,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    font=custom_font,
    highlightthickness=0
)
entry_2.place(
    x=217.5,
    y=23.0,
    width=241.0,
    height=55.0
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    336.0,
    209.5,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    font=custom_font,
    highlightthickness=0
)
entry_3.place(
    x=213.5,
    y=181.0,
    width=245.0,
    height=55.0
)

canvas.create_text(
    27.0,
    32.0,
    anchor="nw",
    text="USERNAME",
    fill="#000000",
    font=custom_font20
)

canvas.create_text(
    27.0,
    113.0,
    anchor="nw",
    text="PASSWORD",
    fill="#000000",
    font=custom_font20
)

canvas.create_text(
    27.0,
    192.0,
    anchor="nw",
    text="EMAIL",
    fill="#000000",
    font=custom_font20
)


button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=open_otp_window,
    relief="flat"
)
button_1.place(
    x=90.0,
    y=271.0,
    width=347.0,
    height=65.0
)

window.resizable(False, False)
window.mainloop()
