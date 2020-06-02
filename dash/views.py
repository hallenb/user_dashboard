from django.shortcuts import render, redirect
from django.contrib import messages
from dash.models import Users, UserLevels, Messages, Comments
import bcrypt

def index(request):
    #preload database
    start = UserLevels.objects.filter()
    if len(start) == 0:
            UserLevels.objects.create(level=9)
            UserLevels.objects.create(level=5)
    return render(request, 'index.html')

def signin(request):
    return render(request, 'sign_in.html')

def register(request):
    return render(request, 'register.html')

def signout(request):
    request.session.clear()
    return redirect('/')

def user_show(request, num):
    if 'user_id' in request.session:
        user = Users.objects.get(id=num)
        message = Messages.objects.filter(message_to=user).order_by("-created_at")
        context = {
            'user': user,
            'message': message
        }
        return render(request, 'show.html', context)
    return redirect('/dashboard')

def post_message(request, num):
    if request.method == "POST":
        if 'user_id' in request.session:
            message_to = Users.objects.get(id=num)
            message_from = Users.objects.get(id=request.session["user_id"])
            Messages.objects.create(message=request.POST['message'], message_to=message_to, creator=message_from)
            return redirect(user_show, num)
        return redirect('/')
    return redirect('/dashboard')

def post_comment(request, num):
    if request.method == "POST":
        if 'user_id' in request.session:
            creator = Users.objects.get(id=request.session['user_id'])
            message = Messages.objects.get(id=request.POST['message'])
            Comments.objects.create(comment=request.POST['comment'], creator=creator, message=message)
            return redirect(user_show, num)
        return redirect('/')
    return redirect('/dashboard')

def newUser(request):
    if 'user_id' in request.session:
        user = Users.objects.get(id=request.session['user_id'])
        if user.user_level.level == 9:
            return render(request, 'newuser.html')
        return redirect('/dashboard')
    return redirect('/dashboard')

def remove_verify(request, num):
    if 'user_id' in request.session:
        context = {
            'user': Users.objects.get(id=num)
        }
        return render(request, 'remove.html', context)
    return redirect('/dashboard')

def delete_user(request, num):
    if 'user_id' in request.session:
        user = Users.objects.get(id=request.session['user_id'])
        if user.user_level.level == 9:
            rmuser = Users.objects.get(id=num)
            rmuser.delete()
        return redirect('/dashboard')
    return redirect('/dashboard')

def dashboard(request):
    if 'user_id' in request.session:
        context = {
            'users': Users.objects.all()
        }
        user = Users.objects.get(id=request.session['user_id'])
        if user.user_level.level == 9:
            return render(request, 'admin_dash.html', context)
        return render(request, 'dashboard.html', context)
    return redirect('/')

def user_edit(request, num):
    if 'user_id' in request.session:
        logged_user = Users.objects.get(id=request.session['user_id'])
        if logged_user.user_level.level == 9:
            context = {
                'user': Users.objects.get(id=num)
            }
            return render(request, 'user_edit.html', context)
        return redirect('/dashboard')
    return redirect('/dashboard')

def user_info(request, num):
    if request.method == 'POST':
        errors = Users.objects.info_validator(request.POST)

        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
                return redirect(user_edit, num)
        
        user = Users.objects.get(id=num)
        user.email = request.POST['email'].lower()
        user.fname = request.POST['fname']
        user.lname = request.POST['lname']
        if request.POST['level'] == '5':
            lev = UserLevels.objects.get(id=2)
            user.user_level = lev
        if request.POST['level'] == '9':
            lev = UserLevels.objects.get(id=1)
            user.user_level = lev
        user.save()
        return redirect('/dashboard')
    return redirect('/dashboard')

def user_pass(request, num):
    if request.method == 'POST':
        errors = Users.objects.pass_validator(request.POST)

        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
                return redirect(user_edit, num)

        user = Users.objects.get(id=num)
        hashed = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt())
        user.password = hashed.decode()
        user.save()
        return redirect('/dashboard')
    return redirect('/dashboard')

def profile(request):
    if 'user_id' in request.session:
        context = {
            'user': Users.objects.get(id=request.session['user_id'])
        }
        return render(request, 'profile.html', context)
    return redirect('/')

def profile_info(request):
    if request.method == 'POST':
        errors = Users.objects.info_validator(request.POST)

        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
                return redirect('/profile')
        
        user = Users.objects.get(id=request.session['user_id'])
        user.email = request.POST['email'].lower()
        user.fname = request.POST['fname']
        user.lname = request.POST['lname']
        user.save()
        return redirect('/dashboard')
    return redirect('/dashboard')

def profile_pass(request):
    if request.method == 'POST':
        errors = Users.objects.pass_validator(request.POST)

        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
                return redirect('/profile')

        user = Users.objects.get(id=request.session['user_id'])
        hashed = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt())
        user.password = hashed.decode()
        user.save()
        return redirect('/dashboard')
    return redirect('/dashboard')

def profile_desc(request):
    if request.method == 'POST':
        user = Users.objects.get(id=request.session['user_id'])
        user.description = request.POST['desc']
        user.save()
        return redirect('/dashboard')
    return redirect('/dashboard')

def newRegister(request):
    if request.method == "POST":
        errors = Users.objects.user_validator(request.POST)

        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
            if 'user_id' in request.session:
                return redirect('/user/new')
            return redirect('/register')

        new_user = Users.objects.filter()
        if len(new_user) > 0:
            lev = UserLevels.objects.get(id=2)
        else:
            lev = UserLevels.objects.get(id=1)

        hashed = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt())
        new_user = Users.objects.create(fname=request.POST['fname'],lname=request.POST['lname'],email=request.POST['email'].lower(), password=hashed.decode(), user_level=lev)

        if 'user_id' in request.session:
            return redirect('/dashboard')

        request.session['user_id'] = new_user.id

        return redirect('/dashboard')
    return redirect('/register')

def newSignin(request):
    if request.method=="POST":
        logged_user=Users.objects.filter(email=request.POST['email'].lower())
        if len(logged_user)>0:
            logged_user = logged_user[0]
            if bcrypt.checkpw(request.POST['pw'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect('/dashboard')
            return redirect('/signin')
        return redirect('/signin')
    return redirect('/signin')