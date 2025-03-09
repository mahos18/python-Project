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
