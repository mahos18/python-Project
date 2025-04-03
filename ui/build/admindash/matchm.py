

from pathlib import Path
from dbconnectionadmin import get_standings,get_matches,fetch_teams,add_match,remove_match,reschedule_all_matches,get_player_count,get_team_ids
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,messagebox
from tkinter import ttk
import tkinter as tk
import subprocess


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Soham\Desktop\RAMDOM PROJECTS\cricket_league_management\ui\build\admindash\assets1\assets_match\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1440x720")
window.configure(bg = "#FFFFFF")

def open_scorecard(match_id):
    subprocess.run(["python", "scorecard/scorecard.py", str(match_id)])

def display_standings():
    standings = get_standings()
    if not standings:
        print("No standings data available")
        return

    style = ttk.Style()
    style.configure("Treeview", font=("Iceland", 18))  # Change font for rows
    style.configure("Treeview.Heading", font=("Iceland", 15, "bold")) 
    style.configure("Treeview", rowheight=40) # Change font for headings

    # Create Treeview widget
    columns = ("Team Name", "Matches Played", "Wins", "Lose", "Points")
    column_ratios = [0.35, 0.30, 0.10, 0.10, 0.15]  # Adjust ratios (sum should be 1.0)
    total_width = 500  # Set total width of the table

    tree1 = ttk.Treeview(window, columns=columns, show="headings")

    # Define column headings & set width dynamically
    for col, ratio in zip(columns, column_ratios):
        tree1.heading(col, text=col)
        tree1.column(col, anchor="center", width=int(total_width * ratio))
    tree1.place(x=90, y=370, width=580, height=295)  # Adjust placement & size

    # Insert data into the table
    for team in standings:
        tree1.insert("", "end", values=(
            team["team_name"],
            team["matches_played"],
            team["wins"],
            team["losses"],
            team["points"]
        ))

def matches(tree):
    standings = get_matches()
    if not standings:
        print("No matches data available")
        return
    for item in tree.get_children():
        tree.delete(item)
    # Define column headings & set width dynamically
    for col, ratio in zip(columns, column_ratios):
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=int(total_width * ratio))
    tree.place(x=739, y=100, width=599, height=510)  # Adjust placement & size

    # Insert data into the table
    for team in standings:
        tree.insert("", "end", values=(
            team["ID"],
            team["team1"],
            team["team2"],
            team["status"],
            team["winner"]
        
        ))


def open_schedule_match_window():
    schedule_window = tk.Toplevel()
    schedule_window.title("Schedule Match")
    schedule_window.geometry("300x250")

    tk.Label(schedule_window, text="Select Team 1:").pack(pady=5)
    teams = fetch_teams()  # Fetch team list from database
    team_dict = {team[1]: team[0] for team in teams}  # Map team name to team ID

    team1_var = tk.StringVar()
    team1_dropdown = ttk.Combobox(schedule_window, textvariable=team1_var, values=list(team_dict.keys()), state="readonly")
    team1_dropdown.pack(pady=5)

    tk.Label(schedule_window, text="Select Team 2:").pack(pady=5)
    team2_var = tk.StringVar()
    team2_dropdown = ttk.Combobox(schedule_window, textvariable=team2_var, values=list(team_dict.keys()), state="readonly")
    team2_dropdown.pack(pady=5)

    def schedule_match():
        team1_name = team1_var.get().strip()
        team2_name = team2_var.get().strip()
        
        if not team1_name or not team2_name:
            messagebox.showwarning("Input Error", "Please select both teams.")
            return
        
        if team1_name == team2_name:
            messagebox.showwarning("Input Error", "A team cannot play against itself.")
            return

        team1_id = team_dict.get(team1_name)
        team2_id = team_dict.get(team2_name)

        if add_match(team1_id, team2_id):
            messagebox.showinfo("Success", "Match scheduled successfully!")
            schedule_window.destroy()
            matches(tree)
        else:
            messagebox.showerror("Error", "Failed to schedule match.")

    tk.Button(schedule_window, text="Schedule Match", command=schedule_match).pack(pady=10)
    schedule_window.mainloop()

def check_teams_and_proceed():
    """Check if both teams have exactly 11 players before proceeding"""
    selected_item = tree.focus()  # Get selected match
    if not selected_item:
        messagebox.showerror("Error", "Please select a match to start.")
        return

    match_details = tree.item(selected_item, "values")  # Get match details
    match_id = match_details[0]  # Assuming Match ID is in the first column

    # Fetch Team IDs
    team1_id, team2_id = get_team_ids(match_id)
    
    if not team1_id or not team2_id:
        messagebox.showerror("Error", "Invalid match data. Teams not found.")
        return

    # Get player counts
    team1_count = get_player_count(team1_id)
    team2_count = get_player_count(team2_id)

    # Check if both teams have 11 players
    if team1_count != 11 or team2_count != 11:
        messagebox.showerror("Error", f"Team 1 has {team1_count} players, Team 2 has {team2_count} players. Both must have 11 players.")
        return

    messagebox.showinfo("Success", "Both teams have 11 players. Proceeding to the next step!")
    open_scorecard(match_id)




def start_match():
    selected_item = tree.focus()  # Get the selected match from the treeview
    if not selected_item:
        messagebox.showerror("Error", "Please select a match to start.")
        return

    match_details = tree.item(selected_item, "values")  # Get match details

    # Show confirmation popup
    confirm = messagebox.askyesno("Confirm", f"Do you want to start the match: {match_details[0]}?")
    
    if confirm:
        # Proceed with starting the match
        print(f"Starting match: {match_details[0]}")  


def remove_selected_match(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a match to remove.")
        return
    confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to remove the scheduled match?")
    if not confirm:
        return  # Get selected team
    match_id = tree.item(selected_item, "values")[0]  # Get match ID from selected row
    if remove_match(match_id):  # Call the database function
        messagebox.showinfo("Success", "Match removed successfully!")
        tree.delete(selected_item)  # Remove from UI as well
    else:
        messagebox.showerror("Error", "Failed to remove match.")

def open_reschedule_window():
    reschedule_window = tk.Toplevel()
    reschedule_window.title("Reschedule Matches")
    reschedule_window.geometry("300x150")
    
    tk.Label(reschedule_window, text="Reschedule all matches?").pack(pady=10)
    
    def reschedule_all():
        if reschedule_all_matches():  # Call the database function
            messagebox.showinfo("Success", "All matches have been rescheduled!")
            matches(tree)
            reschedule_window.destroy()
        else:
            messagebox.showerror("Error", "Failed to reschedule matches.")
    
    tk.Button(reschedule_window, text="Reschedule All", command=reschedule_all).pack(pady=5)
    tk.Button(reschedule_window, text="Cancel", command=reschedule_window.destroy).pack(pady=5)
    
    reschedule_window.mainloop()




canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 720,
    width = 1368,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

style = ttk.Style()
style.configure("Treeview", font=("Iceland", 20))  # Change font for rows
style.configure("Treeview.Heading", font=("Iceland", 17, "bold")) 
style.configure("Treeview", rowheight=40) # Change font for headings

# Create Treeview widget
columns = ("ID","Team 1", "Team 2", "Status", "Winner")
column_ratios = [0.2,0.2,0.2,0.2,0.2]  # Adjust ratios (sum should be 1.0)
total_width = 599  # Set total width of the table

tree = ttk.Treeview(window, columns=columns, show="headings")

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    875.72265625,
    643.0985092381961,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    918.0,
    606.0000015039914,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    862.0,
    1176.9999984960086,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    1037.0,
    344.0,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    378.0,
    500.0,
    image=image_image_5
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=open_schedule_match_window,
    relief="flat"
)
button_1.place(
    x=17.0,
    y=65.0,
    width=308.0,
    height=73.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: remove_selected_match(tree),
    relief="flat"
)
button_2.place(
    x=224.0,
    y=180.0,
    width=308.0,
    height=73.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=check_teams_and_proceed,
    relief="flat"
)
button_3.place(
    x=410.0,
    y=65.0,
    width=308.0,
    height=73.0
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    872.0,
    59.0,
    image=image_image_6
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    193.0,
    340.0,
    image=image_image_7
)
reschedule_btn = tk.Button(
    window, 
    text="Reschedule All Matches", 
    command=open_reschedule_window, 
    font=("Iceland", 15, "bold"), 
    bg="#4CAF50", 
    fg="white", 
    width=20, 
    height=2
)
reschedule_btn.place(x=1109, y=610)  


matches(tree)
display_standings()
window.resizable(False, False)
window.mainloop()
