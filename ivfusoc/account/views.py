from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegestrationForm, UserEditForm, ProfileEditForm, SearchForm
from django.contrib.postgres.search import SearchVector
from django.contrib.auth.decorators import login_required
from .models import Profile
import os
from images.models import Image
from django.contrib.auth.models import User
from django.conf import settings


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
            
    else:
        form = LoginForm()
    
    return render(request, 'account/login.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})

def register(request):
    if request.method == 'POST':
        user_form = UserRegestrationForm(request.POST)
        if user_form.is_valid():

            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            user = authenticate(request, username=user_form.cleaned_data['username'], password=user_form.cleaned_data['password'])
            
            new_user.save()
            
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            photo_path = os.path.join(settings.MEDIA_ROOT, 'users\03.png')

            profile_form = Profile(user=new_user, photo=photo_path)
            profile_form.save()

            return render(request, 'account/dashboard.html', {'section': 'dashboard'})
            
    else:
        user_form = UserRegestrationForm()

    return render(request, 'account/register.html', {'user_form': user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})

#def people_list(request):
#    users = User.objects.all()
#    return render(request, 'account/user_list.html', {'section': 'people','users': users})

def person_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = User.objects.annotate(search=SearchVector('username', 'first_name'),).filter(search=query)
    return render(request, 'account/search.html', {'form':form, 'query': query, 'results': results, 'section': 'people'}) 

def person_detail(request, id):
    person = get_object_or_404(Profile, id=id)
    media = Image.objects.filter(user=person.user)
    return render(request, 'account/user_detail.html', {'person': person, 'media': media})