from datetime import datetime
from flask import current_app, url_for
from flask_login import UserMixin
from app import db, login_manager


# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# User Model
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False)  # Changed to db.Text
    email = db.Column(db.Text, nullable=False)  # Changed to db.Text
    password = db.Column(db.Text, nullable=False)  # Changed to db.String(64)
    performance = db.relationship('Score', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"


# Question Model
class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.Text, nullable=False)  # Changed to db.Text
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.Text, nullable=False)
    option_b = db.Column(db.Text, nullable=False)
    option_c = db.Column(db.Text, nullable=False)
    option_d = db.Column(db.Text, nullable=False)
    correct_option = db.Column(db.Text, nullable=False)  # Changed to db.Text

    def __repr__(self):
        return f"<Question {self.subject}: {self.question_text[:30]}...>"


# Score Model
class Score(db.Model):
    __tablename__ = 'scores'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.Text, nullable=False)  # Changed to db.Text
    correct_answers = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    date_taken = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.relationship('ScoreDetail', back_populates='score', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Score {self.subject} by User ID {self.user_id}: {self.percentage}%>"


# ScoreDetail Model
class ScoreDetail(db.Model):
    __tablename__ = 'score_details'
    id = db.Column(db.Integer, primary_key=True)
    score_id = db.Column(db.Integer, db.ForeignKey('scores.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    user_answer = db.Column(db.Text, nullable=True)  # Changed to db.Text
    correct_answer = db.Column(db.Text, nullable=False)  # Changed to db.Text
    score = db.relationship('Score', back_populates='details')
