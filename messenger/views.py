from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.dateformat import format

from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .models import Message


@login_required
def home(request):
    messages = Message.objects.filter(sender=request.user)
    return render(request, 'messenger/home.html', {'messages': Message.objects.all()})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'messenger/signup.html', {'form': form})

@login_required
def message_create(request):
    users = User.objects.all()
    return render(request, 'messenger/message_create.html', {'users': users})

@login_required
def message_save(request):
    sender = request.user
    text = request.POST.get('message')
    receiver_username = request.POST.get('recipient')
    receiver = User.objects.get(username=receiver_username)
    if request.POST.get('submit'):
        m = Message(text=text,
                    sent=True,
                    sender=sender,
                    receiver=receiver)
    else:   # elif request.POST.get('save')
        m = Message(text=text,
                    sent=False,
                    sender=sender,
                    receiver=receiver)
    m.save()
    message_id = m.id
    print("This is the message id: ")
    
    print( message_id )

    return redirect('/inbox.html')

@login_required
def message_update(request, message_id):
    current_message = Message.objects.filter(id=message_id)[0]
    current_message.sender = request.user
    current_message.text = request.POST.get('message')
    receiver_username = request.POST.get('recipient')
    current_message.receiver = User.objects.get(username=receiver_username)
    if request.POST.get('submit'):
        current_message.sent = True; 
    else:   
        current_message.sent = False; 
    current_message.save()

    return redirect('/inbox.html')

@login_required
def sent(request):
    filtered_message_objects = Message.objects.filter(sender=request.user, sent=True)
    return render(request, 'messenger/sent.html', {'filtered_message_objects': filtered_message_objects})

@login_required
def inbox(request):
    filtered_message_objects = Message.objects.filter(receiver=request.user, sent=True)
    return render(request, 'messenger/inbox.html', {'filtered_message_objects': filtered_message_objects})

@login_required
def drafts(request):
    filtered_message_objects = Message.objects.filter(sender=request.user, sent=False)
    for draft in filtered_message_objects:
        print(draft)
    return render(request, 'messenger/drafts.html', {'filtered_message_objects': filtered_message_objects})

@login_required
def message_edit(request):
    users = User.objects.all()
    id = request.POST.get('message_edit')
    message = Message.objects.filter(id=id)
    return render(request, 'messenger/message_edit.html', {'users': users, 'message': message[0]})


@login_required
def message_detail(request, id): 
    message = Message.objects.get(id=id)
    return render(request, 'messenger/message_detail.html', {'message': message})


