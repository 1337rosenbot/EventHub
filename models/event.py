class Event():
    def __init__(self, id, user_id, name, date, location, description):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.description = description
        self.date = date
        self.location = location


def add_attendee(self, user_id):
    self.attendees.append(user_id)
    self.attendee_count += 1

def remove_attendee(self, user_id): 
    if user_id in self.attendees:
        self.attendees.remove(user_id)
        self.attendee_count -= 1
    else:
        raise ValueError("User not found in attendees list.")

def get_attendee_count(self):
    return self.attendee_count

