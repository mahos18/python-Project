import mysql.connector
from mysql.connector import Error
import smtplib
import random
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re

def connect_db():
    """Establish and return a database connection."""
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="cricket-league-management"
        )
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None



def get_teams():
    """Fetch all team names."""
    connection = connect_db()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT team_name FROM teams")
        teams = [row[0] for row in cursor.fetchall()]
        return teams
    except Error as e:
        print(f"Error fetching teams: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def add_team(team_name):
    """Add a new team."""
    connection = connect_db()
    if not connection:
        return
    
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO teams (team_name) VALUES (%s)", (team_name,))
        connection.commit()
    except Error as e:
        print(f"Error adding team: {e}")
    finally:
        cursor.close()
        connection.close()

def remove_team(team_name):
    """Remove a team and unassign its players."""
    connection = connect_db()
    if not connection:
        return
    
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE players SET team_id = NULL WHERE team_id = (SELECT team_id FROM teams WHERE team_name = %s)", (team_name,))
        cursor.execute("DELETE FROM teams WHERE team_name = %s", (team_name,))
        connection.commit()
    except Error as e:
        print(f"Error removing team: {e}")
    finally:
        cursor.close()
        connection.close()

def update_player_team(player_name, team_name):
    """Assign a player to a team."""
    connection = connect_db()
    if not connection:
        return
    
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE players SET team_id = (SELECT team_id FROM teams WHERE team_name = %s) WHERE player_name = %s", (team_name, player_name))
        connection.commit()
    except Error as e:
        print(f"Error updating player's team: {e}")
    finally:
        cursor.close()
        connection.close()
def get_team_players(team_name): 
    connection = connect_db()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT player_name, role FROM players WHERE team_id =(SELECT team_id FROM teams WHERE team_name = %s)",(team_name,))
        players = [row[0] for row in cursor.fetchall()]
        return players
    except Error as e:
        print(f"Error fetching players: {e}")
        return []
    finally:
        cursor.close()
        connection.close()



def get_most_runs():
    connection = connect_db()
    cursor = connection.cursor()
    
    query = """SELECT p.player_name, t.team_name, p.runs 
                FROM players p
                JOIN teams t ON p.team_id = t.team_id
                ORDER BY p.runs DESC 
                ;"""
    cursor.execute(query)
    data = cursor.fetchall()
    
    connection.close()
    return data

def get_most_wickets():
    connection = connect_db()
    cursor = connection.cursor()
    
    query = """SELECT p.player_name, t.team_name, p.wickets 
                FROM players p
                JOIN teams t ON p.team_id = t.team_id
                ORDER BY p.wickets DESC 
                ;"""
    cursor.execute(query)
    data = cursor.fetchall()
    
    connection.close()
    return data

def get_highest_strike_rate():
    connection = connect_db()
    cursor = connection.cursor()
    
    query = """SELECT p.player_name, t.team_name, 
                (SUM(ps.runs_scored) / NULLIF(SUM(ps.balls_faced), 0)) * 100 AS strike_rate
            FROM player_statistics ps
            JOIN players p ON ps.player_id = p.player_id
            JOIN teams t ON p.team_id = t.team_id
            GROUP BY p.player_id, t.team_name
            ORDER BY strike_rate DESC
            ;
            """
    cursor.execute(query)
    data = cursor.fetchall()
    
    connection.close()
    return data

def get_points_table():
    connection = connect_db()
    cursor = connection.cursor()
    
    query = """
        SELECT team_name, matches_played, wins, losses,points
        FROM standings 
        ORDER BY points DESC
        """   
    cursor.execute(query)
    data = cursor.fetchall()
    
    connection.close()
    return data

# Database connection function





# 1. Fetch all players
def get_all_players(search=""):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT p.player_id, p.player_name, p.role, t.team_name 
        FROM players p 
        LEFT JOIN teams t ON p.team_id = t.team_id
        WHERE p.player_name LIKE %s OR t.team_name LIKE %s OR p.player_id LIKE %s
    """
    
    search_pattern = f"%{search}%"  # Add wildcards for partial match
    cursor.execute(query, (search_pattern, search_pattern,search_pattern))
    players = cursor.fetchall()
    conn.close()
    return players

def add_user(username, password, email, role):
    try:
        conn= connect_db()
        cursor = conn.cursor()

        # Check if the username already exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        if result[0] > 0:
            return "username_error"

        # Insert new player
        cursor.callproc('add_player_if_role_isplayer', (username, password, email, role))
        conn.commit()
        return True

    except mysql.connector.Error as err:
        print (f"Database Error: {err}")
        return False

    finally:
        cursor.close()
        conn.close()



verification_codes = {}
def send_verification_email(receiver_email):
   
    verification_code = str(random.randint(1000, 9999))  # Generate 6-digit OTP
    verification_codes[receiver_email] = verification_code  # Store OTP for checking later

    sender_email = "sohamlohote@gmail.com"  # Your email
    sender_password = "xcsx lnej szxw gnpo"  # Use App Password (NOT your email password)

    msg = EmailMessage()
    msg.set_content(f"Your verification code is: {verification_code}")
    msg["Subject"] = "Email Verification"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    except smtplib.SMTPRecipientsRefused:
        return "error"
    except smtplib.SMTPAuthenticationError:
        return "error"
    except smtplib.SMTPConnectError:
        return "error"
    except Exception as e:
        return "error"

def emailalreadyexist(email):
    try:
        conn= connect_db()
        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        existing_user = cursor.fetchone()
        cursor.close()
        conn.close()
        if existing_user:
            return True
        else:
            return False
        
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return None

def usernamealreadyexist(username):
    try:
        conn= connect_db()
        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (username,))
        existing_user = cursor.fetchone()
        cursor.close()
        conn.close()
        if existing_user:
            return True
        else:
            return False
        
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return None


def verify_email_code(email, code):
    return verification_codes.get(email) == code

def is_team_full(team_id):
    conn = connect_db()  # Ensure connect_db() is implemented
    cursor = conn.cursor()
    try:
        query = "SELECT COUNT(*) FROM players WHERE team_id = %s"
        cursor.execute(query, (team_id,))
        count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return count >= 11 
    except Error as e:
        print(f"Error fetching players: {e}")
        return False


# 2. Add a new player
def add_player(player_name,role,team_id,username):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        query = "UPDATE players  SET player_name = %s, role = %s, team_id = %s WHERE  user_id=(SELECT user_id FROM users WHERE username =%s)"
        cursor.execute(query, (player_name, role,team_id,username))
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print(f"Error fetching players: {e}")
        return False
    

# 3. Update player details
def update_player(player_id, new_name, new_role, new_team_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        query = "UPDATE players SET player_name = %s, role = %s, team_id = %s WHERE player_id = %s"
        cursor.execute(query, (new_name, new_role, new_team_id, player_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True  # Success
    except Exception as e:
        print("Error updating player:", e)
        return False  # Failure
# 4. Delete a player
def delete_player(player_id):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        query = "DELETE FROM players WHERE player_id=%s"
        cursor.execute(query, (player_id,))
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print(f"Error fetching players: {e}")
        return False

# 5. Get player details by ID
def get_player_by_id(player_id):
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT player_id, player_name, age, role, team_id FROM players WHERE player_id=%s"
    cursor.execute(query, (player_id,))
    player = cursor.fetchone()
    conn.close()
    return player

def fetch_teams():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT team_id, team_name FROM teams")
        teams = cursor.fetchall()
        conn.close()
        return teams
    except Exception as e:
        print("Error fetching teams:", e)
        return []
    
def get_user_id(player_id):
    """Fetch the user_id associated with the given player_id from the database."""
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT user_id FROM players WHERE player_id = %s", (player_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print("Database Error:", e)
        return None
    finally:
        cursor.close()
        conn.close()

def remove_user(username):
    """Remove a team and unassign its players."""
    connection = connect_db()
    if not connection:
        return
    
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM players WHERE userid = (SELECT user_id FROM users WHERE username=%s)", (username,))
        cursor.execute("DELETE FROM users WHERE username = %s", (username,))
        connection.commit()
    except Error as e:
        print(f"Error removing team: {e}")
    finally:
        cursor.close()
        connection.close()

#match management

def get_standings():
    conn =connect_db()
    if not conn:
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT team_name, matches_played, wins, losses,points
        FROM standings 
        ORDER BY points DESC
        """
        cursor.execute(query)
        standings = cursor.fetchall()  # List of dictionaries
        return standings  
    except mysql.connector.Error as e:
        print("Error fetching standings:", e)
        return None
    finally:
        conn.close()

def get_matches():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT m.match_id AS ID,t1.team_name AS team1, 
        t2.team_name AS team2, 
        m.status, 
        COALESCE(w.team_name, 'Not Decided') AS winner
            FROM Matches m
            JOIN Teams t1 ON m.team1_id = t1.team_id
            JOIN Teams t2 ON m.team2_id = t2.team_id
            LEFT JOIN Teams w ON m.winner_team_id = w.team_id;
        """
        cursor.execute(query)
        matches = cursor.fetchall()
        return matches
    except mysql.connector.Error as e:
        print("Error fetching matches:", e)
        return None
    finally:
        conn.close()

def add_match(team1_id, team2_id):
    conn = connect_db()
    cursor = conn.cursor()

    insert_query = "INSERT INTO matches (team1_id, team2_id, status) VALUES (%s, %s, 'Scheduled')"
    
    try:
        cursor.execute(insert_query, (team1_id, team2_id))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return False
    finally:
        conn.close()

def fetch_teams():
    conn = connect_db()
    cursor = conn.cursor()
    
    query = "SELECT team_id, team_name FROM Teams"
    
    try:
        cursor.execute(query)
        teams = cursor.fetchall()  # Returns a list of tuples (team_id, team_name)
        return teams
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return []
    finally:
        conn.close()

def remove_match(match_id):
    conn = connect_db()
    cursor = conn.cursor()

    delete_query = "DELETE FROM matches WHERE match_id = %s"
    
    try:
        cursor.execute(delete_query, (match_id,))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return False
    finally:
        conn.close()


def reschedule_all_matches():
    conn=connect_db()    
    cursor = conn.cursor()

    try:
        # Delete all scheduled matches
        delete_query = "DELETE FROM matches WHERE status = 'Scheduled'"
        cursor.execute(delete_query)
        
        # Fetch all teams
        teams = fetch_teams()
        team_ids = [team[0] for team in teams]

        # Insert new match schedules (each team plays against every other team)
        insert_query = "INSERT INTO matches (team1_id, team2_id, status) VALUES (%s, %s, 'Scheduled')"
        for i in range(len(team_ids)):
            for j in range(i+1, len(team_ids)):  # Avoid duplicate matches
                cursor.execute(insert_query, (team_ids[i], team_ids[j]))

        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return False
    finally:
        conn.close()


def get_team_ids(match_id):
    """Fetch team IDs for a given match ID"""
    conn=connect_db()    
    cursor = conn.cursor()
    
    query = "SELECT team1_id, team2_id FROM matches WHERE match_id = %s"
    cursor.execute(query, (match_id,))
    result = cursor.fetchone()
    t1_id=result[0]
    t2_id=result[1]
    cursor.close()
    conn.close()
    return t1_id,t2_id if result else (None, None)

def get_player_count(team_id):
    """Fetch the number of players for a given team ID"""
    conn=connect_db()    
    cursor = conn.cursor()
    
    query = "SELECT COUNT(*) FROM players WHERE team_id = %s"
    cursor.execute(query, (team_id,))
    count = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    return count