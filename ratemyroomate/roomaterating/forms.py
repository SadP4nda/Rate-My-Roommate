from django import forms
from .models import Comment, Roomate, CollegeSuggestion
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget


class CommentForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaWidget())
    class Meta:
        model = Comment
        fields = ('Overall_Rating', 'Description')

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-fields'

class RoommateCreateForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaWidget())
    class Meta:
        model = Roomate
        fields = ['college', 'first_name', 'last_name', 'student_id']

    def __init__(self, *args, **kwargs):
        super(RoommateCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-fields'

class CollegeSuggestionCreateForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaWidget())
    class Meta:
        model = CollegeSuggestion
        fields = ['college']

    def __init__(self, *args, **kwargs):
        super(CollegeSuggestionCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-fields'
