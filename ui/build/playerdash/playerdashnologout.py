from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Label,messagebox
from dbconnectionplayer import get_player_details,get_standings,get_upcoming_matches,get_team_id
import sys
import os
from tkinter import ttk

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Soham\Desktop\RAMDOM PROJECTS\cricket_league_management\ui\build\playerdash\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def logout():
    # Show confirmation dialog
    confirm = messagebox.askyesno("Logout", "Are you sure you want to log out?")
    
    if confirm:
        window.destroy()  # Destroy current window
        # Get parent directory path
        parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        main_script = os.path.join(parent_dir, "main.py")

        # Run main.py from the parent directory
        if os.path.exists(main_script):
            os.system(f'python "{main_script}"')  # Run the main script

def load_user_id():
    """Fetches the user_id from command-line arguments if provided."""
    return sys.argv[1] if len(sys.argv) > 1 else None# Replace with actual logged-in user ID

user_id = load_user_id() 


# Fetch player details from DB
player_data = get_player_details(user_id)

if player_data:
    player_name = player_data['player_name']
    team_name = player_data['team_name'] if player_data['team_name'] else "Not Assigned"
    runs = player_data['runs']
    wickets = player_data['wickets']
    matches = player_data['matches_played']
    #wins = player_data['wins']
    role = player_data['role'] if player_data['role'] else "N/A"
else:
    player_name, team_name, runs, wickets, matches, wins, role = "Unknown", "Not Assigned", 0, 0, 0, 0, "N/A"


window = Tk()
window.geometry("1368x720")
window.configure(bg="#FFFFFF")

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

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
canvas.create_image(345.0, 360.0, image=image_image_1)

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
canvas.create_image(346.0, 172.0, image=image_image_2)

# Creating rectangles for data fields
canvas.create_rectangle(89.0, 301.0, 602.0, 360.0, fill="#FFFFFF", outline="")
canvas.create_rectangle(89.0, 383.0, 233.0, 497.0, fill="#FFFFFF", outline="")
canvas.create_rectangle(89.0, 520.0, 233.0, 634.0, fill="#FFFFFF", outline="")
canvas.create_rectangle(274.0, 383.0, 418.0, 497.0, fill="#FFFFFF", outline="")
canvas.create_rectangle(274.0, 520.0, 418.0, 634.0, fill="#FFFFFF", outline="")
canvas.create_rectangle(458.0, 383.0, 602.0, 497.0, fill="#FFFFFF", outline="")
canvas.create_rectangle(458.0, 520.0, 602.0, 634.0, fill="#FFFFFF", outline="")

# Creating Labels
canvas.create_text(289.0, 531.0, anchor="nw", text="MATCHES", fill="#000000", font=("Iceland", 24 * -1))
canvas.create_text(132.0, 533.0, anchor="nw", text="WINS", fill="#000000", font=("Iceland", 24 * -1))
canvas.create_text(127.0, 392.0, anchor="nw", text="RUNS", fill="#000000", font=("Iceland", 24 * -1))
canvas.create_text(474.0, 394.0, anchor="nw", text="WICKETS", fill="#000000", font=("Iceland", 24 * -1))
canvas.create_text(490.0, 529.0, anchor="nw", text="TEAM", fill="#000000", font=("Iceland", 24 * -1))
canvas.create_text(318.0, 392.0, anchor="nw", text="ROLE", fill="#000000", font=("Iceland", 24 * -1))

# Creating Labels for Values (Below Each Title)
name_label = Label(window, text=player_name, font=("Iceland", 25), bg="#FFFFFF")
name_label.place(x=245.0, y=310.0)

runs_label = Label(window, text=runs, font=("Iceland", 20), bg="#FFFFFF")
runs_label.place(x=140, y=430)

wickets_label = Label(window, text=wickets, font=("Iceland", 20), bg="#FFFFFF")
wickets_label.place(x=510, y=430)

matches_label = Label(window, text=matches, font=("Iceland", 20), bg="#FFFFFF")
matches_label.place(x=330, y=570)

wins_label = Label(window, text="0", font=("Iceland", 20), bg="#FFFFFF")
wins_label.place(x=150, y=570)

team_label = Label(window, text=team_name, font=("Iceland", 14), bg="#FFFFFF")
team_label.place(x=460, y=570)

role_label = Label(window, text=role, font=("Iceland", 20), bg="#FFFFFF")
role_label.place(x=300, y=430)

image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
canvas.create_image(1025.0, 185.0, image=image_image_3)

image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
canvas.create_image(1025.0, 532.0, image=image_image_4)

canvas.create_text(742.0, 48.0, anchor="nw", text="UPCOMING MATCHES", fill="#000000", font=("Iceland", 41 * -1))
canvas.create_text(742.0, 376.0, anchor="nw", text="TEAM STANDINGS", fill="#000000", font=("Iceland", 41 * -1))


def display_standings():
    standings = get_standings()
    if not standings:
        print("No standings data available")
        return

    style = ttk.Style()
    style.configure("Treeview", font=("Iceland", 18))  # Change font for rows
    style.configure("Treeview.Heading", font=("Iceland", 14, "bold")) 
    style.configure("Treeview", rowheight=38) # Change font for headings

    # Create Treeview widget
    columns = ("Team Name", "Matches Played", "Wins", "Lose", "Points")
    column_ratios = [0.35, 0.15, 0.15, 0.15, 0.20]  # Adjust ratios (sum should be 1.0)
    total_width = 500  # Set total width of the table

    tree = ttk.Treeview(window, columns=columns, show="headings")

    # Define column headings & set width dynamically
    for col, ratio in zip(columns, column_ratios):
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=int(total_width * ratio))
    tree.place(x=750, y=420, width=560, height=250)  # Adjust placement & size

    # Insert data into the table
    for team in standings:
        tree.insert("", "end", values=(
            team["team_name"],
            team["matches_played"],
            team["wins"],
            team["losses"],
            team["points"]
        ))


def display_matches(team_id):
    matches = get_upcoming_matches(team_id)
    if not matches:
        print("No  matches data available")
        return

    style = ttk.Style()
    style.configure("Treeview", font=("Iceland", 17))  # Change font for rows
    style.configure("Treeview.Heading", font=("Iceland", 14, "bold")) 
    style.configure("Treeview", rowheight=38) # Change font for headings

    # Create Treeview widget
    columns = ("Team 1", "Team 2", "Date", "Status")
    column_ratios = [0.30,0.30,0.20,0.20]  # Adjust ratios (sum should be 1.0)
    total_width = 500  # Set total width of the table

    tree = ttk.Treeview(window, columns=columns, show="headings")

    # Define column headings & set width dynamically
    for col, ratio in zip(columns, column_ratios):
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=int(total_width * ratio))
    tree.place(x=740, y=100, width=560, height=240)  # Adjust placement & size

    # Insert data into the table
    for team in matches:
        tree.insert("", "end", values=(
            team[1],
            team[2],
            team[0]
            
        ))


team_id=get_team_id(user_id)
if team_id:
    id=team_id[0]
    print(f"Debug: team_id type -> {type(team_id)}, value -> {team_id}")
    display_matches(id)

display_standings()

window.resizable(False, False)
window.mainloop()
