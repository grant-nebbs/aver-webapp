from datetime import datetime

import requests
from django.http import HttpResponse
from django.shortcuts import render
import json
from .models import User
from django.utils.timezone import make_aware

# Initial variables to keep track of information
users = []
num_of_questions_answered = []
total_num_users = []
total_num_questions = []


# Home view that runs api calls
def home(request):
    # Initial call to test response
    response = requests.get('https://api.stackexchange.com/2.2/users?fromdate=1615420800&order=asc&sort=reputation'
                            '&site=stackoverflow&pagesize=100&page=1')
    data = response.json()
    page_num = 1

    # Iteration through pages of user information
    while 'has_more' in data and data['has_more']:
        # API call and data processing
        response = requests.get('https://api.stackexchange.com/2.2/users?fromdate=1615420800&order=asc&sort=reputation'
                                '&site=stackoverflow&pagesize=100&page=' + str(page_num))
        data = response.json()
        values = data.values()
        total_users = 0

        i = 0
        for value in values:
            if type(value) == list:
                # Find total number of users on page
                for user in value:
                    total_users += 1

            # Adds users on page to running total
            total_num_users.append(total_users)

            if page_num == 1 and type(value) == list:
                # Processes users according to data model
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
        # Reads only the first 30 pages in order to not overload api servers, can be adjusted
        if page_num == 30:
            break

    # Initial call to test response
    q_response = requests.get('https://api.stackexchange.com/2.2/questions?order=desc&sort=activity&site'
                              '=stackoverflow&pagesize=100&page=1')
    q_data = q_response.json()
    q_page_num = 1
    # Iteration through pages of question information
    while 'has_more' in q_data and q_data['has_more']:
        q_response = requests.get('https://api.stackexchange.com/2.2/questions?order=desc&sort=activity&site'
                                  '=stackoverflow&pagesize=100&page=' + str(q_page_num))
        q_data = q_response.json()
        values = q_data.values()
        total_questions = 0
        questions_answered = 0
        for value in values:
            if type(value) == list:
                for question in value:
                    # Tracks total number of questions on API page
                    total_questions += 1
                    for user in users:
                        # Checks if question has been asked by users from earlier API call
                        if 'user_id' in question['owner'] and user.user_id == question['owner']['user_id']:
                            # Mark if user has asked a question or multiple questions
                            if user.asked_question:
                                user.multiple_questions = True
                            else:
                                user.asked_question = True

                            # Check if question has been answered and add to a tally
                            if question['is_answered']:
                                questions_answered += 1

            total_num_questions.append(total_questions)
            num_of_questions_answered.append(questions_answered)

            break

        q_page_num += 1
        # Reads only the first 30 pages in order to not overload api servers
        if q_page_num == 30:
            break

    # Renders a home page based on an index file
    return render(request, 'StackApp/index.html')


# View for the answer for the first question
def question1(request):
    # Process for summing up num of users who have asked a question and rendering it in view
    answer = 0
    for user in users:
        if user.asked_question:
            answer += 1
    context = {
        'answer': str(answer) + " users have asked a question"
    }
    return render(request, 'StackApp/question.html', context=context)


# View for the answer for the second question
def question2(request):
    # Processes number of questions answered from selected users
    answer = sum(num_of_questions_answered)
    context = {
        'answer': str(answer) + " of the questions have been answered"
    }
    return render(request, 'StackApp/question.html', context=context)


# View for the answer for the third question
def question3(request):
    # Processes number of users who have asked multiple questions
    answer = 0
    for user in users:
        if user.multiple_questions:
            answer += 1
    context = {
        'answer': str(answer) + " users have asked multiple questions"
    }
    return render(request, 'StackApp/question.html', context=context)


# View for the answer for the fourth question
def question4(request):
    # Processes users who joined in last month
    answer = sum(total_num_users)
    context = {
        'answer': str(answer) + " users have joined in the last month"
    }
    return render(request, 'StackApp/question.html', context=context)


# View for the answer for the five question
def question5(request):
    # Processes questions asked in last month
    answer = sum(total_num_questions)
    context = {
        'answer': str(answer) + " questions have been asked in the last month"
    }
    return render(request, 'StackApp/question.html', context=context)
