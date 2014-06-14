from django.db import models
from Login.models import Person
# Create your models here.

class Category(models.Model):
	category = models.CharField('Category', max_length=100, unique=True, blank=False, null=False)
	def __unicode__(self):
		return self.category


class Question(models.Model):
	category = models.ForeignKey(Category)
	question = models.CharField('Question', max_length=200, unique=True)
	option1 = models.CharField('Option1', max_length=200, unique=True)
	option2 = models.CharField('Option2', max_length=200, unique=True)
	option3 = models.CharField('Option3', max_length=200, unique=True)
	option4 = models.CharField('Option4', max_length=200, unique=True)
	choice_list = (('option1', option1), ('option2', option2), 
		('option3', option3), ('option4', option4))
	correct_option = models.CharField('Correct Answer', 
		max_length=200, choices=choice_list, blank=False)
	def __unicode__(self):
		return self.question

class QuizRoom(models.Model):
	questions = models.ManyToManyField(Question, related_name='questions', null=False)
	member1 = models.ManyToManyField(Person, related_name='member1', null=False)
	member2 = models.ManyToManyField(Person, related_name='member2', null=False)
	startQuiz1 = models.BooleanField('Start Quiz 1', default=False)
	startQuiz2 = models.BooleanField('Start Quiz 2', default=False)
	marks1 = models.CharField('Marks 1', max_length=10)
	marks2 = models.CharField('Marks 2', max_length=10)
	time1 = models.CharField('Time 1', max_length=10)
	time2 = models.CharField('Time 2', max_length=10)
	def __str__(self):
		return str(self.pk)

class CategoryQuiz(models.Model):
	category = models.ForeignKey(Category)
	members = models.ManyToManyField(Person)