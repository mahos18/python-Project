import mysql.connector

# Establish database connection
def get_db_connection():
    return mysql.connector.connect(
         host="localhost",
        user="root",
        password="",
        database="cricket-league-management"
)

# Get team IDs from match ID
def get_team_ids(match_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT team1_id, team2_id FROM matches WHERE match_id = %s"
    cursor.execute(query, (match_id,))
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return result if result else (None, None)

# Get player IDs of a team
def get_team_players(team_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT player_id FROM players WHERE team_id = %s"
    cursor.execute(query, (team_id,))
    players = [row[0] for row in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    
    return players
