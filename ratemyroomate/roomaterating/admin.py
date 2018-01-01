from django.contrib import admin
from .models import College, Roomate, Comment, CollegeSuggestion
# Register your models here.
admin.site.register(College)
admin.site.register(Roomate)
admin.site.register(Comment)
admin.site.register(CollegeSuggestion)
