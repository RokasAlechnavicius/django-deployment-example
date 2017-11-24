from django.shortcuts import render
from basic_app.forms import UserForm,NewUserProfileInfo


# importai skirti loginui ir jo valdymui
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    context_dict = {'text':'hello world','number':100}
    return render(request,'basic_app/index.html',context_dict)

@login_required # reikalauja, kad butu prisijunge kad galetu kviesti logout funkcija. decorators
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

    return render(request,'basic_app/index.html',context_dict)

def other(request):
    return render(request,'basic_app/other.html')

def relative(request):
    return render(request,'basic_app/relative_url_templates.html')

def register(request):
    # assume, kad neregistruotas
    registered = False
    # jeigu request = post, paimam informacija esancia is forms
    if request.method =="POST":
        user_form = UserForm(data=request.POST)
        profile_form = NewUserProfileInfo(data=request.POST)
        # patikrinam ar abi forms atitinka restrictionus, jei taip tai paimam viska is
        # base user form
        if user_form.is_valid() and profile_form.is_valid() :
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit = False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    # jeigu nebuvo request post, tada tiesiog sukuriam ir grazinam
    else:
        user_form = UserForm()
        profile_form = NewUserProfileInfo()


    return render(request,'basic_app/registration.html',
                            {'user_form':user_form,
                              'profile_form':profile_form,
                              'registered':registered})






def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse(" account is not active")

        else:
            print("bad credentials")
            print("Username {} and password {}".format(username,password))
            return HttpResponse("invalid login details supplied")

    else:
        return render(request,"basic_app/login.html",{})
    #reurn render(request,'basic_app/login.html')
