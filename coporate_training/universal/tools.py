from pymongo import MongoClient
import datetime as dt
import pandas as pd

aetna_courses = ['Hadoop - Hadoop for Business Analyst',
                 'Hadoop - Hadoop for Data Engineers - Unix',
                 'Hadoop - Hadoop for Data Engineers - Advanced Hive',
                 'Hadoop - Hadoop for Data Engineers - Advanced Pig',
                 'Advanced Analytics - Python Basic',
                 'Advanced Analytics - Python Packages',
                 'Advanced Analytics - Python Big Data'
                 ]

def connect_course_db():
    client = MongoClient('mongodb://heroku_q6lsp17r:695vf0bga9tl0q8tlo5r6lm4f6@216.230.228.86:61178/heroku_q6lsp17r')
    db = client.heroku_q6lsp17r
    enrollments = db.enrollments
    users = db.users
    courses = db.courses
    return courses, users, enrollments

def connect_assessment_db():
    client_assessment = MongoClient('mongodb://ndsa:NYCDataSci2016@216.230.228.86:61179/exam')
    db_assessment = client_assessment.exam
    examsessions = db_assessment.examsessions
    exams = db_assessment.exams
    return examsessions, exams


def get_course_id(title):
    courses, users, enrollments = connect_course_db()
    return courses.find_one({'title': title})['_id']


def add_requirement():  #### 'student': luke_id need to be removed!!
    '''
    exam: False before taken, True after taken before graded, Actual score after graded
    makeup: False unless exam grade<75, else(True before makeup exam taken,
                                             Score after makeup exam graded)
    certificate: False before sent; True after sent
    '''
    courses, users, enrollments = connect_course_db()
    examsessions, exams = connect_assessment_db()
    day_range = dt.datetime.today() - dt.timedelta(days=2)
    enrollments.update_many(
        {"start": {"$gte": day_range},
         "course": {'$in': map(get_course_id, aetna_courses)},
         "require": {'$exists': False}
         },
        {
            '$set': {'require': {'exam': False, 'makeup': False, 'certificate': False}}
        })


def update_exam_from_enrollment():
    '''
    exam: False before taken, True after taken before graded, Actual score after graded
    certificate: False before sent; True after sent
    '''
    courses, users, enrollments = connect_course_db()
    examsessions, exams = connect_assessment_db()
    day_range = dt.datetime.today() - dt.timedelta(days=20)
    exam_email = map(lambda x: {'exam': x['exam'], 'student': x['email'], 'grades':x['grades']},
                     examsessions.find({"start": {"$gte": day_range}}))
    for item in exam_email:
        exam = item['exam']
        email = item['student']
        grades= item['grades']

        try:
            item['course'] = courses.find_one({'exam': exam})['_id']
        except TypeError:
            item['course'] = 'No course use this exam'

        try:
            item['student'] = users.find_one({'email': email})['_id']
        except:
            item['student'] = 'No registered student has this e-mail'

        if grades:
            enrollments.update_one({
                    'student': item['student'],
                    'course': item['course']
                }, {
                    '$set': {'require.exam': sum(grades)}
                })
        else:
            enrollments.update_one({
                'student': item['student'],
                'course': item['course']
            }, {
                '$set': {'require.exam': True}
            })



def alert_ungraded_exam():
    courses, users, enrollments = connect_course_db()
    examsessions, exams = connect_assessment_db()
    luke_id = users.find_one({'name':'Luke Lin'})['_id']
    find_grader = lambda course: (courses.find_one({'_id': course})['grader'],
                                  courses.find_one({'_id': course})['title'])
    ungraded_exam = map(lambda x: x['course'],
                        enrollments.find({'require.exam': True, 'student':{'$ne':luke_id}}))
    summary = pd.DataFrame(map(find_grader, ungraded_exam), columns=['grader', 'course'])
    summary['count'] = 1
    return summary.groupby(['grader', 'course']).count()


#if __name__ == '__main__':
 #   update_exam_from_enrollment()
  #  print alert_ungraded_exam()
