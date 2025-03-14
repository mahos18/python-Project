import mysql.connector
import smtplib
import random
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re

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

def get_user_id(username, password):
    try:
        conn= connect_db()
        cursor = conn.cursor()

        query = "SELECT user_id FROM users WHERE username = %s AND password_hash = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result:
            return result[0]  
        else:
            return None  
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return None



verification_codes = {}
def send_verification_email(receiver_email):
   
    verification_code = str(random.randint(100000, 999999))  # Generate 6-digit OTP
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


def verify_email_code(email, code):
    return verification_codes.get(email) == code