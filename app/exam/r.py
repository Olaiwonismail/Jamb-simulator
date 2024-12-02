from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint,session)
from flask_login import current_user, login_required
from app import db
from app.models import Question
from app.exam.forms import SubjectForm,QuestionForm
from flask_session import Session
from sqlalchemy.sql.expression import func
exam = Blueprint('exam',__name__)

@exam.route('/')
def home():

    return render_template('home.html')

#  Route for the about page
@exam.route('/select_subject',methods = ['GET','POST'])
def select_subject():
    form = SubjectForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            selected_subjects = form.subjects.data  # This is where you access the selected items
            selected_subjects[:0] = ["English Language"]
            return redirect(url_for('exam.start_exam',list = ','.join(selected_subjects)))
        else:
            flash('Select up to 3 more subjects')
    return render_template('select_subject.html',form=form)

@exam.route('/start_exam/<list>',methods = ['GET','POST'])
def start_exam(list):

    session['subjects'] = list
    list = list.split(',')
    questions_1 = Question.query.filter_by(subject= list[1]).order_by(func.random()).limit(41).all()
    questions_2 = Question.query.filter_by(subject= list[2]).order_by(func.random()).limit(41).all()
    questions_3 = Question.query.filter_by(subject= list[3]).order_by(func.random()).limit(41).all()
    eng_questions = Question.query.filter_by(subject= 'English').order_by(func.random()).limit(41).all()
    # print(Question.query.filter_by(subject= 'English').order_by(func.random()).limit(41).all())

    # questions = questions.limit(41)

    answer = None
    # questions = [eng_questions,questions_1,questions_2,questions_3]
    empty_list1 = []
    empty_list2 = []
    empty_list3 = []
    empty_list4 = []
    for question in eng_questions:

        empty_list1.append([question,answer])
    for question in questions_1:
        empty_list2.append([question,answer])
    for question in questions_2:
        empty_list3.append([question,answer])
    for question in questions_3:
        empty_list4.append([question,answer])
    # questions = empty_list
    session[list[0]] = empty_list1
    session[list[1]] = empty_list2
    session[list[2]] = empty_list3
    session[list[3]] = empty_list4
    print(list[0])
    # print('hi',session['question'] )
    return render_template('start_exam.html',list=list)

from datetime import datetime, timedelta


@exam.route('/my_exam',methods = ['GET','POST'])
def my_exam():
    subject = request.args.get('subject','English Language')
    if session.get(subject):
        list = session.get('subjects')
        list = list.split(',')
    else:
        return redirect(url_for('exam.select_subject'))
    page = int(request.args.get('page',1))

    questions = session[subject][page][0]
    all_questions = session[subject]
    answer = session[subject][page][1]
    form = QuestionForm()
    form.answer.choices = [
    ('A', ' ' +questions.option_a),
    ('B', ' ' +questions.option_b),
    ('C', ' ' +questions.option_c),
    ('D', ' ' +questions.option_d)
    ]

    if request.method == 'GET':
        if session[subject][page][1]:
            form.answer.data = session[subject][page][1]
    if request.form.get('answer'):
        selected_answer = request.form.get('answer')  # Retrieve selected answer
        print(selected_answer)
        session[subject][page][1] = selected_answer
    num = 41
    if "start_time" not in session:
        session["start_time"] = (datetime.now() + timedelta(hours=2)).isoformat()

    # Calculate remaining time
    end_time = datetime.fromisoformat(session["start_time"])
    remaining_time = max((end_time - datetime.now()).seconds, 0)  # Ensure non-negative



    return render_template('exam.html', remaining_time=remaining_time,questions = questions,all_questions=all_questions,subject=subject, form=form,list = list,num= num,page=page)
