import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class DataBase():
    def __init__(self):
        self.mysqlConnection = None
        self.cursor = None
        
    
    def __enter__(self):
        self.mysqlConnection = mysql.connector.connect(
            host="localhost", #port 3306
            user="root",
            password=os.getenv("DB_PASSWORD"),
            database="event_hub_db"
        )
        try:
            self.cursor = self.mysqlConnection.cursor(buffered=True)
            self.ensure_users_table_exists()
            self.ensure_events_table_exists()
            self.ensure_attendees_table_exists()
            return self
        except mysql.connector.Error as error:
            print(f"Error while connecting to MySQL: {error}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.mysqlConnection:
            if exc_type is None:
                self.mysqlConnection.commit()
            else:
                self.mysqlConnection.rollback()
            self.mysqlConnection.close()


    def ensure_users_table_exists(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL
            );
        """)

    def ensure_events_table_exists(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                name VARCHAR(255) NOT NULL,
                date DATE NOT NULL,
                location VARCHAR(255) NOT NULL,
                description TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)
    
    def ensure_attendees_table_exists(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendees (
                id INT AUTO_INCREMENT PRIMARY KEY,
                event_id INT NOT NULL,
                user_id INT NOT NULL,
                FOREIGN KEY (event_id) REFERENCES events(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)


    # User
    def create_user(self, name, email, password_hash):
        self.cursor.execute("SELECT * FROM users WHERE email = %s;", (email,))
        existing_user = self.cursor.fetchone()
        if existing_user:
            return False
        self.cursor.execute("INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)", (name, email, password_hash))
        self.mysqlConnection.commit()
        return True

    def load_user(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        return self.cursor.fetchone()
    

    def load_user_by_email(self, email):
        self.cursor.execute("SELECT * FROM users WHERE email = %s;", (email,))
        return self.cursor.fetchone()
    
    def update_user(self, user_id, name, email, password_hash=None):
        if password_hash:
            self.cursor.execute(
                "UPDATE users SET name = %s, email = %s, password_hash = %s WHERE id = %s",
                (name, email, password_hash, user_id)
            )
        else:
            self.cursor.execute(
                "UPDATE users SET name = %s, email = %s WHERE id = %s",
                (name, email, user_id)
            )
        self.mysqlConnection.commit()
                
    def delete_user(self, user_id):
        self.cursor.execute("DELETE FROM attendees WHERE user_id = %s", (user_id,))

        self.cursor.execute("DELETE FROM events WHERE user_id = %s", (user_id,))

        self.cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        self.mysqlConnection.commit()
        
        
    def get_user_attended_events(self, user_id):
        self.cursor.execute("""
            SELECT events.* FROM events
            JOIN attendees ON events.id = attendees.event_id
            WHERE attendees.user_id = %s
            ORDER BY events.date ASC
        """, (user_id,))
        return self.cursor.fetchall()
    
    def get_user_created_events(self, user_id):
        self.cursor.execute("""
            SELECT * FROM events
            WHERE user_id = %s
        """, (user_id,))
        return self.cursor.fetchall()


    #event
    def create_event(self, user_id, name, date, location, description):
        self.cursor.execute("INSERT INTO events (user_id, name, date, location, description) VALUES (%s, %s, %s, %s, %s)", (user_id, name, date, location, description))
        self.mysqlConnection.commit()
        self.add_attendee(self.cursor.lastrowid, user_id)

    
    def delete_event(self, event_id):
        self.cursor.execute("DELETE FROM attendees WHERE event_id = %s", (event_id,))
        
        self.cursor.execute("DELETE FROM events WHERE id = %s", (event_id,))
        self.mysqlConnection.commit()
    
    def update_event(self, event_id, name, date, location, description):
        self.cursor.execute("UPDATE events SET name = %s, date = %s, location = %s, description = %s WHERE id = %s", (name, date, location, description, event_id))
        self.mysqlConnection.commit()

    
    def get_all_events(self):
        self.cursor.execute("SELECT * FROM events WHERE date >= CURDATE() ORDER BY date ASC")
        return self.cursor.fetchall()
    
    def get_event(self, event_id):
        self.cursor.execute("SELECT id, user_id, name, date, location, description FROM events WHERE id = %s", (event_id,))
        return self.cursor.fetchone()
    
    #attendees
    def add_attendee(self, event_id, user_id):
        self.cursor.execute("INSERT INTO attendees (event_id, user_id) VALUES (%s, %s)", (event_id, user_id))
        self.mysqlConnection.commit()
    
    def remove_attendee(self, event_id, user_id):
        self.cursor.execute("DELETE FROM attendees WHERE event_id = %s AND user_id = %s", (event_id, user_id))
        self.mysqlConnection.commit()
        
    
    def get_attendees(self, event_id):
        self.cursor.execute("SELECT user_id FROM attendees WHERE event_id = %s", (event_id,))
        return [user[0] for user in self.cursor.fetchall()]
    
    def get_event_attendee_count(self, event_id):
        self.cursor.execute("SELECT COUNT(*) FROM attendees WHERE event_id = %s", (event_id,))
        return self.cursor.fetchone()[0]
    
    def is_user_attending_event(self, event_id, user_id):
        self.cursor.execute("SELECT * FROM attendees WHERE event_id = %s AND user_id = %s", (event_id, user_id))
        return self.cursor.fetchone() is not None