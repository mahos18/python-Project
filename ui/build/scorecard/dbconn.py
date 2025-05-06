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
    try:
        cursor.execute(query, (match_id,))
        result = cursor.fetchone()
        team1id=result[0]
        team2id=result[1]
        return team1id,team2id if result else None, None
    except Exception as e:
        print("Database Error:", e)
        return None
    finally:
        cursor.close()
        conn.close()
    

def get_team1_name(match_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT team_name FROM teams WHERE team_id= (SELECT team1_id FROM matches WHERE match_id = %s)"
    cursor.execute(query, (match_id,))
    result = cursor.fetchone()
    teamname=result[0]
    cursor.close()
    conn.close()
    
    return teamname if result else (None, None)

def get_team2_name(match_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT team_name FROM teams WHERE team_id= (SELECT team2_id FROM matches WHERE match_id = %s)"
    cursor.execute(query, (match_id,))
    result = cursor.fetchone()
    teamname=result[0]

    cursor.close()
    conn.close()
    
    return teamname if result else (None, None)


# Get player IDs of a team

def get_team_players(team_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT player_id, player_name FROM players WHERE team_id = %s"
    cursor.execute(query, (team_id,))
    
    players = {row[0]: row[1] for row in cursor.fetchall()}
    
    cursor.close()
    conn.close()
    
    return players

def get_player_id(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT player_id FROM players WHERE player_name= %s"
    cursor.execute(query, (name,))
    
    players =  cursor.fetchall()
    id=players[0]
    cursor.close()
    conn.close()
    
    return id

def init_match_statistics(match_id, batsmen_list, bowlers_list):
    conn = get_db_connection()
    cursor = conn.cursor()

    all_players = list(batsmen_list.keys()) + list(bowlers_list.keys())
    inserted = 0

    for player_id in all_players:
        # Check if the player already exists for the current match_id
        cursor.execute("""
            SELECT COUNT(*) FROM match_statistics
            WHERE match_id = %s AND player_id = %s
        """, (match_id, player_id))

        count = cursor.fetchone()[0]
        
        if count == 0:  # Player not found in the table
            try:
                cursor.execute("""
                    INSERT INTO match_statistics (match_id, player_id)
                    VALUES (%s, %s)
                """, (match_id, player_id))
                inserted += 1
            except mysql.connector.Error as e:
                print(f"Error inserting player_id {player_id}: {e}")
        else:
            print(f"Player {player_id} already exists in match_statistics.")

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Initialized {inserted} player entries for match_id {match_id}")

#scoreboard update
def increment_runs_scored(match_id, player_id, runs,bowls_faced):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "UPDATE match_statistics SET runs_scored = runs_scored + %s,balls_faced = balls_faced + %s WHERE match_id = %s AND player_id = %s"
        cursor.execute(query, (runs,bowls_faced, match_id, player_id))
        conn.commit()
    except Exception as e:
        print("Error incrementing runs scored:", e)
    finally:
        cursor.close()
        conn.close()
def get_player_id_by_name(name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT player_id FROM players WHERE player_name = %s"
        cursor.execute(query, (name.strip().lower(),))
        result = cursor.fetchone()
        if result:
            return result[0]  # player_id
        else:
            return None
    except Exception as e:
        print("Error fetching player ID:", e)
        return None

# def increment_balls_faced(match_id, player_id):
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         query = "UPDATE match_statistics SET balls_faced = balls_faced + 1 WHERE match_id = %s AND player_id = %s"
#         cursor.execute(query, (match_id, player_id))
#         conn.commit()
#     except Exception as e:
#         print("Error incrementing balls faced:", e)
#     finally:
#         cursor.close()
#         conn.close()

def get_bowler_stats_by_team(match_id, bowling_team_name):
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Get team_id from team name
    cursor.execute("SELECT team_id FROM teams WHERE team_name = %s", (bowling_team_name,))
    team_result = cursor.fetchone()
    if not team_result:
        print("Team not found")
        return {}
    team_id = team_result[0]

    # 2. Get all players in that team
    cursor.execute("SELECT player_id, player_name FROM players WHERE team_id = %s", (team_id,))
    players = cursor.fetchall()  # list of (player_id, player_name)

    bowler_stats = {}

    # 3. For each player, get match stats
    for player_id, name in players:
        cursor.execute("""
            SELECT wickets_taken, overs_bowled, runs_conceded
            FROM match_statistics
            WHERE player_id = %s AND match_id = %s
        """, (player_id, match_id))
        stat = cursor.fetchone()
    
        if stat:
            wickets, overs, runs = stat

            if overs and float(overs) > 0:
                bowler_stats[name] = {
                    "wickets": wickets,
                    "overs": overs,
                    "runs_conceded": runs
                }

    conn.close()
    return bowler_stats



def increment_fours(match_id, player_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "UPDATE match_statistics SET fours = fours + 1 WHERE match_id = %s AND player_id = %s"
        cursor.execute(query, (match_id, player_id))
        conn.commit()
    except Exception as e:
        print("Error incrementing fours:", e)
    finally:
        cursor.close()
        conn.close()


def increment_sixes(match_id, player_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "UPDATE match_statistics SET sixes = sixes + 1 WHERE match_id = %s AND player_id = %s"
        cursor.execute(query, (match_id, player_id))
        conn.commit()
        return True
    except Exception as e:
        print("Error incrementing sixes:", e)
        return False
    finally:
        cursor.close()
        conn.close()


def increment_overs_wickets_taken(wickets,overs_bowled,runs_conceded,match_id, player_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "UPDATE match_statistics SET wickets_taken = wickets_taken + %s,overs_bowled = overs_bowled + %s,runs_conceded = runs_conceded + %s WHERE match_id = %s AND player_id = %s"
        cursor.execute(query, (wickets,overs_bowled,runs_conceded,match_id, player_id))
        conn.commit()
    except Exception as e:
        print("Error incrementing wickets taken:", e)
    finally:
        cursor.close()
        conn.close()


# def increment_overs_bowled(match_id, player_id, over_increment=0.1):
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         query = "UPDATE match_statistics SET overs_bowled = overs_bowled + %s WHERE match_id = %s AND player_id = %s"
#         cursor.execute(query, (over_increment, match_id, player_id))
#         conn.commit()
#     except Exception as e:
#         print("Error incrementing overs bowled:", e)
#     finally:
#         cursor.close()
#         conn.close()


# def increment_runs_conceded(match_id, player_id, runs):
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         query = "UPDATE match_statistics SET runs_conceded = runs_conceded + %s WHERE match_id = %s AND player_id = %s"
#         cursor.execute(query, (runs, match_id, player_id))
#         conn.commit()
#     except Exception as e:
#         print("Error incrementing runs conceded:", e)
#     finally:
#         cursor.close()
#         conn.close()


def increment_catches_taken(match_id, player_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "UPDATE match_statistics SET catches_taken = catches_taken + 1 WHERE match_id = %s AND player_id = %s"
        cursor.execute(query, (match_id, player_id))
        conn.commit()
    except Exception as e:
        print("Error incrementing catches taken:", e)
    finally:
        cursor.close()
        conn.close()


# def increment_stumpings(match_id, player_id):
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         query = "UPDATE match_statistics SET stumpings = stumpings + 1 WHERE match_id = %s AND player_id = %s"
#         cursor.execute(query, (match_id, player_id))
#         conn.commit()
#     except Exception as e:
#         print("Error incrementing stumpings:", e)
#     finally:
#         cursor.close()
#         conn.close()



def complete_match_update(match_id, data1, data2, winning_team_name):
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Update match scores
    cursor.execute("""
        UPDATE matches 
        SET first_ining_score = %s, second_ining_score = %s 
        WHERE match_id = %s
    """, (data1[1], data2[1], match_id))

    # 2. Get team1_id and team2_id from matches
    cursor.execute("SELECT team1_id, team2_id FROM matches WHERE match_id = %s", (match_id,))
    team1_id, team2_id = cursor.fetchone()

    # 3. Get team names from team IDs
    cursor.execute("SELECT team_name FROM teams WHERE team_id = %s", (team1_id,))
    team1_name = cursor.fetchone()[0]

    cursor.execute("SELECT team_name FROM teams WHERE team_id = %s", (team2_id,))
    team2_name = cursor.fetchone()[0]

    # 4. Determine winner and loser
    if team1_name == winning_team_name:
        winner_id, loser_id = team1_id, team2_id
    else:
        winner_id, loser_id = team2_id, team1_id

    # 5. Update standings for both teams
    cursor.execute("""
        UPDATE standings 
        SET matches_played = matches_played + 1, wins = wins + 1, points = points + 2
        WHERE team_id = %s
    """, (winner_id,))

    cursor.execute("""
        UPDATE standings 
        SET matches_played = matches_played + 1, losses = losses + 1
        WHERE team_id = %s
    """, (loser_id,))

    conn.commit()
    print("Match and standings updated successfully.")