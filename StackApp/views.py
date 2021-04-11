import requests
from django.http import HttpResponse
from django.shortcuts import render


# response = requests.get('')
# data = response.json()

def home(request):
    return render(request, 'StackApp/index.html')


def question1(request):
    return render(request, 'StackApp/question.html')


def question2(request):
    return render(request, 'StackApp/question.html')


def question3(request):
    return render(request, 'StackApp/question.html')


def question4(request):
    return render(request, 'StackApp/question.html')


def question5(request):
    return render(request, 'StackApp/question.html')
