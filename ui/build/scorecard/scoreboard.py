from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox,font
import sys
from tkinter import ttk
import tkinter as tk
from dbconn import get_bowler_stats_by_team,get_player_id_by_name,init_match_statistics, increment_catches_taken,increment_runs_scored, increment_fours, increment_sixes,increment_overs_wickets_taken
import os

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Soham\Desktop\RAMDOM PROJECTS\cricket_league_management\ui\build\scorecard\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# def load_image(canvas, name):
#         try:
#             img = PhotoImage(file=relative_to_assets(name))
#             setattr(canvas, f"img_{name}", img)  # keep reference
#             return img
#         except Exception as e:
#             print(f"[ERROR] {name} could not be loaded: {e}")
#             return None

#ui

ining_run=0
ining_wickets=0
current_over=0
overs_data=[]
batsman_stats = {}
bowler_stats = {}
current_batsman="soham"
batsman1="soham"
batsman2="soham"
current_bowler="soham"
bowler="soham"
wik=0
match_score_text=""

def open_scoreboard(match_id, batting_team_name, bowling_team_name, b1, b2, bow, batsmen_list, bowlers_list,match_overs,ining):
    
    #add all player data to db by defualt as they played match
    init_match_statistics(match_id, batsmen_list, bowlers_list)
    global batsman1,batsman2
    batsman1=b1
    batsman2=b2
    bowler=bow
    
    

    #dictionaries
    global current_batsman,current_bowler
    current_batsman=batsman1
    current_bowler=bowler
    global wik
    wik=0
    global batsman_stats,bowler_stats
    
    global overs_data
   
    global ining_run
    global ining_wickets
    ining_run=0
    ining_wickets=0
    overs_data.clear()
    overs_data = [[] for _ in range(match_overs)]
    batsman_stats.clear()
    bowler_stats.clear()
    batsman_stats[batsman1] = {"runs": 0, "balls": 0}
    batsman_stats[batsman2] = {"runs": 0, "balls": 0}
    bowler_stats[current_bowler] = {"runs_conceded": 0, "wickets": 0, "balls": 0,"overs":0} 
    on_strike = {"is_striker_p1": True}

    window = Tk()
    window.geometry("1368x720")
    window.configure(bg="#FFFFFF")
    custom_font = font.Font(family="Iceland", size=30)
    custom_font25 = font.Font(family="Iceland", size=25)
    

    #functions
    
    def set_currentbowler(name):
        global current_bowler
        current_bowler=name
        

    def change_strike():
        global current_batsman
        if on_strike["is_striker_p1"]:
            canvas.itemconfig(s1, text="")    # remove strike from P1
            canvas.itemconfig(s2, text="*")
            current_batsman=batsman2  # give strike to P2
        else:
            canvas.itemconfig(s1, text="*")   # give strike to P1
            canvas.itemconfig(s2, text="")
            current_batsman=batsman1    # remove strike from P2

        on_strike["is_striker_p1"] = not on_strike["is_striker_p1"]

    def add_delivery(outcome):
        global current_over, overs_data
        
        # Count only legal deliveries
        legal_deliveries = [b for b in overs_data[current_over] if b not in ["WD", "NB","EX+1","EX+2","EX+3","EX+4","EX+6"]]
        
        if len(legal_deliveries) >= 6:
            messagebox.showerror("Error", "Over completed procedd to next over.")
            return False
        else:
            
            overs_data[current_over].append(outcome)
            canvas.itemconfig(over_bowls, text=overs_data[current_over])
            if len(overs_data[current_over])>9:
                canvas.itemconfig(over_bowls, font=("Iceland",33))
            if len(overs_data[current_over])>6:
                canvas.itemconfig(over_bowls, font=("Iceland",45))
            return True
          
    
    def update_over_scores():
        global current_bowler
        cb=current_bowler
        wickets=bowler_stats[cb]["wickets"]
        runs_conceded=bowler_stats[cb]["runs_conceded"]
        overs=1
        bowler_id = get_player_id_by_name(cb.strip().title())
        print(cb)
        print(bowler_id)
        print(overs_data[current_over])
        increment_overs_wickets_taken(wickets,overs,runs_conceded,match_id,bowler_id)
        bowler_stats[current_bowler] = {"runs_conceded": 0, "wickets": 0, "balls": 0,"overs":0} 
        
       
    def complete_ining():
        global match_score_text
        update_over_scores()
        summary_win = tk.Toplevel()
        summary_win.title("Inning Summary")
        summary_win.geometry("800x800")
        
        # Title

        tk.Label(summary_win, text="Inning Summary", font=("Iceland", 58, "bold")).pack(pady=10)
        match_score_text = f"{ining_run} / {ining_wickets}"
        tk.Label(summary_win, text=match_score_text, font=("Iceland", 60), fg="#004aad").pack(pady=10)
        

        # ----- Batsman Stats Table -----

        batsman_frame = tk.Frame(summary_win)
        batsman_frame.pack(pady=10)
        tk.Label(batsman_frame, text="Batsman Stats", font=("Iceland", 30, "bold")).grid(row=0, column=0, columnspan=3)

        tk.Label(batsman_frame, text="Name", font=("Iceland", 30, "underline")).grid(row=1, column=0, padx=10)
        tk.Label(batsman_frame, text="Runs", font=("Iceland", 30, "underline")).grid(row=1, column=1, padx=10)
        tk.Label(batsman_frame, text="Balls", font=("Iceland", 30, "underline")).grid(row=1, column=2, padx=10)

        for idx, (name, stats) in enumerate(batsman_stats.items(), start=2):
            tk.Label(batsman_frame, text=name, font=("Iceland", 30, "underline")).grid(row=idx, column=0, padx=10)
            tk.Label(batsman_frame, text=str(stats["runs"]), font=("Iceland", 30, "underline")).grid(row=idx, column=1, padx=10)
            tk.Label(batsman_frame, text=str(stats["balls"]), font=("Iceland", 30, "underline")).grid(row=idx, column=2, padx=10)
        

        

        # ----- Bowler Stats Table -----
        bowler_frame = tk.Frame(summary_win)
        bowler_frame.pack(pady=10)

        bowler_stats = get_bowler_stats_by_team(match_id, bowling_team_name)

        tk.Label(bowler_frame, text="Bowler Stats", font=("Iceland", 30, "bold")).grid(row=0, column=0, columnspan=2)
        tk.Label(bowler_frame, text="Name", font=("Iceland", 30, "bold")).grid(row=1, column=0, padx=10)
        tk.Label(bowler_frame, text="W-R(O)", font=("Iceland", 30, "bold")).grid(row=1, column=1, padx=10)

        for idx, (name, stats) in enumerate(bowler_stats.items(), start=2):
            summary = f"{stats['wickets']}-{stats['runs_conceded']}({stats['overs']})"
            tk.Label(bowler_frame, text=name,font=("Iceland", 30, "underline")).grid(row=idx, column=0, padx=10)
            tk.Label(bowler_frame, text=summary,font=("Iceland", 30, "underline")).grid(row=idx, column=1, padx=10)

        

        # ----- Over Data Table -----
        



        # Close Button
        tk.Button(summary_win, text="Start Next Inining", command=summary_win.destroy,font=("Iceland", 30, "underline")).pack(pady=10)
   
    def update_batsmen_stats(batsman,num):
        global current_batsman,batsman_stats
        current_batsman=batsman
        print(current_batsman)
        update_playerscore_after_wicket(num,batsman_stats[current_batsman]["runs"],batsman_stats[current_batsman]["balls"])

    def change_batsman(out_batsman_num):
        
        def submit_new_batsman():
            new_batsman = new_batsman_var.get()
            if not new_batsman:
                messagebox.showerror("Error", "Please select a new batsman.")
                return

            nonlocal out_batsman_num
            print("out batsmen no:",out_batsman_num)
            global batsman1,batsman2,batsman_stats
            # print("batsman1 ,batsman2",batsman1,batsman2)
            if out_batsman_num == 1:
                
                
                batsman1 = new_batsman
                batsman_stats[new_batsman] = {"runs": 0, "balls": 0}
                update_batsmen_stats(batsman1,out_batsman_num)
                canvas.itemconfig(P1, text=new_batsman)
                if on_strike["is_striker_p1"]:
                    canvas.itemconfig(s1, text="*")
                    canvas.itemconfig(s2, text="")
                    on_strike["is_striker_p1"] = True
                else:
                    canvas.itemconfig(s1, text="")
                    canvas.itemconfig(s2, text="*")
                    on_strike["is_striker_p1"] = False
            else:
                
                batsman2 = new_batsman
                # batsman_stats[batsman2] = {"runs": 0, "balls": 0}
                batsman_stats[new_batsman] = {"runs": 0, "balls": 0}
                update_batsmen_stats(batsman2,out_batsman_num)
                canvas.itemconfig(P2, text=new_batsman)
                if not on_strike["is_striker_p1"]:
                    canvas.itemconfig(s1, text="")
                    canvas.itemconfig(s2, text="*")
                    on_strike["is_striker_p1"] = False
                else:
                    canvas.itemconfig(s1, text="*")
                    canvas.itemconfig(s2, text="")
                    on_strike["is_striker_p1"] = True

            for k, v in list(batsmen_list.items()):
                if v == new_batsman:
                    batsmen_list.pop(k)
                    break
                
            popup.destroy()

            # ✅ Notify the original function with new batsman
            # update_callback(new_batsman)

        popup = tk.Toplevel()
        popup.title("New Batsman Selection")
        popup.geometry("300x150")

        tk.Label(popup, text="Select New Batsman").pack(pady=10)

        new_batsman_var = tk.StringVar()
        dropdown = ttk.Combobox(popup, textvariable=new_batsman_var)

        # Filter out already playing batsmen
        already_playing = [batsman1, batsman2]
        remaining_batsmen = [name for name in batsmen_list.values() if name not in already_playing]
        
        dropdown["values"] = remaining_batsmen
        if remaining_batsmen:
            new_batsman_var.set(remaining_batsmen[0])
        dropdown.pack(pady=5)

        tk.Button(popup, text="Submit", command=submit_new_batsman).pack(pady=10)

        popup.grab_set()

        # return 







    # Create Canvas

    
    batsman1=batsman1
    # Batsman stats: {name: {"runs": 0, "balls": 0}}
    
    # Bowler stats: {name: {"runs_conceded": 0, "wickets": 0, "balls": 0}}
    
    current_batsman=batsman1
    
    

    # def check_over_or_wicket():
    #     if bowler_stats[current_bowler]["balls"] == 6:
    #         save_bowler_to_db(current_bowler)
    #         # select new bowler...
        
    #     if batsman_out:  # handle this in your event
    #         save_batsman_to_db(current_batsman)
    #         # replace with next batsman...


    #buttonfunctions  
    def update_inning_score(runs_value, wickets_value):
        canvas.itemconfig(runs, text=str(runs_value).zfill(3))      # Format to 3 digits
        canvas.itemconfig(wickets, text=str(wickets_value).zfill(2))  # Format to 2 digits
    def update_playerscore_after_wicket(x,y,z):
        if x==1:
            canvas.itemconfig(P1_runs, text=y)      # Format to 3 digits
            canvas.itemconfig(P1_bowls, text=z)
        else:
            canvas.itemconfig(P2_runs, text=y)      # Format to 3 digits
            canvas.itemconfig(P2_bowls, text=z) 

    def update_playerscore(x,y,z):
        if x==batsman1:
            canvas.itemconfig(P1_runs, text=y)      # Format to 3 digits
            canvas.itemconfig(P1_bowls, text=z)
        else:
            canvas.itemconfig(P2_runs, text=y)      # Format to 3 digits
            canvas.itemconfig(P2_bowls, text=z)  
    
    def addrun(runs):
        global current_batsman, current_bowler, batsman_stats
        global batsman1, batsman2  # Ensure batsman1 and batsman2 are global
        global ining_run,ining_wickets
        print(current_batsman)
        print(batsman1,batsman2)
        b1=batsman1
        b2=batsman2
        if add_delivery(runs):
            current_bowler = bowler
            ining_run += runs
            update_inning_score(ining_run, ining_wickets)

            if on_strike["is_striker_p1"]:
                current_batsman = b1  # Access batsman1 globally
            else:
                current_batsman = b2  # Access batsman2 globally

            print(current_batsman)

            # Update the batsman's stats
            batsman_stats[current_batsman]["runs"] += runs
            batsman_stats[current_batsman]["balls"] += 1
            bowler_stats[current_bowler]["runs_conceded"] += runs
            bowler_stats[current_bowler]["balls"] += 1

            print(batsman_stats[current_batsman])
            # Handle fours and sixes
            if runs == 4:
                print(batsmen_list)
                batsman_id = get_player_id_by_name(current_batsman.strip().title())
                print(current_batsman)
                print(batsman_id)
                increment_fours(match_id, batsman_id)

            if runs == 6:
                batsman_id =  get_player_id_by_name(current_batsman.strip().title())
                print(current_batsman)
                print(batsman_id)
                if increment_sixes(match_id, batsman_id):
                    print("6 added in db" )

            # Handle deliveries and over
            legal_deliveries = [b for b in overs_data[current_over] if b not in ["WD", "NB"]]
            update_playerscore(current_batsman, batsman_stats[current_batsman]["runs"], batsman_stats[current_batsman]["balls"])
            
            if len(legal_deliveries) == 6:
                next_buton.config(state="normal")
                
                bowler_stats[current_bowler]["overs"] += 1

            if runs == 1 or runs == 3:
                change_strike()

            if current_over + 1 >= match_overs:
                next_buton.config(text="Complete Ining")
                next_buton.config(width=524)
                next_buton.config(font=("Iceland", 20))
                next_buton.config(command=complete_ining)

            print(f"addrun({runs})")
            return

        
            
        
            

    def extra():
        def submit_extra():
            runs = extra_var.get()
            strike_change = strike_var.get()
            if strike_change=="Yes":
                change_strike()
            
            if not runs:
                messagebox.showerror("Error", "Please select runs")
                return
            
            # Call your logic here
            runss="EX+"+runs
            add_delivery(runss)
            intruns=int(runs)
            bowler_stats[current_bowler]["runs_conceded"]+=intruns
            
            # Close popup
            extra_popup.destroy()

        extra_popup = tk.Toplevel()
        extra_popup.title("Extra Run Info")
        extra_popup.geometry("300x200")

        tk.Label(extra_popup, text="Select Extra Runs:").pack(pady=5)
        extra_var = tk.StringVar()
        extra_dropdown = ttk.Combobox(extra_popup, textvariable=extra_var, values=["1", "2", "3", "4", "6"])
        extra_dropdown.pack()

        tk.Label(extra_popup, text="Change Strike?").pack(pady=10)
        strike_var = tk.StringVar(value="No")  # Default value
        
        tk.Radiobutton(extra_popup, text="Yes", variable=strike_var, value="Yes").pack()
        tk.Radiobutton(extra_popup, text="No", variable=strike_var, value="No").pack()

        submit_btn = tk.Button(extra_popup, text="Submit", command=submit_extra)
        submit_btn.pack(pady=10)

        extra_popup.grab_set()

    def Noball():
        add_delivery("NB")
        bowler_stats[current_bowler]["runs_conceded"]+=1

    def catch():
      
        def submit_catch():
            catcher = catcher_var.get()
            if not catcher:
                messagebox.showerror("Error", "Please select the fielder who took the catch.")
                return
            player_id = next((k for k, v in bowlers_list.items() if v == catcher), None)
            increment_catches_taken(match_id,player_id)
            # You can now call your update logic here using `catcher`
            # Example: update_wicket_info(match_id, current_batsman, current_bowler, catcher)
            catch_popup.destroy()
            wicket()

        catch_popup = tk.Toplevel()
        catch_popup.title("Catch Details")
        catch_popup.geometry("300x150")

        tk.Label(catch_popup, text="Who took the catch?").pack(pady=10)

        catcher_var = tk.StringVar()
        catcher_dropdown = ttk.Combobox(catch_popup, textvariable=catcher_var)

        # 🏏 Add fielders (like bowlers or others in your bowlers_list)
        catcher_dropdown["values"] = list(bowlers_list.values())  # or a separate fielders list
        catcher_dropdown.pack(pady=5)

        submit_btn = tk.Button(catch_popup, text="Submit", command=submit_catch)
        submit_btn.pack(pady=10)
        

        catch_popup.grab_set()

    def wide():
        add_delivery("WD")
        bowler_stats[current_bowler]["runs_conceded"]+=1

    def wicket():
        global wik
        bowler_stats[current_bowler]["wickets"]+=1
        runs=batsman_stats[current_batsman]["runs"]
        balls=batsman_stats[current_batsman]["balls"]
        wik+=1
        canvas.itemconfig(wickets,text=wik)
        # wickets.config(text=wik)
        batsman_id = next((k for k, v in batsmen_list.items() if v == current_batsman), None)
        increment_runs_scored(match_id,batsman_id,runs,balls)
        add_delivery("W")
        if on_strike["is_striker_p1"]:
            change_batsman(1)
        else:
            change_batsman(2)

    def nextover():
        # Popup to change the bowler
        change_strike()
        update_over_scores()
        bowler_popup = tk.Toplevel()
        bowler_popup.title("Select New Bowler")
        bowler_popup.geometry("300x150")
        canvas.itemconfig(over_bowls, text="")

        tk.Label(bowler_popup, text="Select New Bowler:").pack(pady=10)

        new_bowler_var = tk.StringVar()
        bowler_dropdown = ttk.Combobox(bowler_popup, textvariable=new_bowler_var, values=list(bowlers_list.values()))
        bowler_dropdown.pack(pady=5)

        def set_new_bowler():
            global current_bowler, current_over, overs_data,bowler_stats

            selected_bowler = new_bowler_var.get()
            if not selected_bowler:
                messagebox.showerror("Error", "Please select a bowler.")
                return
            
            set_currentbowler(selected_bowler)
            bowler_stats[current_bowler] = {"runs_conceded": 0, "wickets": 0, "balls": 0,"overs":0} 
            update_scoreboard(batsman1, batsman2, current_bowler)
            print(current_bowler)
            current_over += 1
            bowler_popup.destroy()

            print(f"New Over: {current_over + 1}, New Bowler: {current_bowler}")
            # You can also update a label in your scoreboard UI if needed
            next_buton.config(state="disabled")

        confirm_button = tk.Button(bowler_popup, text="Confirm", command=set_new_bowler)
        confirm_button.pack(pady=10)


    def update_teamNames():
        canvas.itemconfig(team1, text=batting_team_name)
        canvas.itemconfig(team2, text=bowling_team_name)
        canvas.itemconfig(current_batting_team, text=batting_team_name)

    def update_scoreboard(new_batsman1, new_batsman2, new_bowler):
        canvas.itemconfig(P1, text=new_batsman1)
        canvas.itemconfig(P2, text=new_batsman2)
        canvas.itemconfig(bowler_name, text=new_bowler)



    # Scoreboard Text

    #ui
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
    canvas.image_1 = image_image_1 
    canvas.create_image(1114.0, 247.0, image=canvas.image_1)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    canvas.image_2 = image_image_2
    canvas.create_image(681.0, 59.0, image=canvas.image_2)

    image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
    canvas.image_3 = image_image_3 
    canvas.create_image(427.0, 247.0, image=canvas.image_3)

    image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
    canvas.image_4 = image_image_4 
    canvas.create_image(428.0, 447.0, image=canvas.image_4)

    image_image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
    canvas.image_5 = image_image_5 
    canvas.create_image(430.0, 609.0, image=canvas.image_5)

    image_image_6 = PhotoImage(file=relative_to_assets("image_6.png"))
    canvas.image_6 = image_image_6 
    canvas.create_image(1115.0, 543.0, image=canvas.image_6)

    team1 = canvas.create_text(124.0, 29.0, anchor="nw", text="Team name 1", fill="#000000", font=("Iceland", 53))
    team2 = canvas.create_text(840.0, 29.0, anchor="nw", text="Team name 2", fill="#000000", font=("Iceland", 53))
    canvas.create_text(644.0, 38.0, anchor="nw", text="V/S", fill="#000000", font=("Iceland", 53))

    image_image_7 = PhotoImage(file=relative_to_assets("image_7.png"))
    canvas.image_7 = image_image_7 
    canvas.create_image(427.0, 181.0, image=canvas.image_7)

    image_image_8 = PhotoImage(file=relative_to_assets("image_8.png"))
    canvas.image_8 = image_image_8 
    canvas.create_image(427.0, 299.0, image=canvas.image_8)

    # Buttons
    BUTTON_WIDTH = 91
    BUTTON_HEIGHT = 91
    button_positions = [
        (73, 399),(195, 399), (683, 398),(509, 557), (204, 557), (317, 398),
        (561, 399),  (702, 557), (54, 557),
        (343, 557),  (439, 399)
    ]
    button_texts = [
        "0", "1", "6", "CATCH", "NB",
        "2", "4", "W", "EX", "WIDE", "3"
    ]
    def fun(i):
        switch = {
            0: lambda: addrun(0),
            1: lambda: addrun(1),
            5: lambda: addrun(2),
            10: lambda: addrun(3),
            6: lambda: addrun(4),
            2: lambda: addrun(6),
            8: extra,
            4: Noball,
            3: catch,
            9: wide,
            7: wicket
            
        }
        action = switch.get(i, lambda: print("Invalid option"))
        action()

    white = "white"
    red = "#ff0000"
    black = "black"
    buttons = []
    for i, (x, y) in enumerate(button_positions):
        button_name="btn{i}"
        button_name= tk.Button(
            window,
            text=button_texts[i],
            width=BUTTON_WIDTH // 7,
            height=BUTTON_HEIGHT // 20,
            font=custom_font25 if button_texts[i] in ["CATCH", "WIDE"] else custom_font,
            bg=red if button_texts[i] in ["CATCH", "W"] else white,
            fg=white if button_texts[i] in ["CATCH", "W"] else black,
            activebackground="#45a049",
            activeforeground="white",
            command=lambda i=i:fun(i)
        )
        button_name.lift()
        button_name.place(x=x, y=y, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
        buttons.append(button_name)
    P1 = canvas.create_text(47.0, 151.0, anchor="nw", text="player 1", fill="#000000", font=("Iceland", 51))
    P2 = canvas.create_text(47.0, 269.0, anchor="nw", text="player 2", fill="#000000", font=("Iceland", 51))
    P1_runs = canvas.create_text(570.0, 151.0, anchor="nw", text="00", fill="#000000", font=("Iceland", 51))
    P2_runs = canvas.create_text(570.0, 269.0, anchor="nw", text=batsman_stats[batsman1]["balls"], fill="#000000", font=("Iceland", 51))
    P1_bowls = canvas.create_text(686.0, 161.0, anchor="nw", text="00", fill="#000000", font=("Iceland", 35))
    P2_bowls = canvas.create_text(686.0, 279.0, anchor="nw", text="00", fill="#000000", font=("Iceland", 35))
    s1 = canvas.create_text(754.0, 151.0, anchor="nw", text="*", fill="#000000", font=("Iceland", 56))
    s2 = canvas.create_text(753.0, 278.0, anchor="nw", text="", fill="#000000", font=("Iceland", 56))
    current_batting_team = canvas.create_text(893.0, 135.0, anchor="nw", text="TEAM NAME", fill="#FFFFFF", font=("Iceland", 40))
    runs = canvas.create_text(942.0, 212.0, anchor="nw", text="000", fill="#FFFFFF", font=("Iceland", 60))
    slash = canvas.create_text(1109.0, 210.0, anchor="nw", text="/", fill="#FFFFFF", font=("Iceland", 60))
    wickets = canvas.create_text(1154.0, 212.0, anchor="nw", text=wik, fill="#FFFFFF", font=("Iceland", 60))
    bowler_name = canvas.create_text(893.0, 408.0, anchor="nw", text="bowler name", fill="#F81115", font=("Iceland", 50))
    over_bowls = canvas.create_text(893.0, 488.0, anchor="nw", text="", fill="#6E2323", font=("Iceland", 60))
    next_buton=tk.Button(
            window,
            text="NEXT OVER",
            width=BUTTON_WIDTH // 7,
            height=BUTTON_HEIGHT // 20,
            font=custom_font25 if button_texts[i] in ["CATCH", "WIDE"] else custom_font,
            bg=red if button_texts[i] in ["CATCH", "W"] else white,
            fg=white if button_texts[i] in ["CATCH", "W"] else black,
            activebackground="#45a049",
            activeforeground="white",
            command=nextover
        )
    next_buton.place(x=893.0, y=588.0, width=190, height=70)
    next_buton.config(state="disabled")
    # Internal update functions
    update_teamNames()
    update_scoreboard(batsman1, batsman2, bowler)
    window.resizable(False, False)

    window.mainloop()
    return batting_team_name,match_score_text

# Match_ID= 110
# Batting_Team="Dadar Dashers"
# Bowling_Team="Matunga Blasters"
# Batsman_1="Naveen Joshi"
# Batsman_2="Kishore Dubey"
# Bowler="Abhishek Tiwari"
# Batsmen_List= {22: 'Naveen Joshi', 21: 'Kishore Dubey', 20: 'Arvind Sharma', 19: 'Suraj Pandey', 18: 'Gopal Shetty', 17: 'Ravi Thakur', 16: 'Deepak Mishra', 15: 'Soham Lohote', 14: 'Sandeep Pawar', 13: 'Anil Saxena', 12: 'Yogesh Iyer'}
# Bowlers_List= {33: 'Tarun Mehta', 32: 'Abhishek Tiwari', 31: 'Jayesh Pandey', 30: 'Ashok Rawat', 29: 'Nitin Chauhan', 28: 'Ramesh Yadav', 27: 'Sunil Pillai', 26: 'Mohan Babu', 25: 'Karthik Reddy', 24: 'Rajeev Kapoor', 23: 'Prakash Menon'}
# overs=1

# hello=open_scoreboard(
#     Match_ID,
#     Batting_Team,
#     Bowling_Team,
#     Batsman_1,
#     Batsman_2,
#     Bowler,
#     Batsmen_List,
#     Bowlers_List,
#     overs,
#     1
# )