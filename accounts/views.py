from django.shortcuts import render, redirect 
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.views.decorators.cache import never_cache


# Create your views here.
def signin(request):
    if request.session.has_key('user_login'):
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username,password=password)

            if user is not None:
                auth.login(request, user)
                request.session['user_login'] = 'user_login'
                return redirect('home')
            else:
                messages.info(request,'Invalid credentials')
                return redirect('signin')
        else:
            return render(request,'signin.html')


def signup(request):
    if request.session.has_key('user_login'):
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username already taken')
                    return redirect('signup')
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email already taken')
                    return redirect('signup')
                else:
                    user = User.objects.create_user(username=username, password=password1, email=email)
                    user.save()
                    return redirect('signin')

            else:
                messages.info(request, 'Password is not matching')
                return redirect('signup')
            
        else:
            return render(request,'signup.html')



def home(request):
    if request.session.has_key('user_login'):
        return render(request,'home.html')
    else:
        return render(request,'signin.html')




def signout(request):
    if request.session.has_key('user_login'):
        #request.session.flush()
        del request.session['user_login']
        #auth.logout(request)
        return redirect('signin')
    else:
        return redirect('signin')