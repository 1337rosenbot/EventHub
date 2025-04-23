from flask import render_template, redirect, url_for, request, Blueprint
from flask_login import login_required, current_user
from models.database import DataBase
from models.event import Event
from models.forms import CreateEventForm


events_bp = Blueprint('events', __name__)

@events_bp.route('/events')
def get_all_events():
    with DataBase() as db:
        events = [Event(*event) for event in db.get_all_events()]

    return render_template('events/all_events.html', events = events)


@events_bp.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = CreateEventForm()
    if form.validate_on_submit():
        with DataBase() as db:
            db.create_event(
                current_user.id,
                form.event_name.data,
                form.event_date.data,
                form.event_location.data,
                form.event_description.data
            )
        return redirect(url_for('users.profile'))
    return render_template('events/create_event.html', form=form)


@events_bp.route('/event/<int:event_id>', methods=['GET', 'POST'])
def event_details(event_id):
    with DataBase() as db:
        event = db.get_event(event_id)
    
    if request.method == 'POST':
        if 'attend' in request.form:
            with DataBase() as db:
                db.add_attendee(event_id, current_user.id)
            return redirect(url_for('events.event_details', event_id=event_id))
        
        elif 'cancel' in request.form:
            with DataBase as db:
                db.remove_attendee(event_id, current_user.id)
            return redirect(url_for('events.event_details', event_id=event_id))
    
    return render_template('events/event_details.html', event=event)


@events_bp.route('/delete_event/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    with DataBase() as db:
        db.delete_event(event_id)
    
    return redirect(url_for('users.profile'))


@events_bp.route('/update_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def update_event(event_id):
    with DataBase() as db:
        event = db.get_event(event_id)
    form = CreateEventForm()
    if request.method == 'POST' and form.validate_on_submit():
        with DataBase() as db:
            db.update_event(
                event_id,
                form.event_name.data,
                form.event_date.data,
                form.event_location.data,
                form.event_description.data
            )
        return redirect(url_for('users.profile'))

    if request.method == 'GET':
        form.event_name.data = event[2]
        form.event_date.data = event[3]
        form.event_location.data = event[4]
        form.event_description.data = event[5]
    return render_template('events/update_event.html', form=form, event=event)

@events_bp.route('/event_signup/<int:event_id>', methods=['POST'])
@login_required
def event_signup(event_id):
    error = None
    success = None
    with DataBase() as db:
        event = db.get_event(event_id)
        if db.is_user_attending_event(event_id, current_user.id):
            error = "You are already attending this event."
        else:
            db.add_attendee(event_id, current_user.id)
            success = "You are now attending this event."
    return render_template('events/event_details.html', event=event, error=error, success=success)

@events_bp.route('/unsignup/<int:event_id>', methods=['GET', 'POST'])
@login_required
def event_unsignup(event_id):
    if request.method == 'POST':
        with DataBase() as db:
            db.remove_attendee(event_id, current_user.id)
        return redirect(url_for('users.profile'))
    
    return render_template('events/events_unsignup.html')