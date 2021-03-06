from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User,auth

#from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.views.decorators.cache import never_cache

# Create your views here.
@never_cache
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
                    request.session['admin_login'] = 'admin_login'
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
@never_cache
def ad_home(request):
    
    if request.session.has_key('admin_login'):
        users = User.objects.order_by('id').all()
        return render(request,'ad_home.html',{'users':users} )
    else:
        return render(request,'ad_signin.html')
    



#@user_passes_test(lambda user: user.is_superuser,login_url='ad_signin')
@never_cache
def user_edit(request, id):
    if request.session.has_key('admin_login'):
        user =User.objects.get(pk=id)
        return render(request,'user_edit.html',{'user' : user})
    else:
        return render(request,'ad_signin.html')



#@user_passes_test(lambda user: user.is_superuser,login_url='ad_signin')
@never_cache
def update_user(request, id):
    if request.session.has_key('admin_login'):
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            if User.objects.exclude(id=id).filter(username=username).exists():
                messages.info(request,'Username already taken')
                return redirect('update_user',id=id)
            elif User.objects.exclude(id=id).filter(email=email).exists():
                messages.info(request,'Email already taken')
                return redirect('update_user',id=id)
            else:
                User.objects.filter(pk=id).update(username=username, email=email)
                return redirect('ad_home')
        else:
            user =User.objects.get(pk=id)
            return render(request,'user_edit.html',{'user' : user})
    else:
        return render(request,'ad_signin.html')


#@user_passes_test(lambda user: user.is_superuser,login_url='ad_signin')
@never_cache
def cancel_edit(request):
    if request.session.has_key('admin_login'):
        return redirect('ad_home')
    else:
        return render(request,'ad_signin.html')


#@user_passes_test(lambda user: user.is_superuser,login_url='ad_signin')
@never_cache
def user_delete(request, user_id):
    if request.session.has_key('admin_login'):
        User.objects.filter(id=user_id).delete()
        return redirect('ad_home')
    else:
        return render(request,'ad_signin.html')


#@user_passes_test(lambda user: user.is_superuser,login_url='ad_signin')
@never_cache
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
@never_cache
def ad_signout(request):
    if request.session.has_key('admin_login'):
        #request.session.flush()
        del request.session['admin_login']
        #auth.logout(request)
        return render(request,'ad_signin.html')
    else:
        return render(request,'ad_signin.html')