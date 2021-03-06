from django.db import models
from django.core.validators import RegexValidator
from datetime import datetime
# Create your models here.
class College(models.Model):
    campus = models.CharField(max_length=50,)
    website_link = models.CharField(max_length=200)

    class Meta:
        unique_together = ('campus', 'website_link',)
    def __str__(self):
        return self.campus

class Roomate(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, validators=[RegexValidator(regex='^[A-Za-z\s]*$',
                                                                           message="Please enter a first name "
                                                                                   "(No numbers or special characters)",
                                                                           code="invalid_college")])
    last_name = models.CharField(max_length=30, validators=[RegexValidator(regex='^[A-Za-z]*$',
                                                                           message="Please enter a last name "
                                                                                   "(No numbers, special characters or spaces)",
                                                                           code="invalid_college")])
    student_id = models.CharField(blank= False, max_length = 30, validators=[RegexValidator(regex='^[A-Za-z0-9]*$',
                                                                           message="Please enter a Student ID "
                                                                                   "(No special characters or spaces)",
                                                                           code="invalid_college")])

    class Meta:
        unique_together = ('last_name', 'first_name','college', 'student_id')



    @property
    def full_name(self):
        return self.first_name + " " + self.last_name
    def __str__(self):
        return self.full_name


class Comment(models.Model):
    roomate = models.ForeignKey(Roomate)
    date = models.DateField(default=datetime.now)
    ONE = 1.0
    TWO = 2.0
    THREE = 3.0
    FOUR = 4.0
    FIVE = 5.0
    RATING_CHOICES = (
        (FIVE, "5"),
        (FOUR, "4"),
        (THREE, "3"),
        (TWO, "2"),
        (ONE, "1"),
    )
    Overall_Rating = models.DecimalField(choices=RATING_CHOICES, max_digits=2, decimal_places=1)
    Description = models.TextField(max_length= 500, blank= False, null= False)


    def __str__(self):
        return self.comment_name
    @property
    def comment_name(self):
        return 'Comment: ' + str(self.pk) + ', with Rating: ' + str(self.Overall_Rating) + ' , On: ' + str(self.date)

class CollegeSuggestion(models.Model):
    college = models.CharField(max_length = 50, validators=[RegexValidator(regex='^[A-Za-z\s]*$',
                                                                           message="Please enter a college name "
                                                                                   "(No numbers or special characters)",
                                                                           code="invalid_college")])
    def __str__(self):
        return self.college