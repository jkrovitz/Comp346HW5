from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.dateformat import format

from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .models import Message


''' 
Jeremy Krovitz
Homework 5 
COMP 346 - Internet Computing 

I worked with Luke Brown and Rae Hushion on this assignment.

Assignment Description: 
In this assignment I created a messaging application 
that lets users send messages to each other. 
'''

@login_required
def home(request):
    # This is the home function view. 
    messages = Message.objects.filter(sender=request.user)
    return render(request, 'messenger/home.html', {'messages': Message.objects.all()})

def signup(request):
    # This funtion allows users to create an account if 
    # they do not already have one. 
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
    # This function allows the signed in user to compose a message to
    # any registered user. 
    users = User.objects.all()
    return render(request, 'messenger/message_create.html', {'users': users})

@login_required
def message_save(request):
    #This function saves the sender's message, sends it to the correct
    #receiver and redirects the signed in user to the home page. 
    sender = request.user
    text = request.POST.get('message')
    receiver_username = request.POST.get('recipient')
    receiver = User.objects.get(username=receiver_username)
    if request.POST.get('submit'):
        m = Message(text=text,
                    sent=True,
                    sender=sender,
                    receiver=receiver)
    else:   
        m = Message(text=text,
                    sent=False,
                    sender=sender,
                    receiver=receiver)
    m.save()
    message_id = m.id
    return redirect('/inbox.html')

@login_required
def message_detail(request, id): 
    #This function render's the details page for a particular message. It shows the entire 
    # message that is sent rather than just one line of the message, as is shown in the inbox, 
    #sent messages, and drafts page. 
    message = Message.objects.get(id=id)
    return render(request, 'messenger/message_detail.html', {'message': message})

@login_required
def inbox(request):
    #This is the inbox for each user. Messages get filtered based on 
    #the user who is signed in and is the receiver of the message. 
    filtered_message_objects = Message.objects.filter(receiver=request.user, sent=True)
    return render(request, 'messenger/inbox.html', {'filtered_message_objects': filtered_message_objects})

@login_required
def sent(request):
    #This is the sent box of the signed in user. These are the messages
    #that the signed in user has sent. 
    filtered_message_objects = Message.objects.filter(sender=request.user, sent=True)
    return render(request, 'messenger/sent.html', {'filtered_message_objects': filtered_message_objects})

@login_required
def drafts(request):
    #This function creates the signed-in user's drafts page, where they 
    #can see all messages that they have saved as drafts but have not
    #yet sent. 
    filtered_message_objects = Message.objects.filter(sender=request.user, sent=False)
    return render(request, 'messenger/drafts.html', {'filtered_message_objects': filtered_message_objects})

@login_required
def message_edit(request):
    #This function creates the page where a user edits there message. 
    #The right message is found using its id. 
    users = User.objects.all()
    id = request.POST.get('message_edit')
    message = Message.objects.filter(id=id)
    return render(request, 'messenger/message_edit.html', {'users': users, 'message': message[0]})

@login_required
def message_update(request, message_id):
    #This function updates the the message that was saved as a draft 
    # and if the user chooses to sent the message, sent is set to 
    # true otherwise sent gets set to false.  
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

