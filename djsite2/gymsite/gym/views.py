import json
import logging
import openai
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.urls import reverse
from django.db.models import Max, Min
import requests

from gym.forms import RegistrationForm, LoginForm, QuestionForm, ReviewForm
from gym.models import Master, Lesson, ClubCard, Client, Group, Article, Question, Vacancy, Review
from gym.constants import OPENAI_API_KEY, LessonChoice

logger = logging.getLogger(__name__)

# print('........lesson',lesson.subject_name, 'related to schedule',schedule.name)
def test_view(request):
    return render(request=request, template_name='gym/LabWork1/test_page.html')
def banners_view(request):
    return render(request=request, template_name='gym/LabWork2/2banners.html')
def scrolling_view(request):
    return render(request=request, template_name='gym/LabWork2/3scrolling_animation.html')
def volume_effect_view(request):
    return render(request=request, template_name='gym/LabWork2/4volume_effect.html')
def get_clients_data(request):
    data_from_database = Client.objects.values('name', 'gender', 'age', 'card')  # Замените на свои поля
    return JsonResponse(list(data_from_database), safe=False)
def wonder_table_view(request):
    return render(request=request, template_name='gym/LabWork2/9table.html')
def prototype_example(request):
    return render(request=request, template_name='gym/LabWork2/10class_prototype.html')
def extends_view(request):
    return render(request=request, template_name='gym/LabWork2/10class_extends.html')
def array_view(request):
    return render(request=request, template_name='gym/LabWork2/11array.html')
def leave_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Перенаправление на страницу "Спасибо за отзыв"
    else:
        form = ReviewForm()
    return render(request, 'gym/LabWork1/review_form.html', {'form': form})
def review_list_view(request):
    context={'review_list': Review.objects.all()}
    return render(request=request,template_name='gym/LabWork1/reviews7.html', context=context)
def vacancies_view(request):
    context={'vacancy_list': Vacancy.objects.all()}
    return render(request=request, template_name='gym/LabWork1/vacancies6.html', context=context)
def privacy_policy_view(request):
    return render(request=request, template_name='gym/LabWork1/privacy_policy5.html')
def submit_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()  # Save the question to the database
            #return redirect('gym/index.html')  # Redirect to a success page
        return redirect('home')
def view_explanation_dictionary_page(request):
    questions = Question.objects.all()
    context = {'question_list': questions}
    return render(request=request, template_name= 'gym/LabWork1/explanation_dictionary4.html', context=context)
def view_article_list(request):
    articles = Article.objects.all()
    context = {'article_list': articles}
    return render(request=request, template_name='gym/LabWork1/article_list3.html', context=context)
def about_view(request):
    return render(request=request, template_name='gym/LabWork1/about2.html')
def main_news_view(request):
    last_article = Article.objects.latest('timestamp')
    context = {'last_article': last_article}
    return render(request=request, template_name='gym/LabWork1/main_news1.html', context=context)
def logout(request):
    #return render(request, template_name='gym/index.html', context={'mastername': None})
    return index(request=request)
def get_statistics_dictionary():
    dt = dict()
    lessons = Lesson.objects.all()
    for lesson in lessons:
        lesson_students = 0  # people attending this lesson
        schedules = lesson.schedule_set.all()  # all schedules which reference this lesson
        for schedule in schedules:
            group = schedule.group
            group_clients = group.clients.all()#all clients of current_group
            lesson_students += len(group_clients)
        dt[lesson.get_subject_name()] = lesson_students*12
    return dt
def index(request, mastername=None):
    logger.warning('index_callded')
    masters = Master.objects.all()
    clients = Client.objects.all()
    max_object = Lesson.objects.aggregate(max_parameter=Max('lesson_price'))
    max_value = max_object['max_parameter']
    most_expensive_lesson = Lesson.objects.filter(lesson_price=max_value).first()

    min_object = Lesson.objects.aggregate(min_parameter=Min('lesson_price'))
    min_value = min_object['min_parameter']
    the_cheapest_lesson = Lesson.objects.filter(lesson_price=min_value).first()

    lessons = Lesson.objects.all()
    most_popular_subject = str()
    max_students_count = 0

    most_profitable_subject = str()
    max_weekly_profit = 0

    for lesson in lessons:
        lesson_students = set()#people attending this lesson
        lesson_profit = 0
        lessons_in_a_week = len(lesson.days.all())
        schedules = lesson.schedule_set.all()#all schedules which reference this lesson

        for schedule in schedules:
            group = schedule.group
            group_clients = group.clients.all()#all clients of current_group
            lesson_students.update(set(group_clients))

        for client in lesson_students:
            if client.card is not None:
                lesson_profit += lesson.lesson_price * (1 - float(client.card.get_discount() / 100))
            else:
                lesson_profit += lesson.lesson_price
        lesson_profit *= lessons_in_a_week

        if len(lesson_students) > max_students_count:
            max_students_count = len(lesson_students)
            most_popular_subject = lesson.get_subject_name()

        if lesson_profit > max_weekly_profit:
            most_profitable_subject = lesson.get_subject_name()
            max_weekly_profit = lesson_profit

    print('......type_clients', type(clients))
    sum = 0
    for item in clients:
        sum += item.age
    if len(clients) == 0:
        aver_age = 0
    else:
        aver_age = sum/len(clients)
    context = {
        'mastername': mastername,
        'masters': masters,
        'average_client_age': round(aver_age, 2),
        'most_expensive_lesson': most_expensive_lesson,
        'the_cheapest_lesson': the_cheapest_lesson,
        'most_popular_subject': most_popular_subject,
        'max_students_count': max_students_count,
        'most_profitable_subject': most_profitable_subject,
        'max_weekly_profit': round(max_weekly_profit, 2),
        'form': QuestionForm(),
        'statistics_dict': get_statistics_dictionary()
    }
    return render(request=request, template_name='gym/index.html',context=context)

def cards_view(request):
    cards = ClubCard.objects.all()
    context = {
        'cards': cards
    }
    return render(request=request, template_name='gym/clubcard_list.html', context=context)
def pageNotFound(request ,exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            subject_name = form.cleaned_data['subject_name']
            password = form.cleaned_data['password']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            photo = form.cleaned_data['photo']
            individual_class_price = form.cleaned_data['individual_class_price']
            # Check if the user already exists
            if Master.objects.filter(username=username).exists():
                messages.error(request, 'User already exists.')
                return redirect('registration')
            # Create and save the user to the database
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            master = Master(username=username, subject_name= subject_name, password=password, phone_number=phone_number, email=email, photo=photo, individual_class_price=individual_class_price, user=user)
            master.save()
            # Redirect the user to a success page or login page
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'gym/registration.html', {'form': form})
def login(request):
    return HttpResponse('Login')
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username =username, password=password)
            if user is not None:
                if user.is_superuser:
                    admin_url = reverse('admin:index')  # Replace 'admin:index' with the actual URL pattern for the admin panel
                    return redirect(admin_url)
                else:
                    #masters = Master.objects.all()
                    # context={'mastername': username,
                    #          'masters':masters}
                    # return render(request,template_name='gym/index.html',context=context) #Replace home
                    return index(request=request, mastername=username)
            else:
                form.add_error(None, 'Invalid email or password.')
    else:
        form = LoginForm()
    return render(request, 'gym/login.html', {'form': form})
def lesson_list(request):
    # Get filter parameters from the request GET parameters
    subject_name = request.GET.get('subject_name')
    lesson_price_higher = request.GET.get('lesson_price_higher')
    lesson_price_lower = request.GET.get('lesson_price_lower')

    # Apply filters based on the provided parameters
    lessons = Lesson.objects.all()
    subject_name_choices = Lesson.objects.values_list('subject_name', flat=True).distinct()
    full_name_choices = []
    lesson_dict = dict(LessonChoice)
    for item in subject_name_choices:
        full_name_choices.append(lesson_dict[str(item)])

    if subject_name:
        result_dict = {key: value for value, key in LessonChoice}
        lessons = lessons.filter(subject_name=result_dict[subject_name])
    if lesson_price_higher:
        lessons = lessons.filter(lesson_price__gte=lesson_price_higher)
    if lesson_price_lower:
        lessons = lessons.filter(lesson_price__lte=lesson_price_lower)
    context = {
        'lessons': lessons,
        'subject_name_choices': full_name_choices,
    }
    return render(request, 'gym/lesson_list.html', context)

def master_list(request):
    masters = Master.objects.all()
    context = {
        'masters': masters
    }
    return render(request, 'gym/master_list.html', context)
def lessons_for_current_master(request, username):
    master = Master.objects.get(username=username)
    related_lessons = master.lesson_set.all()
    context = {
        'lesson_list': related_lessons,
    }
    return render(request,'gym/lessons_for_current_user.html',context=context)
def students_for_current_master(request, username):
    master = Master.objects.get(username=username)
    related_students = master.individual_students.all()
    context = {
        'student_list': related_students
    }
    return render(request, 'gym/students_for_current_user.html', context=context)
def client_list(request):
    client_name = request.GET.get('client_name')
    client_age_higher = request.GET.get('client_age_higher')
    client_age_lower = request.GET.get('client_age_lower')
    clients = Client.objects.all()
    if client_name:
        clients = clients.filter(name=client_name)
    if client_age_higher:
        clients = clients.filter(age__gte=client_age_higher)
    if client_age_lower:
        clients = clients.filter(age__lte=client_age_lower)
    context = {'clients': clients}
    return render(request, 'gym/client_list.html', context=context)
def group_list(request):
    groups = Group.objects.all()
    context = {'group_list': groups}
    return render(request, 'gym/group_list.html', context=context)
def show_post(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    context = {
        'client':client
    }
    return render(request, 'gym/post_client.html', context=context)
def api_test(request):
    response = requests.get('https://dog.ceo/api/breeds/image/random').content
    response_dict = json.loads(response)
    image_url = response_dict['message']
    return render(request, 'gym/test_page.html', {'response': image_url})

def api_test2(request):
    openai.api_key = OPENAI_API_KEY

    response = openai.Image.create(
        prompt="a beautiful human face",
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    return render(request, 'gym/test_page.html', {'response': image_url})
