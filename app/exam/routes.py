from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint,session,jsonify)
# from flask_login import current_user, login_required
from app import db
from app.models import Question,Score,ScoreDetail
from app.exam.forms import SubjectForm,QuestionForm
from flask_session import Session
from sqlalchemy.sql.expression import func
import time
from datetime import datetime,timedelta
from flask_login import  login_required,current_user
exam = Blueprint('exam',__name__)

@exam.route('/')
def home():

    return render_template('home.html')

#  Route for the about page
@exam.route('/select_subject',methods = ['GET','POST'])
@login_required
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
@login_required

def start_exam(list):
    preserved_data = {'_user_id': session.get('_user_id'), '_fresh': session.get('_fresh')}
    session.clear()
    session.update(preserved_data)
    # if not session.get('subjects'):
    #     return redirect(url_for('exam.select_subject'))
    session['subjects'] = list
    list = list.split(',')
    questions_1 = Question.query.filter_by(subject= list[1]).order_by(func.random()).limit(41).all()
    questions_2 = Question.query.filter_by(subject= list[2]).order_by(func.random()).limit(41).all()
    questions_3 = Question.query.filter_by(subject= list[3]).order_by(func.random()).limit(41).all()
    eng_questions = Question.query.filter_by(subject= 'English').order_by(func.random()).limit(61).all()
    # print(Question.query.filter_by(subject= 'English').order_by(func.random()).limit(41).all())

    # questions = questions.limit(41)
    question_list = [questions_1,questions_2,questions_3,eng_questions]
    print(question_list)
    for item in question_list:
        if len(item)==0:
            flash("""Please not some subjects are not availabe.
               Kindly select from these subjects:
             Physics, Government, Chemistry and Biology
             """)
            return redirect(url_for('exam.select_subject'))

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




@exam.route('/my_exam', methods=['GET', 'POST'])
@login_required

def my_exam():
    session['exam_in_progress'] = True
    subject = request.args.get('subject', 'English Language')
    if session.get(subject):
        list = session.get('subjects')
        list = list.split(',')
    else:
        return redirect(url_for('exam.select_subject'))
    page = int(request.args.get('page', 1))

    questions = session[subject][page][0]
    all_questions = session[subject]
    answer = session[subject][page][1]
    form = QuestionForm()
    form.answer.choices = [
        ('A', ' ' + questions.option_a),
        ('B', ' ' + questions.option_b),
        ('C', ' ' + questions.option_c),
        ('D', ' ' + questions.option_d)
    ]

    if request.method == 'GET':
        if session[subject][page][1]:
            form.answer.data = session[subject][page][1]
    if request.form.get('answer'):
        selected_answer = request.form.get('answer')  # Retrieve selected answer
        session[subject][page][1] = selected_answer
    num = len(session[subject])
    print(session['exam_in_progress'])
    if 'end_time' not in session:
        session['end_time'] = (datetime.now()+timedelta(hours=2)).isoformat()
    return render_template(
        'exam.html',
        end_time = session['end_time'],
        questions=questions,
        all_questions=all_questions,
        subject=subject,
        form=form,
        list=list,
        num=num,
        page=page
    )

# @exam.route('/submit/',methods = ['GET','POST'])
# def submit():
#     session['exam_in_progress'] = False
#     list = session.get('subjects')
#     list = list.split(',')
#     subject1_score=0
#     subject2_score=0
#     subject3_score=0
#     subject4_score=0
#     subject1 = session.get(list[0])
#     subject2 = session.get(list[1])
#     subject3 = session.get(list[2])
#     subject4 = session.get(list[3])
#     for item in subject1:
#         if item[1]:
#             if item[0].correct_option == item[1] :
#                 subject1_score+=1
#     for item in subject2:
#         if item[1]:
#             if item[0].correct_option == item[1] :
#                 subject2_score+=1
#     for item in subject3:
#         if item[1]:
#             if item[0].correct_option == item[1] :
#                 subject3_score+=1
#     for item in subject4:
#         if item[1]:
#             if item[0].correct_option == item[1] :
#                 subject4_score+=1
#     session.clear()
#     return f'{subject4_score,subject2_score,subject1_score,subject3_score} {subject4_score+subject2_score+subject1_score+subject3_score}'

@exam.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    if 'subjects' not in session:
        flash('No exam data found. Please take the exam first.')
        return redirect(url_for('exam.select_subject'))

    # Mark the exam as completed
    session['exam_in_progress'] = False
    subjects = session['subjects'].split(',')
    total_score = 0
    score_data = {}

    for subject in subjects:
        if subject in session:
            questions = session[subject]
            correct_answers = 0
            score_details = []  # List to hold details for ScoreDetail

            # Evaluate user's answers
            for question, user_answer in questions:
                if user_answer and question.correct_option == user_answer:
                    correct_answers += 1

                # Save each question's details
                score_details.append(ScoreDetail(

                    question_text=question.question_text,
                    user_answer=user_answer,
                    correct_answer=question.correct_option
                ))

            # Calculate and store scores for the subject
            total_questions = len(questions)
            percentage = (correct_answers / total_questions) * 100 if total_questions else 0
            score_data[subject] = {
                'correct': correct_answers,
                'total': total_questions,
                'percentage': percentage
            }
            total_score += correct_answers

            # Save the subject's score and details to the database
            score = Score(
            user_id=current_user.id,
                subject=subject,
                correct_answers=correct_answers,
                total_questions=total_questions,
                percentage=percentage,
                date_taken=datetime.utcnow(),
                details=score_details
            )
            db.session.add(score)

    # Commit all the scores and details to the database
    db.session.commit()

    # Render the score page
    return render_template(
        'score.html',
        score_data=score_data,
        total_score=total_score,
        total_subjects=len(subjects)
    )

from math import ceil
from flask import render_template
from flask_login import login_required, current_user
from app.models import Score

@exam.route('/score_history')
@login_required
def score_history():
    # Query all scores for the logged-in user
    user_scores = Score.query.filter_by(user_id=current_user.id).order_by(Score.date_taken.desc()).all()

    # Group scores into lists of 4
    grouped_scores = [user_scores[i:i + 4] for i in range(0, len(user_scores), 4)]

    # Calculate totals for each group
    grouped_totals = []
    for group in grouped_scores:
        total_correct = sum(score.correct_answers for score in group)
        total_questions = sum(score.total_questions for score in group)
        grouped_totals.append({
            "scores": group,
            "total_correct": total_correct,
            "total_questions": total_questions,
            "percentage": (total_correct / total_questions * 100) if total_questions > 0 else 0,
        })

    return render_template('score_history.html', grouped_totals=grouped_totals)
