import tkinter as tk
from tkinter import ttk

def add_player():
    # Placeholder function to add a player
    pass

def edit_player():
    # Placeholder function to edit a selected player
    pass

def delete_player():
    # Placeholder function to delete a selected player
    pass

def refresh_table():
    # Placeholder function to refresh player data
    pass

# Create main window
window = tk.Tk()
window.title("Player Management")
window.geometry("800x500")
window.configure(bg="#F0F0F0")

# Search Bar
search_label = tk.Label(window, text="Search Player:")
search_label.pack(pady=5)
search_entry = tk.Entry(window, width=30)
search_entry.pack(pady=5)

# Player Table (Treeview)
tree = ttk.Treeview(window, columns=("ID", "Name", "Team", "Runs", "Wickets"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Team", text="Team")
tree.heading("Runs", text="Runs")
tree.heading("Wickets", text="Wickets")

tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Buttons
btn_frame = tk.Frame(window)
btn_frame.pack(pady=10)

add_btn = tk.Button(btn_frame, text="Add Player", command=add_player)
add_btn.grid(row=0, column=0, padx=5)

edit_btn = tk.Button(btn_frame, text="Edit Player", command=edit_player)
edit_btn.grid(row=0, column=1, padx=5)

delete_btn = tk.Button(btn_frame, text="Delete Player", command=delete_player)
delete_btn.grid(row=0, column=2, padx=5)

refresh_btn = tk.Button(btn_frame, text="Refresh", command=refresh_table)
refresh_btn.grid(row=0, column=3, padx=5)

window.mainloop()
