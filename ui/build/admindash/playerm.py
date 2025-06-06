
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,font,messagebox
from dbconnectionadmin import get_all_players,add_player,fetch_teams,delete_player,update_player,get_user_id,is_team_full
from tkinter import ttk
import tkinter as tk
import os

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Soham\Desktop\RAMDOM PROJECTS\cricket_league_management\ui\build\admindash\assets1\assetsplayer\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

tree = None 
def add():
    
    os.system("python admindash/addplayer.py")

    search()

def search():
    search_query = entry_1.get()
    standings = get_all_players(search_query)
    if not standings:
        messagebox.showerror("Error","No Data available")
        return

    style = ttk.Style()
    style.configure("Treeview", font=("Iceland", 22))  # Change font for rows
    style.configure("Treeview.Heading", font=("Iceland", 24, "bold")) 
    style.configure("Treeview", rowheight=38) # Change font for headings

    # Create Treeview widget
    columns = ("Player Id","Player Name","Role","Team Name")
    column_ratios = [0.2,0.3,0.2,0.3]  # Adjust ratios (sum should be 1.0)
    total_width = 500  # Set total width of the table

    global tree
    tree = ttk.Treeview(window, columns=columns, show="headings")
    # Define column headings & set width dynamically
    for col, ratio in zip(columns, column_ratios):
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=int(total_width * ratio))
    tree.place(x=140, y=240, width=900, height=420)  # Adjust placement & size

    # Insert data into the table
    for team in standings:
        tree.insert("", "end", values=(
            team["player_id"],
            team["player_name"],
            team["role"],
            team["team_name"]        
        ))
    return tree



    
    






def edit():
    global tree  # Use the global tree variable

    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a player to edit.")
        return

    # Get selected player's data
    player_data = tree.item(selected_item, "values")
    player_id, player_name, role, team_name = player_data  # Extract values

    # Edit Window
    edit_window = tk.Toplevel()
    edit_window.title("Edit Player")
    edit_window.geometry("300x250")

    tk.Label(edit_window, text="Player Name:").pack(pady=5)
    entry_name = tk.Entry(edit_window)
    entry_name.pack(pady=5)
    entry_name.insert(0, player_name)  # Pre-fill with existing name

    tk.Label(edit_window, text="Role:").pack(pady=5)
    role_var = tk.StringVar()
    role_dropdown = ttk.Combobox(edit_window, textvariable=role_var, values=["Batsman", "Bowler", "WicketKeeper"], state="readonly")
    role_dropdown.pack(pady=5)
    role_dropdown.set(role)  # Set current role

    tk.Label(edit_window, text="Team:").pack(pady=5)
    teams = fetch_teams()  # Fetch team list from database
    team_dict = {team[1]: team[0] for team in teams}  # Map team name to team ID
    team_var = tk.StringVar()
    team_dropdown = ttk.Combobox(edit_window, textvariable=team_var, values=list(team_dict.keys()), state="readonly")
    team_dropdown.pack(pady=5)
    team_dropdown.set(team_name)  # Set current team

    def submit_edit():
        new_name = entry_name.get().strip()
        new_role = role_var.get().strip()
        new_team_name = team_var.get().strip()
        new_team_id = team_dict.get(new_team_name, None)

        if not new_name:
            messagebox.showwarning("Input Error", "Player name is required.")
            return
        if not new_team_id:
            messagebox.showwarning("Input Error", "Please select a team.")
            return
        if is_team_full(new_team_id):  
            messagebox.showwarning("Team Error", "Team already has 11 players.")
            return 

        if update_player(player_id, new_name, new_role, new_team_id):
            search()
            tree.item(selected_item, values=(player_id, new_name, new_role, new_team_name))
            messagebox.showinfo("Success", "Player updated successfully!")
            edit_window.destroy()
        else:
            messagebox.showerror("Error", "Failed to update player.")

        # Update the UI
        

        
        

    tk.Button(edit_window, text="Save Changes", command=submit_edit).pack(pady=10)
    edit_window.mainloop()

    
def delete(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a player to delete.")
        return
    
    player_id = tree.item(selected_item, "values")[0]  # Assuming player_id is the first column

    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Player ID {player_id}?")
    if confirm:
        if delete_player(player_id):  # Call database function
            search()
            messagebox.showinfo("Success", "Player deleted successfully.")
            tree.delete(selected_item)  # Remove from UI
        else:
            messagebox.showerror("Error", "Failed to delete player.")




def profile():
    global tree
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a player to view the profile.")
        return
    
    player_id = tree.item(selected_item, "values")[0]  # Get selected player's player_id

    if not player_id:
        messagebox.showerror("Error", "Could not retrieve player ID.")
        return

    # Fetch user_id from the database using player_id
    user_id = get_user_id(player_id)

    if not user_id:
        messagebox.showerror("Error", "Could not retrieve User ID for the selected player.")
        return

    # Open playerdash.py with user_id as an argument
    os.system(f'python playerdash/playerdashnologout.py {user_id}')


window = Tk()

window.geometry("1368x720")
window.configure(bg = "#FFFFFF")
custom_font = font.Font(family="Iceland", size=30)
window.title("PlayerManagement")

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

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    414.0,
    59.0,
    image=image_image_2
)

canvas.create_rectangle(
    91.0,
    181.0,
    1087.0,
    690.0,
    fill="#F9F5C9",
    outline="")

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    347.0,
    186.0,
    image=image_image_3
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    347.0,
    186.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFF8F8",
    fg="#000716",
    font=custom_font,
    highlightthickness=0
)
entry_1.place(
    x=146.0,
    y=159.0,
    width=402.0,
    height=52.0
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=profile,
    relief="flat"
)
button_1.place(
    x=1107.0,
    y=629.0,
    width=172.0,
    height=61.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda:delete(tree),
    relief="flat"
)
button_2.place(
    x=1101.0,
    y=537.0,
    width=172.0,
    height=61.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=edit,
    relief="flat"
)
button_3.place(
    x=1101.0,
    y=445.0,
    width=172.0,
    height=61.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=add,
    relief="flat"
)
button_4.place(
    x=1101.0,
    y=353.0,
    width=172.0,
    height=61.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=search,
    relief="flat"
)
button_5.place(
    x=562.0,
    y=157.0,
    width=172.0,
    height=61.0
)

search()



window.resizable(False, False)
window.mainloop()
