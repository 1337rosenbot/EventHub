# EventHub

DTE-2509 - Oblig 5


## Project Description

EventHub is a Flask-based web application for creating, managing, and signing up for events. Users can register, log in, create events, sign up for events, and manage their profiles.

---

## Setup Instructions

### 1. Clone the Repository

```sh
git clone https://github.com/YOUR_GITHUB_USERNAME/EventHub.git
cd EventHub
```

### 2. Create and Activate a Virtual Environment

```sh
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, install these manually:

```sh
pip install flask flask-login flask-wtf mysql-connector-python email_validator
```

### 4. Configure the Database

- Make sure you have MySQL installed and running.
- Create a database for the project (e.g., `event_hub_db`).
- Update your database connection settings in `models/database.py` if needed.

Example MySQL commands:
```sql
CREATE DATABASE event_hub_db;
CREATE USER 'eventhubuser'@'localhost' IDENTIFIED BY 'yourpassword';
GRANT ALL PRIVILEGES ON event_hub_db.* TO 'eventhubuser'@'localhost';
FLUSH PRIVILEGES;
```

### 5. Set Up Authentication and Environment Variables

**For security, database credentials and secret keys are not hardcoded.**  
You must provide them as environment variables. The recommended way for development is to use a `.env` file in the project root:

Example `.env` file:
```
SECRET_KEY=your_flask_secret_key
DB_USER=eventhubuser
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_NAME=event_hub_db
```

- Install `python-dotenv` if not already installed:  
  `pip install python-dotenv`
- The app will automatically load these variables at startup.
- **Never commit your `.env` file to version control!**

**For production:**  
Set these environment variables directly in your server or deployment environment.

---

### 6. Run the Application

```sh
python app.py
```

The app will be available at [http://127.0.0.1:5000/]


- The app uses Flask-WTF for forms and CSRF protection.
- All custom CSS is in `static/main.css`.
- Make sure to set up your MySQL user and database as described above.
- If you encounter any issues, check the terminal for error messages.

---

## Known Limitations & Possible Improvements

- **Event Attendee List:**  
  Currently, events do not display a list of attendees. A future improvement would be to show all users signed up for each event, either on the event details page or in the admin/user profile.

- **Number of Attendees:**  
  The number of attendees for each event is not shown. Adding a counter or badge to each event would make this information visible.

- **Event Editing Restrictions:**  
  Any logged-in user can update or delete events they created, but there is no admin role or advanced permissions.

- **No Email Notifications:**  
  The system does not send confirmation or reminder emails for event signups or changes.

- **No Pagination or Search:**  
  Event lists are not paginated and there is no search/filter functionality.

- **No Profile and Event Pictures or Social Features:**  
  User profiles are basic and do not support profile pictures or social interactions.


---

Feel free to contribute or suggest improvements!

---

## Contact

For questions, contact 1337RosenBot or open an issue on the repository.
