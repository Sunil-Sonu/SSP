from django.http.response import HttpResponseRedirect,HttpResponse
from django.shortcuts import render, render_to_response
# Create your views here.
from django.template.context import RequestContext

from .forms import UserForm,UserProfileForm
from .models import *
from django.contrib.auth import authenticate, login
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

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
    userid = request.user.id
    info = Purchases.objects.all().filter(curruser__user_id=userid)
    context = {'data': info}
    template = loader.get_template('mysoftwares.html')
    return HttpResponse(template.render(context, request))

@login_required
def softwarepurchased(request,pk):
    context = RequestContext(request)
    userid = request.user.id
    info = Purchases.objects.all().filter(curruser__user_id=userid, softwareinfo__id=pk )

    softwaredetails = Softwares.objects.get(id=pk)

    userdetails = UserProfile.objects.filter(user_id= userid)

    purchaseagain = False
    # IF LIST IS NULL, THEN THE USER BROUGHT IT FOR THE FIRST TIME.
    flag = False
    olduser = False
    newuser = False
    if info:
        #HE HAS ALREADY DOWNLOADED.
        if info[0].maccount ==3:
            # HE HAS PURCHASE IT AGAIN
            info[0].maccount = 1
            info[0].macid1 = "0"
            info[0].macid2 = "0"
            info[0].macid3 = "0"
            olduser = True
            purchaseagain = True
    else:
         newuser = True
    #LOGIC TO GET THE MAC ADDRESS FROM HIS SYSTEM
    import netifaces
    mylist = netifaces.interfaces()
    mydict = netifaces.ifaddresses(mylist[0])[netifaces.AF_LINK]
    str1 = mydict[0].get('addr')
    str2 = ""
    for i in str1:
            if i == ':':
                str2 += '-'
            else:
                str2 += i
    sysmac =  str2.upper()


    if newuser:
        softwaredetails.save()
        userdetails[0].save()
        software = Purchases(curruser= userdetails[0], softwareinfo= softwaredetails, macid1= sysmac, maccount= 1)
        software.save()
    if olduser:      # HE RE-PURCHASES THE SOFTWARE
        info[0].macid1 = sysmac
        info.save()

    # NOW HERE WE PUT IN THE DOWNLOAD FILE LOGIC
    import urllib2

    def getFileType(str):
        name = str.split('/')
        l = len(name)
        print name[l - 1]
        return name[l - 1]

    def setFileSize(int):
        code.seek(file_size - 1)
        code.write('\0')

    url = softwaredetails.link
    filename = getFileType(url)
    f = urllib2.urlopen(url)
    meta = f.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    # SETTING FILE PATH HERE
    import os
    filepath = os.path.join('C:\Users\Public\Downloads', filename)
    if not os.path.exists('C:\Users\Public\Downloads'):
        os.makedirs('C:\Users\Public\Downloads')
    code = open(filepath, "wb")


    setFileSize(file_size)
    code.seek(0)
    req = urllib2.Request(url, headers={'Range': 'bytes=' + str(file_size)})
    data = urllib2.urlopen(req).read()

    for i in data:
        code.write(i)
    code.close()
    return render_to_response('productpurchased.html', {}, context)


@login_required
def singleproduct(request, pk):
    context = RequestContext(request)
    info = Softwares.objects.all().filter(id= pk)
    context = { 'data' : info}
    template = loader.get_template('singleproduct.html')
    return HttpResponse(template.render(context,request))


@login_required
def products(request,pk):
    context = RequestContext(request)
    info = Softwares.objects.all().filter(list_id= pk)
    context = {'data': info}
    template = loader.get_template('products.html')
    return HttpResponse(template.render(context,request))

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
    context=RequestContext(request)
    search_query= request.POST['search_box']
    info=Softwares.objects.all().exclude(current_id=request.user.id).filter(pname__contains=search_query)
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
    return render_to_response('index.html',{},context)



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
