import mysql.connector
from mysql.connector import Error

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

def get_players():
    """Fetch all players without teams."""
    connection = connect_db()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT player_name, role FROM players WHERE team_id IS NULL")
        players = cursor.fetchall()
        return players
    except Error as e:
        print(f"Error fetching players: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

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