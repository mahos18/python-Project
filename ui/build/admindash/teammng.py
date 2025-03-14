import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
#from dbconnectionadmin import add_player_to_team, remove_team, add_team, get_players, get_teams, get_team_players

def open_team_management():
    root = tk.Toplevel()
    root.title("Team Management")
    root.geometry("700x500")
    
    # Dropdown for selecting teams
    tk.Label(root, text="Select Team:").grid(row=0, column=0, padx=10, pady=10)
    teams_dropdown = ttk.Combobox(root, state="readonly")
    teams_dropdown.grid(row=0, column=1, padx=10, pady=10)
    
    # Dropdown for selecting players
    tk.Label(root, text="Select Player:").grid(row=1, column=0, padx=10, pady=10)
    players_dropdown = ttk.Combobox(root, state="readonly")
    players_dropdown.grid(row=1, column=1, padx=10, pady=10)
    
    # Buttons
    tk.Button(root, text="Load Teams", command=lambda: load_teams()).grid(row=2, column=0, padx=10, pady=10)
    tk.Button(root, text="View Players in Team", command=lambda: view_team_players()).grid(row=2, column=1, padx=10, pady=10)
    tk.Button(root, text="Add Player to Team", command=lambda: assign_player()).grid(row=3, column=0, padx=10, pady=10)
    tk.Button(root, text="Delete Team", command=lambda: delete_team()).grid(row=4, column=0, padx=10, pady=10)
    tk.Button(root, text="Add New Team", command=lambda: create_team()).grid(row=5, column=0, padx=10, pady=10)
    
    # Table to display data
    columns = ("Name", "Role")
    table = ttk.Treeview(root, columns=columns, show="headings")
    table.heading("Name", text="Name")
    table.heading("Role", text="Role")
    table.grid(row=6, column=0, columnspan=3, padx=10, pady=10)
    
    def load_teams():
        table.delete(*table.get_children())
        teams = get_teams()
        for team in teams:
            table.insert("", "end", values=(team, "-"))
        teams_dropdown["values"] = teams
    
    def assign_player():
        player = players_dropdown.get()
        team = teams_dropdown.get()
        if player and team:
            add_player_to_team(player, team)
            messagebox.showinfo("Success", f"{player} added to {team}!")
            view_team_players()
        else:
            messagebox.showerror("Error", "Select a player and a team.")
    
    def delete_team():
        team = teams_dropdown.get()
        if team:
            remove_team(team)
            messagebox.showinfo("Success", f"Team {team} deleted!")
            load_teams()
        else:
            messagebox.showerror("Error", "Select a team.")
    
    def create_team():
        team_name = simpledialog.askstring("New Team", "Enter new team name:")
        if team_name:
            add_team(team_name)
            messagebox.showinfo("Success", f"Team {team_name} added!")
            load_teams()
    
    def view_team_players():
        table.delete(*table.get_children())
        team = teams_dropdown.get()
        if team:
            players = get_team_players(team)
            for player in players:
                table.insert("", "end", values=(player[0], player[1]))
        else:
            messagebox.showerror("Error", "Select a team.")
    
    load_teams()
    players_dropdown["values"] = get_players()
    
    root.mainloop()
