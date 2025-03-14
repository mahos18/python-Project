from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, Listbox, Scrollbar, messagebox,simpledialog
from dbconnectionadmin import get_teams, add_team, remove_team, get_players, update_player_team,get_team_players

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Soham\Desktop\RAMDOM PROJECTS\cricket_league_management\ui\build\admindash\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Function to update the listbox with new data
def update_listbox(data):
    listbox.delete(0, "end")  # Clear existing items
    for item in data:
        listbox.insert("end", item)

# Function to load all teams into the listbox
def load_teams():
    teams = get_teams()  # Fetch teams from DB
    update_listbox(teams)
    listbox.selection_clear(0, "end")

# Function to add a new team
def add_new_team():
    teams = get_teams()
    if len(teams) >= 6:
        messagebox.showerror("Limit Reached", "Maximum 6 teams allowed!")
        return
    team_name = simpledialog.askstring("New Team", "Enter new team name:")
    if team_name:
        add_team(team_name)  # Add team to DB
        load_teams()  # Refresh listbox
        messagebox.showinfo("Success", f"Team '{team_name}' added successfully!")

# Function to remove a selected team
def remove_selected_team():
    selected_team = listbox.get("active")
    confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the team '{selected_team}'?")
    if not confirm:
        return  # Get selected team
    if selected_team:
        remove_team(selected_team)  # Remove from DB
        load_teams()  # Refresh listbox
        messagebox.showinfo("Success", f"Team '{selected_team}' removed successfully!")
    else:
        messagebox.showerror("Error", "Please select a team to remove.")

# Function to view players in a selected team
def view_team_players():
    selected_team = listbox.get("active")

    
     # Get selected team
    if not selected_team:
        messagebox.showerror("Error", "Please select a team to view players.")
        return

    try:
        print(f"Debug: Selected Team -> {selected_team}")  # Debugging
        players = get_team_players(selected_team)  # Fetch players from DB

        if not players:
            messagebox.showinfo("Info", f"No players found for team '{selected_team}'")
            return

        update_listbox(players)  # Show players in listbox
    except Exception as e:
        messagebox.showerror("Error", f"Error fetching players: {str(e)}")
# Function to display all players who are not assigned to any team
def show_unassigned_players():
    players = get_players()  # Fetch all players without a team
    update_listbox([f"{p[0]} - {p[1]}" for p in players])  # Format: Player Name - Role

# Function to assign a player to a selected team
def assign_player_to_team():
    selected_item = listbox.get("active")  # Get selected player
    if not selected_item:
        messagebox.showerror("Error", "Please select a player first.")
        return

    selected_team = listbox.get("active")  # Get selected team
    if not selected_team:
        messagebox.showerror("Error", "Please select a team.")
        return

    player_name = selected_item.split(" - ")[0]  # Extract player name
    update_player_team(player_name, selected_team)  # Update DB

    messagebox.showinfo("Success", f"Player '{player_name}' assigned to team '{selected_team}'!")
    show_unassigned_players()  # Refresh list to show only unassigned players

# Initialize Tkinter Window
window = Tk()
window.geometry("1368x720")
window.configure(bg="#FFFFFF")

canvas = Canvas(window, bg="#FFFFFF", height=720, width=1368, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)

# Background Images
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
canvas.create_image(1056, 360, image=image_image_1)

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
canvas.create_image(338, 366, image=image_image_2)

# Listbox with Scrollbar (for Players & Teams)
listbox_frame = Canvas(window, bg="white", width=300, height=400, bd=2, relief="ridge")
listbox_frame.place(x=780, y=80)  # Positioned Beside Image 1

scrollbar = Scrollbar(listbox_frame, orient="vertical")
listbox = Listbox(listbox_frame, yscrollcommand=scrollbar.set, font=("Iceland", 50), width=15, height=8)
scrollbar.config(command=listbox.yview)

listbox.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Buttons for Team & Player Management
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(image=button_image_1, borderwidth=0, highlightthickness=0, command=load_teams, relief="flat")  # Load teams
button_1.place(x=130, y=80, width=415, height=94)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(image=button_image_2, borderwidth=0, highlightthickness=0, command=add_new_team, relief="flat")  # Add team
button_2.place(x=130, y=220, width=415, height=94)

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(image=button_image_3, borderwidth=0, highlightthickness=0, command=remove_selected_team, relief="flat")  # Remove team
button_3.place(x=130, y=350, width=415, height=94)

button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_4 = Button(image=button_image_4, borderwidth=0, highlightthickness=0, command=view_team_players, relief="flat")  # View team players
button_4.place(x=130, y=480, width=415, height=94)



# Load teams initially
listbox.selection_clear(0, "end")
load_teams()


window.resizable(False, False)
window.mainloop()
