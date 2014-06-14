from django.contrib import admin
from Login.models import Person, WallPost, Messages

# Register your models here.
class WallInline(admin.TabularInline):
	model = WallPost

class MessageInline(admin.TabularInline):
	model = Messages

class Admin(admin.ModelAdmin):
	inlines = [WallInline, MessageInline]
	list_display = ('userID', 'name', 'birthday')
	search_fields = ['userID']

admin.site.register(Person, Admin)