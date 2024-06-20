from django.db import models
from django.contrib.auth.models import AbstractUser, User
from .choices import DEGREE_CHOICES, LEVEL_CHOICES, MAJOR_CHOICES
from .scripts import POSITION_HELP_TEXT

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    about = models.TextField(blank=True)


class Education(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    academy = models.CharField(max_length=255) # TODO: refactore to be a model
    degree = models.CharField(max_length=255, choices=DEGREE_CHOICES)
    major = models.CharField(max_length=255, choices=MAJOR_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='educations')

    def __str__(self):
        return '%s of %s' % (self.degree, self.academy)

class Experience(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    company = models.CharField(max_length=255) # TODO: refactore to be a model
    ##### DO NOT USE THID METHOD FOR HELP TEXTS! ####
    position = models.CharField(max_length=255, help_text=POSITION_HELP_TEXT) # TODO: refactore to be a model
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences')

    def __str__(self):
        return '%s %s' % (self.user, self.position)

class Task(models.Model):
    description = models.TextField()
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.description

class Skill(models.Model):
    level = models.CharField(max_length=255, choices=LEVEL_CHOICES)
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    tech_stack = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='tech_stacks')

class Language(models.Model):
    level = models.CharField(max_length=255, choices=LEVEL_CHOICES)
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='languages')

class Course(models.Model):
    academy_name = models.CharField(max_length=255) # TODO: refactore to be a model
    title = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return self.title

class Social(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='socials')
    url = models.URLField()
    image = models.ImageField(upload_to='social_images/', blank=True)
    name = models.CharField(max_length=255)
