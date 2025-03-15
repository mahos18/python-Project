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
                ORDER BY p.runs DESC 
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
        JOIN teams t ON p.team_id = t.team_id
        WHERE p.player_name LIKE %s OR t.team_name LIKE %s OR p.player_id LIKE %s
    """
    
    search_pattern = f"%{search}%"  # Add wildcards for partial match
    cursor.execute(query, (search_pattern, search_pattern,search_pattern))
    players = cursor.fetchall()
    conn.close()
    return players

# 2. Add a new player
def add_player(player_name,role):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        query = "INSERT INTO players (player_name, role) VALUES (%s, %s)"
        cursor.execute(query, (player_name, role))
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print(f"Error fetching players: {e}")
        return False
    

# 3. Update player details
def update_player(player_id, player_name, age, role, team_id):
    conn = connect_db()
    cursor = conn.cursor()
    query = "UPDATE players SET player_name=%s, age=%s, role=%s, team_id=%s WHERE player_id=%s"
    cursor.execute(query, (player_name, age, role, team_id, player_id))
    
    conn.commit()
    conn.close()

# 4. Delete a player
def delete_player(player_id):
    conn = connect_db()
    cursor = conn.cursor()
    query = "DELETE FROM players WHERE player_id=%s"
    cursor.execute(query, (player_id,))
    conn.commit()
    conn.close()

# 5. Get player details by ID
def get_player_by_id(player_id):
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT player_id, player_name, age, role, team_id FROM players WHERE player_id=%s"
    cursor.execute(query, (player_id,))
    player = cursor.fetchone()
    conn.close()
    return player
