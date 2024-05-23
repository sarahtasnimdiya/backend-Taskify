from config import db
from datetime import datetime

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False, nullable=False)
    notes = db.Column(db.String(100), unique=False, nullable=True)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    done = db.Column(db.Boolean, default=False, nullable=False)

    def to_jason(self):
        return {
            'id': self.id,
            'title': self.title,
            'notes': self.notes,
            'time': self.time.isoformat(),
            'done': self.done
        }

    