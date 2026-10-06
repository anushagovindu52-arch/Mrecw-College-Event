
import sqlite3

DB_NAME = "mrecw_events.db"


# Connect to database
def get_connection():
    return sqlite3.connect(DB_NAME)


# Create tables
def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # ---------------- REGISTRATIONS TABLE ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_number TEXT UNIQUE NOT NULL,
            branch TEXT NOT NULL,
            year TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            team_name TEXT NOT NULL,
            skills TEXT,
            project_idea TEXT
        )
    """)

    # ---------------- LEADERBOARD TABLE ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team TEXT NOT NULL,
            project TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    """)

    # ---------------- EVENTS TABLE ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            event_date TEXT NOT NULL,
            venue TEXT,
            team_size TEXT,
            prize TEXT,
            rules TEXT
        )
    """)

    conn.commit()
    conn.close()


# ==========================================================
# REGISTRATION
# ==========================================================

def add_registration(
    name,
    roll_number,
    branch,
    year,
    email,
    team_name,
    skills,
    project_idea
):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # Add student registration
        cursor.execute("""
            INSERT INTO registrations
            (name, roll_number, branch, year, email,
             team_name, skills, project_idea)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            roll_number,
            branch,
            year,
            email,
            team_name,
            skills,
            project_idea
        ))

        # Check whether team already exists
        cursor.execute("""
            SELECT id
            FROM leaderboard
            WHERE team = ?
        """, (team_name,))

        existing_team = cursor.fetchone()

        # Add team to leaderboard
        if existing_team is None:

            cursor.execute("""
                INSERT INTO leaderboard
                (team, project, score)
                VALUES (?, ?, ?)
            """, (
                team_name,
                project_idea if project_idea
                else "Project not submitted",
                0
            ))

        conn.commit()

        return True, "Registration successful!"

    except sqlite3.IntegrityError:

        return False, "Roll number or email already registered."

    finally:

        conn.close()


# Get all registrations
def get_registrations():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM registrations
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data


# ==========================================================
# LEADERBOARD
# ==========================================================

# Add leaderboard team
def add_team(team, project, score):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO leaderboard
        (team, project, score)
        VALUES (?, ?, ?)
    """, (
        team,
        project,
        score
    ))

    conn.commit()
    conn.close()


# Get leaderboard
def get_leaderboard():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            team,
            project,
            score
        FROM leaderboard
        ORDER BY score DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data


# ==========================================================
# EVENTS
# ==========================================================

# Add Hackathon / Workshop / Other Event
def add_event(
    event_type,
    name,
    description,
    event_date,
    venue,
    team_size,
    prize,
    rules
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO events
        (event_type, name, description, event_date, venue,
         team_size, prize, rules)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        event_type,
        name,
        description,
        event_date,
        venue,
        team_size,
        prize,
        rules
    ))

    conn.commit()
    conn.close()


# Get all events
def get_events():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            event_type,
            name,
            description,
            event_date,
            venue,
            team_size,
            prize,
            rules
        FROM events
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data
