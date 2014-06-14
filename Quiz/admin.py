from django.contrib import admin
from Quiz.models import Question, Category, QuizRoom
# Register your models here.

class QuestionAdmin(admin.TabularInline):
	model = Question

class CategoryAdmin(admin.ModelAdmin):
	inlines = [QuestionAdmin]

admin.site.register(Category, CategoryAdmin)
admin.site.register(QuizRoom)