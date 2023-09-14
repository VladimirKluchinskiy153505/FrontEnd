
import os

import openai
import requests
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from gymsite import settings
from django.db import models
from django.contrib.auth.models import User
from gym.constants import *
class Review(models.Model):
    name = models.CharField(max_length=50,unique=True, verbose_name='Name')
    score = models.IntegerField(
        validators=[
            MinValueValidator(0, message='Оценка не может быть отрицательной'),
            MaxValueValidator(10, message ='Оценка не может быть больше 10')
        ]
    )
    text = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='DataTime')

    class Meta:
        ordering = ['timestamp']
class Vacancy(models.Model):
    subject_name = models.CharField(max_length=20, choices=LessonChoice, default='NoneSubject',verbose_name='SubjectName')
class Question(models.Model):
    name = models.CharField(max_length=50, verbose_name='Name')
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='DataTime')
    question = models.TextField(max_length=500, verbose_name='QuestionContent')
    answer = models.TextField(max_length=3000,null=True, verbose_name='QuestionAnswer')
    class Meta:
        ordering = ['timestamp']
class Article(models.Model):
    name = models.CharField(max_length=50, verbose_name='ArticleName')
    content = models.TextField(max_length=10000)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='DataTime', null=True)
    def __str__(self):
        return self.name
    def get_first_sentence(self):
        return self.content[0:self.content.find('.')+1]
class Group(models.Model):
    name = models.CharField(max_length=50, verbose_name='GroupName')
    period_price = models.IntegerField()
    clients = models.ManyToManyField('Client')
    schedule = models.OneToOneField('Schedule', on_delete=models.PROTECT)
    def get_clients(self):
        return self.clients.all()
    def __str__(self):
        return self.name
class ClubCard(models.Model):
    name = models.CharField(max_length=10, choices=CardNameChoice, verbose_name='ClubCard')
    discount =models.IntegerField(choices=CardDiscountChoice)
    image = models.ImageField(upload_to="photos/card_images", null=True)
    def __str__(self):
        return dict(CardNameChoice)[str(self.name)]
    def get_discount(self):
        return dict(CardDiscountChoice)[self.discount]

    class Meta:
        ordering = ['discount']
class Client(models.Model):
    name = models.CharField(max_length=50, verbose_name='ClientName')
    gender = models.CharField(max_length=1, choices=GenderChoice)
    age = models.IntegerField(max_length=3, default=0)
    photo = models.ImageField(upload_to="photos/clients", verbose_name='Photo',blank=True, null=True)
    card = models.ForeignKey('ClubCard', on_delete=models.PROTECT,null=True, blank=True,default=None, verbose_name='DiscountCard')
    def save(self, *args, **kwargs):
        if not self.photo:
            openai.api_key = OPENAI_API_KEY

            response = openai.Image.create(
                prompt=f"a beautiful face of human with name:{self.name}, gender:{self.gender}, age{self.age}",
                n=1,
                size="1024x1024"
            )
            if 'data' in response and len(response['data']) > 0:
                chosen_photo = response['data'][0]
                photo_url = chosen_photo['url']

                # Download and save the image to the media folder
                photo_name = f"{self.name}_photo.jpg"
                photo_path = os.path.join(settings.MEDIA_ROOT, 'photos/clients', photo_name)

                response = requests.get(photo_url)
                response.raise_for_status()

                with open(photo_path, 'wb') as file:
                    file.write(response.content)

                # Save the path to the photo in the model field
                self.photo = os.path.join('photos/clients', photo_name)
            else:
                # Error handling for OpenAI API request failure
                raise ValueError('Failed to choose client photo')

        super().save(*args, **kwargs)
    def __str__(self):
        return self.name
    def get_gender(self):
        if self.gender == 'F':
            return 'Female'
        else:
            return 'Male'
    def get_absolute_url(self):
        return reverse('post_client', kwargs={'client_id': self.pk})

    def get_final_cost(self):
        groups = self.group_set.all()#get all groups attending by client
        if self.card == None:
            discount = 0
        else:
            discount = self.card.get_discount()#get discount in %

        total_sum = 0
        for group in groups:
            group_price = 0
            group_schedule = group.schedule
            weeks = group_schedule.weeks_count
            for lesson in group_schedule.lessons.all():
                days = lesson.get_days_count()
                group_price += lesson.lesson_price*days
            group_price *= weeks
            total_sum += group_price
        masters = self.master_set.all()
        for master in masters:
            total_sum+= master.individual_class_price
        return round(total_sum*(1-discount/100), 2)

    class Meta:
        ordering = ['name']
class Lesson(models.Model):
    subject_name = models.CharField(max_length=50, choices=LessonChoice, verbose_name='SubjectName')
    start_time = models.TimeField()
    end_time = models.TimeField()
    lesson_price = models.IntegerField()
    photo = models.ImageField(upload_to="photos/lessons", verbose_name='Photo', default=None, blank=True)
    masters = models.ManyToManyField('Master')
    days = models.ManyToManyField('Day')
    lesson_gym = models.ForeignKey('ClubGym', on_delete=models.PROTECT,default=None, verbose_name='PlaceForConductingClasses')
    def get_days_count(self):
        return len(self.days.all())
    def save(self, *args, **kwargs):
        if not self.photo:
            openai.api_key = OPENAI_API_KEY
            response = openai.Image.create(
                prompt=f"a picture of activity with name:{self.get_subject_name()}",
                n=1,
                size="1024x1024"
            )
            if 'data' in response and len(response['data']) > 0:
                chosen_photo = response['data'][0]
                photo_url = chosen_photo['url']

                # Download and save the image to the media folder
                photo_name = f"{self.subject_name}_{self.pk}_photo.jpg"
                photo_path = os.path.join(settings.MEDIA_ROOT, 'photos/lessons', photo_name)

                response = requests.get(photo_url)
                response.raise_for_status()

                with open(photo_path, 'wb') as file:
                    file.write(response.content)

                # Save the path to the photo in the model field
                self.photo = os.path.join('photos/lessons', photo_name)
            else:
                # Error handling for OpenAI API request failure
                raise ValueError('Failed to choose lesson photo')
        super().save(*args, **kwargs)
    def __str__(self):
        return self.subject_name

    def get_days(self):
        day_dict =dict(DayChoice)
        day_list = [str(obj) for obj in self.days.all()]
        new_day_list = [day_dict[obj] for obj in day_list]
        return new_day_list
    def get_subject_name(self):
        return dict(LessonChoice)[str(self.subject_name)]

    def get_related_masters(self):
        return self.masters.all()

    class Meta:
        ordering = ['subject_name', 'start_time']
class Master(models.Model):
    username = models.CharField(max_length=50,unique=True,default='NoneMaster', verbose_name='MasterName')
    subject_name = models.CharField(max_length=20, choices=LessonChoice,default='NoneSubject', verbose_name='SubjectName')
    password = models.CharField(max_length=100, default='***')
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    photo = models.ImageField(upload_to="photos/masters", verbose_name='Photo', default=None,blank=True)
    individual_class_price = models.IntegerField(default=10)
    individual_students = models.ManyToManyField('Client', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        print('.........save called')
        if not self.photo:
            openai.api_key = OPENAI_API_KEY
            response = openai.Image.create(
                prompt=f"a picture of {self.get_subject_name()} trainer with name:{self.username}",
                n=1,
                size="1024x1024"
            )
            if 'data' in response and len(response['data']) > 0:
                chosen_photo = response['data'][0]
                photo_url = chosen_photo['url']

                # Download and save the image to the media folder
                photo_name = f"{self.username}_photo.jpg"
                photo_path = os.path.join(settings.MEDIA_ROOT, 'photos/masters', photo_name)

                response = requests.get(photo_url)
                response.raise_for_status()

                with open(photo_path, 'wb') as file:
                    file.write(response.content)

                # Save the path to the photo in the model field
                self.photo = os.path.join('photos/masters', photo_name)
            else:
                # Error handling for OpenAI API request failure
                raise ValueError('Failed to choose client photo')

        super().save(*args, **kwargs)
    def __str__(self):
        return self.username
    def get_subject_name(self):
        return dict(LessonChoice)[str(self.subject_name)]
    class Meta:
        ordering = ['username']
class Day(models.Model):
    name = models.CharField(max_length=10, choices=DayChoice)
    def __str__(self):
        return self.name
# Create your models here.
class Schedule(models.Model):
    name = models.CharField(max_length=50, default='000')
    weeks_count = models.IntegerField()
    lessons = models.ManyToManyField('Lesson')
    def __str__(self):
        return 'schedule '+str(self.name)
class ClubGym(models.Model):
    name = models.CharField(max_length=20, choices=ClubGymChoice)
    floor = models.IntegerField()
    def __str__(self):
        return dict(ClubGymChoice)[str(self.name)]

