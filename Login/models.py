from django.db import models

gender_list = (('Male','Male'),('Female','Female'),('Other', 'Other'))

# Create your models here.
class Person(models.Model):
	userID = models.CharField('User ID', max_length=50, unique=True, blank=False)
	name = models.CharField('Name', max_length=100, blank=False)
	email = models.EmailField('Email', max_length=200, blank=False)
	birthday = models.DateField('Birthday', blank=False)
	password = models.CharField(max_length=50, blank=False)
	gender = models.CharField('Gender',max_length=10, choices=gender_list, blank=False)
	contact = models.CharField('Contact No.', max_length=15, blank=True, null=True)
	friends = models.ManyToManyField('self', blank=True)
	sent_requests = models.ManyToManyField('self', blank=True, null=True, symmetrical=False, related_name="Sent")
	pending_requests = models.ManyToManyField('self', blank=True, null=True, symmetrical=False, related_name="Pending")
	def __unicode__(self):
		return unicode(self.name)

class WallPost(models.Model):
	userID = models.ForeignKey(Person)
	text = models.CharField('Content Text', max_length=2000)
	pub_date = models.DateTimeField('Date Published')
	def __unicode__(self):
		return self.text


class Messages(models.Model):
	sender = models.ForeignKey(Person)
	receiverID = models.CharField('Receiver ID', max_length=50)
	receiverName = models.CharField('Receiver Name', max_length=100)
	message_text = models.CharField('Message', max_length=2000)
	sent_date = models.DateTimeField('Message Sending Date')
	def __unicode__(self):
		return self.message_text


