from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import sqlite3
import datetime
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import  Memo

# Create your views here.

#Flaw 2: Broken authentication, easiest way to make it better is by not using GET.methods.
# Another way would be to introduce a changepasswordForm class like this:
# class ChangePasswordForm(forms.Form):
#       password = forms.CharField(widgets=forms.PasswordInput)
#       confirm_password = forms.CharField(widget=forms.PasswordInput)
# The for requires an entire rework of the changePassword function to work, let's just use
# the simple solution and change to POST
@login_required
def changePassword(request):
    if request.method == 'GET': # Change to 'POST'

        user= request.user
        password= request.GET.get('password') # change to POST
        confirm_password = request.GET.get('confirm_password')#Change to POST

        if password == confirm_password:
            user.set_password(confirm_password)
            user.save()
            return redirect("/")
        else:
            return redirect("/")
    return redirect("/")

@login_required
@csrf_exempt #Flaw 3: remove csrf_exempt and add csrf_token to function in index.html
def addMemo(request):
    #Flaw 1: Injection flaw

    #if request.method == 'POST':
        #text = request.POST.get('memo')
        #owner = request.user
        #new_memo = Memo.objects.create(memo=text, owner=owner, created_at=datetime.datetime.now())
        #new_memo.save()
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    text = request.POST.get('memo')
    owner_id = request.user.id
    cursor.execute("INSERT INTO memos_memo (memo, owner_id, created_at) VALUES (?,?, ?)", (text, owner_id, datetime.datetime.now()))
    conn.commit()
    return redirect("/")

@login_required
def removeOldestMemo(request):
    if request.method == 'POST':
        user_memos = Memo.objects.filter(owner=request.user).order_by('created_at')

    if user_memos.exists():
        oldest_memo = user_memos.first()
        oldest_memo.delete()
    return redirect('/')

@login_required
def homePageView(request):
    memo = Memo.objects.filter(owner=request.user)
    context = {'memo': memo, 'is_authenticated': request.user.is_authenticated, 'is_staff': request.user.is_staff}
    return render(request, 'memos/index.html', context)

def is_admin(user):

    return user.is_authenticated and user.is_staff



# Flaw 5: broken access control. No real check to verify if it is the right user who is trying to acces the admin page
# comment out @login_required and add @user_passes_test

#@user_passes_test(is_admin)
@login_required
def admin_dashboard(request):

    users = User.objects.all()
    total_users = User.objects.count()

    context = {
        'users': users,
        'total_users': total_users,
    }
    return render(request, 'memos/admin_dashboard.html', context)
