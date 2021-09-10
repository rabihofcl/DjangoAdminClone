from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User,auth

#from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
#from django.views.decorators.cache import never_cache

# Create your views here.

def ad_signin(request):
    if request.session.has_key('admin_login'):
        return redirect('ad_home')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)
            
            if user is not None:
                if user.is_superuser == True:
                    auth.login(request, user)
                    return redirect('ad_home')
                else:
                    messages.info(request,'Not an Admin User')
                    return render(request,'ad_signin.html')
            else:
                messages.info(request,'No User found')
                return render(request,'ad_signin.html')

        else:
            return render(request,'ad_signin.html')



#@user_passes_test(lambda user: user.is_superuser,login_url='ad_signin')
def ad_home(request):
    request.session['admin_login'] = 'admin_login'
    if request.session.has_key('admin_login'):
        if 'searchkey' in request.POST:
            searchkey = request.POST['searchkey']
            users = User.objects.order_by('id').filter(Q(username__contains=searchkey) | Q(email__contains=searchkey) | Q(id__contains=searchkey))
            return render(request,'ad_home.html',{'users':users} )
        else:
            users = User.objects.order_by('-id').all()
            return render(request,'ad_home.html',{'users':users} )
    else:
        return render(request,'ad_signin.html')
    



#@user_passes_test(lambda user: user.is_superuser,login_url='ad_signin')
def user_edit(request, user_id):
    if request.session.has_key('admin_login'):
        user =User.objects.get(pk=user_id)
        return render(request,'user_edit.html',{'user' : user})
    else:
        return render(request,'ad_signin.html')



#@user_passes_test(lambda user: user.is_superuser,login_url='ad_signin')
def update_user(request, user_id):
    if request.session.has_key('admin_login'):
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            User.objects.filter(pk=user_id).update(username=username, email=email)
            return redirect('ad_home')
    else:
        return render(request,'ad_signin.html')


#@user_passes_test(lambda user: user.is_superuser,login_url='ad_signin')
def cancel_edit(request):
    if request.session.has_key('admin_login'):
        return redirect('ad_home')
    else:
        return render(request,'ad_signin.html')


#@user_passes_test(lambda user: user.is_superuser,login_url='ad_signin')
def user_delete(request, user_id):
    if request.session.has_key('admin_login'):
        User.objects.filter(id=user_id).delete()
        return redirect('ad_home')
    else:
        return render(request,'ad_signin.html')


#@user_passes_test(lambda user: user.is_superuser,login_url='ad_signin')
def ad_signup(request):
    if request.session.has_key('admin_login'):
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username already taken')
                    return redirect('ad_signup')
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email already taken')
                    return redirect('ad_signup')
                else:
                    user = User.objects.create_user(username=username, password=password1, email=email)
                    user.save()
                    return redirect('ad_home')

            else:
                messages.info(request, 'Password is not matching')
                return redirect('ad_signup')
            
        else:
            return render(request,'ad_signup.html')
    else:
        return render(request,'ad_signin.html')


#@user_passes_test(lambda user: user.is_superuser,login_url='ad_signin')
def ad_signout(request):
    if request.session.has_key('admin_login'):
        #request.session.flush()
        del request.session['admin_login']
        #auth.logout(request)
        return render(request,'ad_signin.html')
    else:
        return render(request,'ad_signin.html')