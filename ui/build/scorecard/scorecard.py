from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox
import sys
from tkinter import ttk
import tkinter as tk
from dbconn import get_team_players,get_team_ids,get_team1_name,get_team2_name,complete_match_update
import os
import subprocess
from scoreboard import open_scoreboard



def load_match_id():
    """Fetches the user_id from command-line arguments if provided."""
    return sys.argv[1] if len(sys.argv) > 1 else None# Replace with actual logged-in user ID

#db
match_id = load_match_id()





# Initialize Window
# def scorecard(match_id, batting_team, bowling_team, batsman1, batsman2, bowler):
data1=[]
data2=[]


# match_id=110
def open_setup_window(match_id,ining):
    global data
    data=[]
    batsmen_list=dict()
    # remaining_batsmen_list=dict()
    bowlers_list=dict()
    print("match id:",match_id)
    # Create popup window
    popup = Tk()
    popup.title("Select Batting Team and Players")
    popup.geometry("400x300")
    if ining==1:
        heading = tk.Label(popup, text="INNING ONE", font=("Helvetica", 16, "bold"))
        heading.pack(pady=10)
    else:
        heading = tk.Label(popup, text="INNING TWO", font=("Helvetica", 16, "bold"))
        heading.pack(pady=10)

    # Batting team selection
    tk.Label(popup, text="Select Batting Team:").pack()
    team_var = tk.StringVar()
    team1_name,team2_name=get_team1_name(match_id),get_team2_name(match_id)
    team_dropdown = ttk.Combobox(popup, textvariable=team_var, values=[team1_name,team2_name])
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

    tk.Label(popup, text="Select Number of Overs:").pack()
    overs_var = tk.StringVar()
    overs_dropdown = ttk.Combobox(popup, textvariable=overs_var, values=["1","2", "3", "4"], state="readonly")
    overs_dropdown.pack()
    overs_dropdown.current(0)


    players=get_team_ids(match_id)
    team_id1=players[0]
    team_id2=players[1]
    print ("debug")
    print(team_id1)
    print(team_id2)
    team1_players=get_team_players(team_id1)
    print(team1_players)
    team2_players=get_team_players(team_id2)
    print(team2_players)

    # def update_remaining_player_dict():
    #     global remaining_batsmen_list
    #     b1=batsman1_var.get()
    #     b2=batsman1_var.get()
    #     print(b1,b2)
    #     keys_to_remove = [key for key, value in remaining_batsmen_list.items() if value in [b1, b2]]

    #     for key in keys_to_remove:
    #         del remaining_batsmen_list[key]
    #     print("remianing batsmen")
    #     print(remaining_batsmen_list)



    def update_player_lists(*args):

        global batsmen_list, remaining_batsmen_list, bowlers_list 
        batsman1_dropdown.set("")
        batsman2_dropdown.set("")
        bowler_dropdown.set("")
        
        batsman1_dropdown["values"] = []
        batsman2_dropdown["values"] = []
        bowler_dropdown["values"] = []


        selected_team = team_var.get()
        if selected_team == team1_name:
            batsmen_list = team1_players
            remaining_batsmen_list=batsmen_list
            bowlers_list = team2_players
        else:
            batsmen_list = team2_players
            remaining_batsmen_list=batsmen_list
            bowlers_list = team1_players
        
        batsman1_dropdown["values"] = list(batsmen_list.values())
        # remaining_batsmen_list = {pid: name for pid, name in batsmen_list.items() if name != selected_batsman1}
        # print("list_debug")
        # print (remaining_batsmen_list)
        batsman2_dropdown["values"] = list(batsmen_list.values())
        bowler_dropdown["values"] = list(bowlers_list.values())

    # def update_batsman2_dropdown():
    #     selected_batsman1 = batsman1_var.get()
        
    #     remaining_batsmen_list = {pid: name for pid, name in batsmen_list.items() if name != selected_batsman1}
        
    #     batsman2_dropdown.set("")
    #     batsman2_dropdown["values"] = list(remaining_batsmen_list.values())
    # batsman1_var.trace_add("write", update_batsman2_dropdown)
    team_dropdown.bind("<<ComboboxSelected>>", update_player_lists)

    def confirm_selection():
        global data
        if not (team_var.get() and batsman1_var.get() and batsman2_var.get() and bowler_var.get() and overs_var.get()):
            messagebox.showerror("Error", "All selections must be made!")
            return

        batting_team_name = team_var.get()
        bowling_team_name = team1_name if batting_team_name == team2_name else team2_name
        batsman1 = batsman1_var.get()
        batsman2 = batsman2_var.get()
        bowler = bowler_var.get()
        selected_overs = int(overs_var.get())

        messagebox.showinfo("Success", f"Match Setup:\nBatting Team: {batting_team_name}\nBatsmen: {batsman1}, {batsman2}\nBowler: {bowler}\nOvers: {selected_overs}")
        popup.destroy()
        print(batsmen_list, bowlers_list)
        # Pass overs too if open_scoreboard accepts it
        data=open_scoreboard(match_id, batting_team_name, bowling_team_name, batsman1, batsman2, bowler, batsmen_list, bowlers_list, selected_overs,ining)

    confirm_btn = tk.Button(popup, text="Confirm", command=confirm_selection)
    confirm_btn.pack()

    popup.mainloop()
    return data


data1=open_setup_window(match_id,1)
print(data1)
data2=open_setup_window(match_id,2)
if data1 and data2:
    def show_match_summary(data1, data2):
        popup = tk.Toplevel()
        popup.title("Match Summary")

        # Set Iceland 40 bold (you must have the Iceland font installed on your system)
        font_style = ("Iceland", 40, "bold")

        # Display data side by side
        for i in range(len(data1)):
            label1 = tk.Label(popup, text=str(data1[i]), font=font_style)
            label1.grid(row=i, column=0, padx=10, pady=5)

            label2 = tk.Label(popup, text=str(data2[i]), font=font_style)
            label2.grid(row=i, column=1, padx=10, pady=5)

        # Dropdown for winning team
        winning_label = tk.Label(popup, text="Winning Team:", font=font_style)
        winning_label.grid(row=len(data1), column=0, padx=10, pady=20)

        selected_team = tk.StringVar()
        dropdown = ttk.Combobox(popup, textvariable=selected_team, values=[data[0], data2[0]], font=font_style, state="readonly", width=15)
        dropdown.grid(row=len(data1), column=1, padx=10, pady=20)

        # Complete Match Button
        complete_btn = tk.Button(popup, text="Complete Match", font=font_style, command=complete_match_update(match_id, data1, data2, selected_team))
        complete_btn.grid(row=len(data1)+1, column=0, columnspan=2, pady=30)

    # Example usage
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # data = ["Team A", "150/5"]
    # data2 = ["Team B", "148/8"]

    show_match_summary(data1, data2)
    root.mainloop()
print(data1)
print(data2)