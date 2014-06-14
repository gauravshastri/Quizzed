from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django import forms
from Login.models import Person, WallPost, Messages
from Quiz.models import CategoryQuiz
from itertools import chain
from operator import attrgetter
import datetime

# Create your views here.
message1 = "Please Login"
message2 = "New User, Please Register!!!"

def index(request):
	global login, message1, message2
	try:
		new_user = Person.objects.get(userID=request.POST['user'])
		if(new_user.password==request.POST['password']):
			request.session['userID'] = new_user.userID
			return HttpResponseRedirect(reverse('Login.views.login_success'))
		else:
			message1 = "Username or Password Incorrect"
			message2 = "Authentication Failed..."
	except:
		pass
	
	return render_to_response('Login/index.html', 
		{'message1':message1, 'message2':message2}, 
		context_instance=RequestContext(request))


def features(request):
	return render_to_response('Login/features.html')

def contact(request):
	return render_to_response('Login/contact.html')

def message_refresh(request):
	return render_to_response('Login/message_refresh.html')


def logout(request):
	try:
		message1 = "Logged Out Successfully"
		message2 = "Come back soon..."
		user = get_object_or_404(Person, userID = request.session['userID'])
		cat_all = CategoryQuiz.objects.all()
		for cat in cat_all:
			if user in cat.members.all():
				q = cat.members.remove(user)
				message1 = "User removed from Category Quiz"

		del request.session['userID']
		global message1, message2 
		
	except KeyError:
		pass
	return HttpResponseRedirect(reverse('Login.views.index'))

		
def login_success(request):
	try:
		posts=[]
		p = get_object_or_404(Person, userID = request.session['userID'])
		if request.method == 'POST':
			post = request.POST['wallpost']
			p.wallpost_set.create(text=post, pub_date=datetime.datetime.now())
			p.save()
			return HttpResponseRedirect(reverse('Login.views.login_success',))
		post1 = p.wallpost_set.all()
		friends = p.friends.all()
		for (index,friend) in enumerate(friends):
			if index == 0:
				post1 = post1
			else:
				post1 = []
			post=friend.wallpost_set.all()
			posts.append(sorted(chain(post, post1), key=attrgetter('pub_date')))

		deleteError = ""
		bg = ""
		if request.method == 'GET':
			if 'delete' in request.GET.keys():
				post = WallPost.objects.get(pk=request.GET['delete'])
				if post.userID.userID == p.userID:
					post.delete()
					bg = "bg-info"
					deleteError = "Deletion was successful!!!"
				else:
					bg="bg-primary"
					deleteError = "You are not authorized to delete that post..."
				

		return render_to_response('Login/home.html/', 
			{'user': p, 'friends': friends, 'post': posts, 
			'deleteError': deleteError, 'bg':bg},
			context_instance=RequestContext(request))
	except:
		global message1
		message1 = "Invalid Authentication :("
		return HttpResponseRedirect(reverse('Login.views.index',))




def messages(request):
	try:
		if 'delete' in request.GET.keys():
			message = Messages.objects.get(pk=request.GET['delete'])
			message.delete()
			
		if 'friend' in request.GET.keys():
			p = get_object_or_404(Person, userID=request.session['userID'])
			friend = Person.objects.get(userID=request.GET['friend'])
			if request.method == 'POST':
				new_message = request.POST['message']
				p.messages_set.create(message_text=new_message, 
					sender=p,
					receiverID=friend.userID,
					receiverName=friend.name,
					sent_date=datetime.datetime.now())
				p.save()
			messages_sent = p.messages_set.filter(receiverID=friend.userID)
			messages_received = friend.messages_set.filter(receiverID=p.userID)
			messages = sorted(chain(messages_sent, messages_received), key=attrgetter('sent_date'))
			return render_to_response('Login/message_user.html',
			{'messages':messages, 'user':p, 'friend':friend},
			context_instance=RequestContext(request))

		messages=[]
		senders=[]
		finalList=[]
		p = get_object_or_404(Person, userID=request.session['userID'])
		friends = p.friends.all()
		for friend in friends:
			messages_sent = p.messages_set.filter(receiverID=friend.userID)
			messages_received = friend.messages_set.filter(receiverID=p.userID)
			messages.append(sorted(chain(messages_sent, messages_received), key=attrgetter('sent_date')))

		for messageSet in messages:
			if len(senders)==6:
					break;
			for message in messageSet:
				if message.sender.userID in senders:
					pass
				else:
					senders.append(message.sender.userID)
				if message.receiverID in senders:
					pass
				else:
					senders.append(message.receiverID)
		if p.userID in senders:
			senders.remove(p.userID)

		for sender in senders:
			user = Person.objects.get(userID=sender)
			messages_sent = p.messages_set.filter(receiverID=sender)
			messages_received = user.messages_set.filter(receiverID=p.userID)
			messages_all = sorted(chain(messages_sent, messages_received), key=attrgetter('sent_date'), reverse=True)
			item = { 'userID': user.userID, 'name': user.name, 'messages': messages_all[:3] }
			finalList.append(item)

		return render_to_response('Login/message_base.html', 
			{'msg': messages, 'user':p, 'friends': friends,
			'senders':senders, 'finalList': finalList},
			context_instance=RequestContext(request))

	except:
		pass

	global message1
	message1 = "Invalid Authentication :("
	return HttpResponseRedirect(reverse('Login.views.index',))







def friends(request):
	try:
		msg = ""
		p = get_object_or_404(Person, userID = request.session['userID'])
		if request.method == 'GET':
			if 'id' in request.GET.keys():
				new_friend = Person.objects.get(userID=request.GET['id'])
				
				p.sent_requests.add(new_friend)
				new_friend.pending_requests.add(p)

				new_friend.save()
				p.save()
				msg = new_friend.name

			if 'accept' in request.GET.keys():
				msg="here..."
				friend_id = Person.objects.get(userID=request.GET['accept'])
				friend_pending = friend_id.sent_requests.all()
				if p in friend_pending:
					msg = "Friend Request Accepted"
					p.pending_requests.remove(friend_id)
					friend_id.sent_requests.remove(p)
					p.friends.add(friend_id)
					p.save()
					friend_id.save()
				else:
					msg="You don't have a request from this person..."

		pending_requests = p.pending_requests.all()
		sent_requests = p.sent_requests.all()
		friends = p.friends.all()
		persons = Person.objects.all().exclude(userID = p.userID)
		return render_to_response('Login/friends.html', 
			{'user': p, 'friends': friends, 'persons': persons, 'msg': msg,
			'pending_requests': pending_requests, 'sent_requests': sent_requests,
			},
			context_instance=RequestContext(request))
	except:
		global message1, message2
		message1 = "Invalid Authentication :("
		message2 = "Please try again..."
		return HttpResponseRedirect(reverse('Login.views.index',))







def register(request):
    try:
    	new_userID = request.POST['userID']
    	new_name = request.POST['name']
    	new_email = request.POST['email']
    	new_birthday = request.POST['birthday']
    	new_password = request.POST['password']
    	new_gender = request.POST['gender']
    	new_contact = request.POST['contact']
    	p = Person(userID=new_userID, name =new_name, email=new_email,
    		birthday=new_birthday, password=new_password,
    		gender=new_gender, contact=new_contact)
    	p.save()
    	global message1, message2
    	message1 = "New User Created!!"
    	message2 = "Login to continue..."
    	return HttpResponseRedirect(reverse('Login.views.index',))
    except:
    	pass

    return render_to_response(
    	'Login/register.html',
		context_instance=RequestContext(request))




