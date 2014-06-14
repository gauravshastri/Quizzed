from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from Quiz.models import Category, Question, QuizRoom, CategoryQuiz
from Login.models import Person
# Create your views here.

p = []

def index(request):
	try:
		user = get_object_or_404(Person, userID = request.session['userID'])
		friends = user.friends.all()
		cat = Category.objects.all()

		sent_req = QuizRoom.objects.filter(member1=user)
		received_req = QuizRoom.objects.filter(member2=user)
		
		
		return render_to_response('Quiz/index.html', {'category':cat,  
			'friends': friends, 'user': user, 'sr':sent_req, 'rr':received_req}, 
		context_instance=RequestContext(request))
	
	except:
		return HttpResponseRedirect(reverse('Login.views.index'))




def category_quiz(request):
	try:
		user = get_object_or_404(Person, userID = request.session['userID'])
		if request.method == 'GET':
			if 'id' in request.GET.keys():
				cat = Category.objects.get(category=request.GET['id'])
				quiz_id = request.GET['id']
				try:
					cat_quiz = CategoryQuiz.objects.get(pk=cat.pk)
				except:
					cat_quiz = CategoryQuiz(category = cat)
					cat_quiz.save()
					
				cat_quiz.members.add(user)

		return render_to_response('Quiz/category_quiz.html', {'category':cat,  
				'msg': quiz_id, 'category_quiz': cat_quiz}, 
			context_instance=RequestContext(request))

	except:
		return HttpResponseRedirect(reverse('Quiz.views.index'))


def start_quiz(request):
	#try:
		user = get_object_or_404(Person, userID = request.session['userID'])
		if request.method == 'GET':
			if 'id' in request.GET.keys():
				cat = Category.objects.get(id=request.GET['id'])
				msg = request.GET['id']
			if 'member' in request.GET.keys():
				member = Person.objects.get(userID=request.GET['member'])
				qr = QuizRoom(startQuiz1 = False, startQuiz2 = False,
					marks1 = 0, marks2 = 0, time1 = -1, time2 = -1)
				qr.save()
				global p
				p = Question.objects.filter(category=cat).order_by('?')[:5]
				qr.member1.add(user)
				qr.member2.add(member)
				for ques in p:
					qr.questions.add(ques)
				qr.save()
				q = qr.questions.all()
				
		return render_to_response('Quiz/start_quiz.html', {'category':cat,  
				'msg': msg, 'questions':q, 'member': member, 'user':user, 'quizroom':qr}, 
			context_instance=RequestContext(request))

	#except:
		return HttpResponseRedirect(reverse('Quiz.views.index'))


def result(request):
	try:
		if request.method == 'POST':
			total = 0
			qr = QuizRoom.objects.get(pk=request.GET['quizroom'])
			for (index, ques) in enumerate(p):
				ans = "answer["+str(index+1)+"]"
				if ans in request.POST.keys():
					if ques.correct_option == request.POST[ans]:
						total = total +1
	
			score = total
			user = get_object_or_404(Person, userID=request.session['userID'])
			for m in qr.member1.all():
					if user.userID == m.userID:
						qr.marks1 = total
						qr.save()
			for m in qr.member2.all():
				if user.userID == m.userID:
					qr.marks2 = total
					qr.save()

		return render_to_response('Quiz/result.html', {'score':score, 'challenge':qr}, 
		context_instance=RequestContext(request))

	except:
		if 'end' in request.GET.keys():
			try:
				q = QuizRoom.objects.get(pk=request.GET['end']).delete()
			except:
				return HttpResponseRedirect(reverse('Quiz.views.index'))

		return HttpResponseRedirect(reverse('Quiz.views.index'))



def challenge(request):
	try:
		user = get_object_or_404(Person, userID = request.session['userID'])
		friends = user.friends.all()
		if request.method == 'GET':
			if 'friend' in request.GET.keys():
				msg = "GET data received..."
				friend = Person.objects.get(userID=request.GET['friend'])
				qr = QuizRoom(startQuiz1 = False, startQuiz2 = False,
					marks1 = 0, marks2 = 0, time1 = -1, time2 = -1)
				qr.save()
				global p
				p = Question.objects.all().order_by('?')[:3]
				qr.member1.add(user)
				qr.member2.add(friend)
				for ques in p:
					qr.questions.add(ques)
				qr.save()

				return render_to_response('Quiz/challenge.html',
					{'user': user, 'msg': msg, 'friend': friend, 'challenge':qr}, 
					context_instance=RequestContext(request))

			if 'end' in request.GET.keys():
				q = QuizRoom.objects.get(pk=request.GET['end']).delete()
				return HttpResponseRedirect(reverse('Quiz.views.index'))

			if 'quizroom' in request.GET.keys():
				quizroom = request.GET['quizroom']
				qr = QuizRoom.objects.get(pk=quizroom)
				for m in qr.member1.all():
					if user.userID == m.userID:
						msg = "User is %s" % m.name
						qr.startQuiz1 = True
						qr.save()
				for m in qr.member2.all():
					if user.userID == m.userID:
						msg = "User is %s" % m.name
						qr.startQuiz2 = True
						qr.save()
				
				p = qr.questions.all()
				
				return render_to_response('Quiz/challenge_quiz.html',
					{'p':p, 'friends': friends, 'user': user, 
					'msg':msg, 'quizroom': quizroom}, 
					context_instance=RequestContext(request))

		return HttpResponseRedirect(reverse('Quiz.views.index'))

	except:
		return HttpResponseRedirect(reverse('Quiz.views.index'))