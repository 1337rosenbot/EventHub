from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_required
from routes.user_manager import users_bp, login_manager
from routes.event_manager import events_bp
from models.database import DataBase

import secrets


app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)
login_manager.init_app(app)

app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(events_bp, url_prefix='/events')


@app.route("/")
def home():
    with DataBase() as db:
        events = db.get_all_events()
    return render_template('index.html', events=events)



if __name__ == '__main__':
    app.run(debug=True)