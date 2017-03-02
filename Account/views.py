from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.core.exceptions import ValidationError
from django.http import *
from django.contrib.auth.forms import UserCreationForm

from Account.forms import LoginForm, RegistrationForm, Addaccount
from Account.models import Profile, Account , Post
from Account.script import instagram,twitter
from datetime import datetime,timedelta  
from django.utils.timezone import utc


def login(request):
	if not request.user.is_authenticated():
		context = {}
		try:
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				auth_login(request, user)
				return HttpResponseRedirect("/")
			else:
				context['error'] = 'Non active user'
				
		except:
			context['error'] = ''

		populateContext(request, context)
		return render(request, 'login.html', context)

	else:
		return HttpResponseRedirect("/") 

def logout(request):
	context = {}
	try:
		auth_logout(request)
		return HttpResponseRedirect("/")
	except:
		context['error'] = 'Some error occured.'
	
	populateContext(request, context)
	return render(request, 'login.html', context)

def populateContext(request, context):
	context['authenticated'] = request.user.is_authenticated()

	if context['authenticated'] == True:
		context['username'] = request.user.username



def register(request): 
	if not request.user.is_authenticated():
		form = RegistrationForm()

		if request.method == "POST":
			form = RegistrationForm(request.POST)

			if  form.is_valid():
				form.save()       
				return render(request,"login.html",
								   locals())
			else:
				form = RegistrationForm()
				return render(request,"register.html",
								   locals())
		else:
			form = RegistrationForm()
			return render(request, "register.html",{'form':form})

	else:
		return HttpResponseRedirect("/")    

def home(request):
	if request.user.is_authenticated():
		
		return render(request, "index.html")
	else:
		return render(request, "index.html")

def getuserinfo(request,susername=None):
	router = str(request.path_info)

	if router.find('instagram')!= -1:
		print(router.find('instagram'))
		data = Account.objects.get(url=susername,socialaccount='Instagram')
		filtreler = Post.objects.filter(owner=data).order_by('-date')[:5]
		
		last = Post.objects.filter(owner__socialaccount='Instagram').order_by('owner').values('owner__url').distinct()

		return render(request, 'index.html', {'callback': filtreler,'lastsource':last})

	elif router.find('twitter')!= -1:
		data = Account.objects.get(url=susername,socialaccount='Twitter')
		filtreler = Post.objects.filter(owner=data).order_by('-date')[:5]
		counter= len(Account.objects.filter(socialaccount='Twitter'))
		
		last=Post.objects.filter(owner__socialaccount='Twitter').order_by('owner').values('owner__url').distinct()
		
		return render(request, 'index.html', {'callback': filtreler})

	else:
		return render(request, 'index.html', {'callback': 'yokyokyok'})

def accountadd(request,susername=None):
	form = Addaccount()
	
	if request.method == "POST":
		form = Addaccount(request.POST)

		like_user = []
		
		if form.is_valid():
			formdata = form.save(commit=False)
		
			formdata.url = formdata.url.replace(
						"http://","").replace(
						"https://","").replace(
						"www.","").replace(
						"instagram.com/","").replace(
						"twitter.com/","").replace(
						"/","")

			
			if Account.objects.filter(url=formdata.url,socialaccount=formdata.socialaccount) :

				data = Account.objects.get(url=formdata.url,socialaccount=formdata.socialaccount)
				filtreler = Post.objects.filter(owner=data).order_by('-date')
				url = data.url

				if formdata.socialaccount == 'Instagram':
					likes = instagram.getfollowedby(url)
					enpoint = 'instagram/' + formdata.url

				elif formdata.socialaccount == 'Twitter':
					likes = twitter.getfollowedby(url)
					enpoint = 'twitter/' + formdata.url

				if filtreler:
					utcs= filtreler[0].date.tzinfo
					
					if (datetime.now(utcs) - filtreler[0].date).total_seconds() > 600:
						lastlikes=filtreler[0].likes
						
						newposts= Post(likes=likes,owner=data,likesraiting=(likes-lastlikes))
						newposts.save()
				else:
					newposts= Post(likes=likes,owner=data,likesraiting=0)
					newposts.save()


				return redirect(enpoint)
			
			else:
				try:

					formdata.save()
					form = 'ilk kayit'

				except Exception as e:
					form = e
				

				return render(request, 'index.html', {'callback': form})
		else:
			error = "Valid Error"	

		return render(request,'tumblr.html',{'error': error})

	else:
		countertw= len(Account.objects.filter(socialaccount='Instagram'))
		counterins= len(Account.objects.filter(socialaccount='Twitter'))
		
		return render(request, 'index.html', {'form': form,'countertw':countertw,'counterins':counterins})


