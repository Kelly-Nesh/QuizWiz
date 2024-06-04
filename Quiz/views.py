from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from .forms import addQuestionform, createuserform
from .models import Topic, Question, Scores
from django.http import HttpResponse
import random


def home(request):
    return render(request, 'Quiz/home.html')


def addQuestion(request):
    if request.user.is_staff:
        form = addQuestionform()
        if (request.method == 'POST'):
            form = addQuestionform(request.POST)
            if (form.is_valid()):
                form.save()
                return redirect('/')
        context = {'form': form}
        return render(request, 'Quiz/addQuestion.html', context)
    else:
        return redirect('home')


def registerPage(request):
    print(request.POST)
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = createuserform()
        if request.method == 'POST':
            form = createuserform(request.POST)
            if form.is_valid():
                user = form.save()
                return redirect('login')
        context = {
            'form': form,
        }
        return render(request, 'Quiz/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
        context = {}
        return render(request, 'Quiz/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('/')


def topics(request):
    topics = Topic.objects.order_by("name")
    context = {
        'topics': topics
    }
    return render(request, 'Quiz/topics.html', context)


def quiz(request, slug):
    questions = Question.objects.filter(topic__slug=slug)

    if request.method == 'POST':
        score = 0
        wrong = 0
        correct = 0
        total = 0
        for q in questions:
            print(q.ans, request.POST.get(q.question))
            total += 1
            if q.ans == int(request.POST.get(q.question) or 5):
                score += 10
                correct += 1
            else:
                wrong += 1
        percent = score/(total*10) * 100
        context = {
            'score': score,
            'time': request.POST.get('timer'),
            'correct': correct,
            'wrong': wrong,
            'percent': int(percent),
            'total': total
        }
        sc = Scores.objects.get_or_create(
            user=request.user, topic=Topic.objects.get(slug=slug))
        sc[0].score = percent
        sc[0].save()
        return render(request, 'Quiz/result.html', context)
    else:
        context = {
            'questions': questions,
            'topic': Topic.objects.get(slug=slug).name
        }
        # print(questions)
        return render(request, 'Quiz/quiz-page.html', context)


def score(request):
    user = request.user
    scores = Scores.objects.filter(user=user)
    return render(request, "Quiz/user-details.html", {"scores": scores})
