import mysql.connector

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",    # Change if using a different host
            user="root",         # Your MySQL username
            password="",         # Your MySQL password
            database="cricket-league-management"  # Your database name
        )
        return conn
    except mysql.connector.Error as e:
        print("Error connecting to database:", e)
        return None

def get_player_details(user_id):
    conn = get_db_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT p.player_name, p.role, t.team_name, p.runs, p.wickets,p.matches_played,p.team_id
        FROM players p
        LEFT JOIN teams t ON p.team_id = t.team_id
        WHERE p.user_id = %s
        """
        cursor.execute(query, (user_id,))
        player = cursor.fetchone()
        return player  # Returns a single player's data as a dictionary
    except mysql.connector.Error as e:
        print("Error fetching player details:", e)
        return None
    finally:
        conn.close()

def get_team_id(user_id):
    conn = get_db_connection()
    if not conn:
        return "db error"

    try:
        cursor = conn.cursor()
        query = """
        SELECT team_id from players
        WHERE user_id = %s
        """
        cursor.execute(query, (user_id,))
        teamid = cursor.fetchone()
        return teamid 
    except mysql.connector.Error as e:
        print("Error fetching player details:", e)
        return "error"
    finally:
        conn.close()


def get_standings():
    conn = get_db_connection()
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

def get_upcoming_matches(team_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT m.match_date, t1.team_name AS team1_name, t2.team_name AS team2_name,m.status
        FROM matches m
        JOIN teams t1 ON m.team1_id = t1.team_id
        JOIN teams t2 ON m.team2_id = t2.team_id
        WHERE (m.team1_id = %s OR m.team2_id = %s) 
        AND m.match_date >= CURDATE()
        ORDER BY m.match_date ASC
    """
    cursor.execute(query, (team_id,team_id))
    matches = cursor.fetchall()

    conn.close()
    return matches