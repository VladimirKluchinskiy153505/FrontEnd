from django import forms
from django.core.validators import FileExtensionValidator, RegexValidator

from gym.models import LessonChoice, Master, Question, Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'score', 'text']

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=100)
    subject_name = forms.ChoiceField(choices=LessonChoice)
    phone_regex = RegexValidator(
        regex=r'\+375\d+$',
        message="Phone number must be in the format: '+375XXXXXXXXX'"
    )
    phone_number = forms.CharField(validators=[phone_regex])
    email = forms.EmailField(required=False)
    photo = forms.ImageField(required=False,
                             validators=[FileExtensionValidator(['jpg', 'jpeg', 'png','webp'])])
    individual_class_price = forms.IntegerField()

    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Master
        fields = ['username', 'subject_name', 'phone_number', 'email', 'photo', 'individual_class_price', 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(),
            'confirm_password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match.")
        # name = cleaned_data.get('username')
        # if Master.objects.filter(username=name).exists():
        #     raise forms.ValidationError("This name is already taken")

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class QuestionForm(forms.ModelForm):
    name = forms.CharField(label="Your Name", max_length=50)
    email = forms.CharField(label="Your Email", max_length=50)
    #timespan = forms.DateTimeField()
    question = forms.CharField(label="Your Question", widget=forms.Textarea)
    class Meta:
        model = Question
        fields = ['name', 'email', 'question']



