from django.db import models

# Create your models here.
class College(models.Model):
    campus = models.CharField(max_length=50, unique=True)
    website_link = models.CharField(max_length=200)

    def __str__(self):
        return self.campus

class Roomate(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return self.first_name + " " + self.last_name

class Comment(models.Model):
    roomate = models.ForeignKey(Roomate)
    username = models.CharField(max_length=30)
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
    OverallRating = models.DecimalField(choices=RATING_CHOICES, max_digits=2, decimal_places=1)
    Description = models.TextField(max_length= 500, blank= False, null= False)

    def __str__(self):
        return self.username
