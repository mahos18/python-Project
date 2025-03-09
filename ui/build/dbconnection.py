import mysql.connector

def connect_db():
    """Connect to MySQL database on WAMP server"""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",      # Default user in WAMP
            password="",      # Default password (empty in WAMP)
            database="cricket-league-management"
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Database Connection Error: {e}")
        return None

def check_adminlogin(username, password):
    """Check if username and password exist in the database"""
    conn = connect_db()
    if conn is None:
        return False  # DB connection failed

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE admin_username=%s AND password_hash=%s", (username, password))
        result = cursor.fetchone()
        conn.close()
        return result is not None  # Return True if user exists, else False

    except mysql.connector.Error as e:
        print(f"Database Query Error: {e}")
        return False

def check_login(username, password):
    """Check if username and password exist in the database"""
    conn = connect_db()
    if conn is None:
        return False  # DB connection failed

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password_hash=%s", (username, password))
        result = cursor.fetchone()
        conn.close()
        return result is not None  # Return True if user exists, else False

    except mysql.connector.Error as e:
        print(f"Database Query Error: {e}")
        return False



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


def get_user_role(username, password):
    try:
        conn= connect_db()
        cursor = conn.cursor()

        query = "SELECT role FROM users WHERE username = %s AND password_hash = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result:
            return result[0]  # Return the role (e.g., 'admin' or 'player')
        else:
            return None  # No matching user found
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return None