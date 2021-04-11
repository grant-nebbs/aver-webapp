from datetime import datetime

import requests
from django.http import HttpResponse
from django.shortcuts import render
import json
from .models import User
from django.utils.timezone import make_aware

users = []
num_of_questions_answered = []
total_num_users = []
total_num_questions = []


def home(request):
    response = requests.get('https://api.stackexchange.com/2.2/users?fromdate=1615420800&order=asc&sort=reputation'
                            '&site=stackoverflow&pagesize=100&page=1')
    data = response.json()
    page_num = 1
    while 'has_more' in data and data['has_more']:
        response = requests.get('https://api.stackexchange.com/2.2/users?fromdate=1615420800&order=asc&sort=reputation'
                                '&site=stackoverflow&pagesize=100&page=' + str(page_num))
        questions_answered = 0
        data = response.json()
        values = data.values()
        total_users = 0
        total_questions = 0
        i = 0
        for value in values:
            if type(value) == list:
                for user in value:
                    total_users += 1

            total_num_users.append(total_users)

            if page_num == 1:
                for user in value:
                    user_id = user.get('user_id')
                    name = user.get('display_name')
                    link = user.get('link')
                    date = datetime.fromtimestamp(user.get('creation_date'))
                    aware_date = make_aware(date)
                    new_user = User.objects.create(user_id=user_id, name=name, link=link, created_date=aware_date,
                                                   asked_question=False, multiple_questions=False)
                    users.append(new_user)
                    new_user.save()
                    i += 1
                    if i == 20:
                        break

            break
        page_num += 1
        if page_num == 30:
            break

    q_response = requests.get('https://api.stackexchange.com/questions?fromdate=1615420800&order=asc&sort=activity&site'
                              '=stackoverflow&pagesize=100&page=1')
    q_data = q_response.json()
    q_page_num = 1
    while 'has_more' in q_data and q_data['has_more']:
        q_response = requests.get('https://api.stackexchange.com/questions?fromdate=1615420800&order=asc&sort'
                                  '=activity&site '
                                  '=stackoverflow&pagesize=100&page=' + str(q_page_num))
        q_data = q_response.json()
        values = q_data.values()
        for value in values:
            for question in value:
                total_questions += 1
                for user in users:
                    if user.user_id == question['owner']['user_id']:
                        if user.asked_question:
                            user.multiple_questions = True
                        else:
                            user.asked_question = True

                        if question['is_answered']:
                            questions_answered += 1

            break
        total_num_questions.append(total_questions)
        num_of_questions_answered.append(questions_answered)
        q_page_num += 1
        if q_page_num == 30:
            break

    return render(request, 'StackApp/index.html')


def question1(request):
    answer = 0
    for user in users:
        if user.asked_question:
            answer += 1
    context = {
        'answer': str(answer) + " users have asked a question"
    }
    return render(request, 'StackApp/question.html', context=context)


def question2(request):
    answer = sum(num_of_questions_answered)
    context = {
        'answer': str(answer) + " of the questions have been answered"
    }
    return render(request, 'StackApp/question.html', context=context)


def question3(request):
    answer = 0
    for user in users:
        if user.multiple_questions:
            answer += 1
    context = {
        'answer': str(answer) + " users have asked multiple questions"
    }
    return render(request, 'StackApp/question.html', context=context)


def question4(request):
    answer = sum(total_num_users)
    context = {
        'answer': str(answer) + " users have joined in the last month"
    }
    return render(request, 'StackApp/question.html', context=context)


def question5(request):
    answer = sum(total_num_questions)
    context = {
        'answer': str(answer) + " questions have been asked in the last month"
    }
    return render(request, 'StackApp/question.html', context=context)
