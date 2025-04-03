from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox
import sys
from tkinter import ttk
import tkinter as tk

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Soham\Desktop\RAMDOM PROJECTS\cricket_league_management\ui\build\scorecard\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)



def load_match_id():
    """Fetches the user_id from command-line arguments if provided."""
    return sys.argv[1] if len(sys.argv) > 1 else None# Replace with actual logged-in user ID

match_id = load_match_id() 
print(match_id)
def select_batting_team(match_id):
    
    # Create popup window
    popup = tk.Toplevel()
    popup.title("Select Batting Team and Players")
    popup.geometry("400x300")
    
    # Batting team selection
    tk.Label(popup, text="Select Batting Team:").pack()
    team_var = tk.StringVar()
    team_dropdown = ttk.Combobox(popup, textvariable=team_var, values=["Team 1", "Team 2"])
    team_dropdown.pack()
    
    # Batsman selection
    tk.Label(popup, text="Select Batsman 1:").pack()
    batsman1_var = tk.StringVar()
    batsman1_dropdown = ttk.Combobox(popup, textvariable=batsman1_var)
    batsman1_dropdown.pack()
    
    tk.Label(popup, text="Select Batsman 2:").pack()
    batsman2_var = tk.StringVar()
    batsman2_dropdown = ttk.Combobox(popup, textvariable=batsman2_var)
    batsman2_dropdown.pack()
    
    # Bowler selection
    tk.Label(popup, text="Select Bowler:").pack()
    bowler_var = tk.StringVar()
    bowler_dropdown = ttk.Combobox(popup, textvariable=bowler_var)
    bowler_dropdown.pack()
    
    def update_player_lists(*args):
        selected_team = team_var.get()
        if selected_team == "Team 1":
            batsmen_list = team1_players
            bowlers_list = team2_players
        else:
            batsmen_list = team2_players
            bowlers_list = team1_players
        
        batsman1_dropdown["values"] = [f"{p[1]} ({p[0]})" for p in batsmen_list]
        batsman2_dropdown["values"] = [f"{p[1]} ({p[0]})" for p in batsmen_list]
        bowler_dropdown["values"] = [f"{p[1]} ({p[0]})" for p in bowlers_list]
    
    team_dropdown.bind("<<ComboboxSelected>>", update_player_lists)
    
    def confirm_selection():
        if not (team_var.get() and batsman1_var.get() and batsman2_var.get() and bowler_var.get()):
            messagebox.showerror("Error", "All selections must be made!")
            return
        
        messagebox.showinfo("Success", f"Match Setup:\nBatting Team: {team_var.get()}\nBatsmen: {batsman1_var.get()}, {batsman2_var.get()}\nBowler: {bowler_var.get()}")
        popup.destroy()
    
    confirm_btn = tk.Button(popup, text="Confirm", command=confirm_selection)
    confirm_btn.pack()
    
    popup.mainloop()


# Initialize Window
def scorecard():
    window = Tk()
    window.geometry("1368x720")
    window.configure(bg="#FFFFFF")

    # Create Canvas
    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=720,
        width=1368,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Load Images
    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    canvas.create_image(1114.0, 247.0, image=image_image_1)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    canvas.create_image(681.0, 59.0, image=image_image_2)

    image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
    canvas.create_image(427.0, 247.0, image=image_image_3)

    image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
    canvas.create_image(428.0, 447.0, image=image_image_4)

    image_image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
    canvas.create_image(430.0, 609.0, image=image_image_5)

    image_image_6 = PhotoImage(file=relative_to_assets("image_6.png"))
    canvas.create_image(1115.0, 543.0, image=image_image_6)

    # Add Text Elements
    canvas.create_text(184.0, 29.0, anchor="nw", text="Team name 1", fill="#000000", font=("Iceland", 53))
    canvas.create_text(900.0, 24.0, anchor="nw", text="Team name 2", fill="#000000", font=("Iceland", 53))
    canvas.create_text(644.0, 38.0, anchor="nw", text="V/S", fill="#000000", font=("Iceland", 53))

    # Button Actions
    def button_clicked(button_num):
        print(f"Button {button_num} clicked")

    # Create Buttons
    buttons = []
    button_positions = [
        (195, 399), (73, 399), (702, 557), (204, 557), (54, 557),
        (343, 557), (509, 557), (317, 398), (439, 399), (561, 399), (683, 398)
    ]

    for i, pos in enumerate(button_positions, start=1):
        button_img = PhotoImage(file=relative_to_assets(f"button_{i}.png"))
        button = Button(
            image=button_img,
            borderwidth=0,
            highlightthickness=0,
            command=lambda i=i: button_clicked(i),
            relief="flat"
        )
        button.image = button_img  # Keep reference
        button.place(x=pos[0], y=pos[1], width=97, height=97)
        buttons.append(button)
    # Additional UI Elements
    image_image_7 = PhotoImage(file=relative_to_assets("image_7.png"))
    canvas.create_image(427.0, 181.0, image=image_image_7)

    image_image_8 = PhotoImage(file=relative_to_assets("image_8.png"))
    canvas.create_image(427.0, 299.0, image=image_image_8)

    P1=canvas.create_text(47.0, 151.0, anchor="nw", text="player 1", fill="#000000", font=("Iceland", 51))
    P2=canvas.create_text(47.0, 269.0, anchor="nw", text="player 2", fill="#000000", font=("Iceland", 51))
    P1_runs=canvas.create_text(570.0, 151.0, anchor="nw", text="00", fill="#000000", font=("Iceland", 51))
    P2_runs=canvas.create_text(570.0, 269.0, anchor="nw", text="11", fill="#000000", font=("Iceland", 51))
    P1_bowls=canvas.create_text(686.0, 161.0, anchor="nw", text="00", fill="#000000", font=("Iceland", 35))
    P2_bowls=canvas.create_text(686.0, 279.0, anchor="nw", text="11", fill="#000000", font=("Iceland", 35))
    s1=canvas.create_text(754.0, 151.0, anchor="nw", text="*", fill="#000000", font=("Iceland", 56))
    s2=canvas.create_text(753.0, 278.0, anchor="nw", text="\n", fill="#000000", font=("Iceland", 56))
    batting_team=canvas.create_text(893.0, 135.0, anchor="nw", text="TEAM NAME", fill="#FFFFFF", font=("Iceland", 50))
    runs=canvas.create_text(942.0, 212.0, anchor="nw", text="000", fill="#FFFFFF", font=("Iceland", 60))
    slash=canvas.create_text(1109.0, 210.0, anchor="nw", text="/", fill="#FFFFFF", font=("Iceland", 60))
    wickets=canvas.create_text(1154.0, 212.0, anchor="nw", text="00", fill="#FFFFFF", font=("Iceland", 60))
    bowler_name=canvas.create_text(893.0, 408.0, anchor="nw", text="bowler name", fill="#F81115", font=("Iceland", 50))
    over_bowls=canvas.create_text(893.0, 488.0, anchor="nw", text="1,2,3,4,6", fill="#6E2323", font=("Iceland", 60))

    window.resizable(False, False)
    window.mainloop()
scorecard()