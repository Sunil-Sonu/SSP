from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
# Create your views here.
from django.template.context import RequestContext

from .forms import UserForm, UserProfileForm
from .models import *
from django.contrib.auth import authenticate, login
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import urllib2


@login_required
def searchfile(request):
    context = RequestContext(request)
    search_query = request.POST['search_box']
    info = Softwares.objects.all().filter(name__contains=search_query)
    context = {'data': info}
    template = loader.get_template('search.html')
    return HttpResponse(template.render(context, request))


@login_required
def allsoftwares(request):
    context = RequestContext(request)
    info = Softwares.objects.all()
    context = {'data': info}
    template = loader.get_template('allsoftwares.html')
    return HttpResponse(template.render(context, request))


@login_required
def mysoftwares(request):
    context = RequestContext(request)
    userid = request.user.id - 1  # EXCLUDING SUPERUSER
    info = Purchases.objects.all().filter(curruser_id=userid).exclude(macid1="0")
    context = {'data': info}
    template = loader.get_template('mysoftwares.html')
    return HttpResponse(template.render(context, request))


@login_required
def macverficationdownload(request, pk):
    # CREATE AN OBJECT AND SAVE THESE DETAILS.
    software_object = Softwares.objects.get(pk=pk)
    category_id = software_object.list_id
    software_object.save()
    category_object = Categories.objects.get(id=category_id)
    category_object.save()
    user_object = UserProfile.objects.get(user_id=request.user.id)
    user_object.save()
    info = Purchases.objects.all().filter(curruser_id=(request.user.id - 1))
    if bool(info):
        info.delete()

    data = Purchases(curruser=user_object, softwareinfo=software_object, categoryinfo=category_object, macid1="0",
                     macid2="0", macid3="0", maccount=1)
    data.save()
    return HttpResponseRedirect('https://raw.githubusercontent.com/Sunil-Sonu/Trail/master/application.zip', {})


@login_required
def softwarepurchased(request, pk):
    context = RequestContext(request)
    userid = request.user.id
    softwaredetails = Softwares.objects.get(id=pk)
    url = softwaredetails.link
    return HttpResponseRedirect(url, {})


@login_required
def singleproduct(request, pk):
    context = RequestContext(request)
    info = Softwares.objects.all().filter(id=pk)
    context = {'data': info}
    template = loader.get_template('singleproduct.html')
    return HttpResponse(template.render(context, request))


@login_required
def products(request, pk):
    context = RequestContext(request)
    info = Softwares.objects.all().filter(list_id=pk)
    context = {'data': info}
    template = loader.get_template('products.html')
    return HttpResponse(template.render(context, request))


@login_required
def categories(request):
    context = RequestContext(request)
    info = Categories.objects.all()
    context = {'data': info}
    template = loader.get_template('categories.html')
    return HttpResponse(template.render(context, request))


@login_required
def homepage(request):
    context = RequestContext(request)
    info = Softwares.objects.all()
    context = {'data': info}
    template = loader.get_template('homepage.html')
    return HttpResponse(template.render(context, request))


@login_required
def searchitem(request):
    context = RequestContext(request)
    search_query = request.POST['search_box']
    info = Softwares.objects.all().exclude(current_id=request.user.id).filter(pname__contains=search_query)
    context = {'data': info}
    template = loader.get_template('search.html')
    return HttpResponse(template.render(context, request))


def register(request):
    context = RequestContext(request)

    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            curprofile = UserProfile.objects.get(user_id=user.id)
            print curprofile.passcheck
            print user.password
            print user.id
            curprofile.passcheck = user_form.cleaned_data['password']
            curprofile.save()

            registered = True

        else:
            print user_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
        'register.html',
        {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
        context)


def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/homepage/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return render_to_response('login.html', {}, context)
    return render_to_response('login.html', {}, context)


def index(request):
    context = RequestContext(request)
    return render_to_response('index.html', {}, context)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
