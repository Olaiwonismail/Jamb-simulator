
from flask_wtf import FlaskForm
from wtforms.validators import Length,DataRequired
from wtforms import SelectMultipleField, widgets, ValidationError, RadioField, SubmitField

SUBJECTS = [
    # "English Language",
    "Mathematics", "Biology", "Physics", "Chemistry",
    "Agricultural Science", "Home Economics", "Literature-in-English",
    "Government", "Christian Religious Studies (CRS)", "Islamic Religious Studies (IRS)",
    "Economics", "Principle of Account", "Commerce", "Geography", "Music",
    "Hausa", "Igbo", "Yoruba", "French", "Arabic", "Art", "History"
]

class SubjectForm(FlaskForm):
    subjects = SelectMultipleField(
        "Select up to 4 subjects:",
        choices=[(subject, subject) for subject in SUBJECTS],
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False),
        validators=[Length(max=4, message="You can select a maximum of 4 subjects.")],
        default=["English Language"]  # Pre-select English Language
        )
    # Custom Validator for Maximum Selection
    def validate_subjects(self, field):
        if len(field.data) > 4:
            raise ValidationError("You can select a maximum of 4 subjects.")
        if len(field.data) < 3:
            raise ValidationError("You have to select at least 3 more subjects")

class QuestionForm(FlaskForm):
    answer = RadioField(
        'Answer',
        choices=[
            ('A'),
            ('B'),
            ('C'),
            ('D')
        ]
    )
    submit = SubmitField('Submit')
