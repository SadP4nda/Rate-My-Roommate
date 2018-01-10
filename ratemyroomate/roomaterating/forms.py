from django import forms
from .models import Comment, Roomate, CollegeSuggestion
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget


class CommentForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaWidget())
    class Meta:
        model = Comment
        fields = ('Overall_Rating', 'Description')


class RoommateCreateForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaWidget())
    class Meta:
        model = Roomate
        fields = ['college', 'first_name', 'last_name', 'student_id']

class CollegeSuggestionCreateForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaWidget())
    class Meta:
        model = CollegeSuggestion
        fields = ['college']