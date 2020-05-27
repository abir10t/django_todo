from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate#for account logout
from .forms import TodoForm
from .models import Todo # for showing user todo list
from django.utils import timezone
from django.contrib.auth.decorators import login_required #need to login for speacific link
def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method =='GET':
       return render(request, 'todo/signupuser.html' , {'form':UserCreationForm()})

    else:
        if request.POST['password1'] == request.POST['password2']:

            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')

            except 	IntegrityError:
                return render(request, 'todo/signupuser.html' , {'form':UserCreationForm(), 'error':'username already taken'})
        else:
            return render(request, 'todo/signupuser.html' , {'form':UserCreationForm(), 'error':'password did not match'})
@login_required
def currenttodos(request):
     todos=Todo.objects.filter(user=request.user, datecompleted__isnull=True)
     return render(request, 'todo/currenttodos.html',{'todos':todos})
@login_required
def completedtodos(request):
     todos=Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted') #order_by('-datecompleted') for sow date from reverse
     return render(request, 'todo/completedtodos.html',{'todos':todos})


@login_required
def logoutuser(request):
    if request.method == 'POST':  # it can kicking user out , because browser are doing this work automaticly, so we logged out if it is post request. in base.html -> <a href="{% url 'logoutuser' %}">LOGOUT</a> -> 'GET' statement
           logout(request)   #() -> pass what things are logged out
           return redirect('home')  # redirect use for go to the another function in views.py .


def loginuser(request):
      if request.method =='GET':
          return render(request, 'todo/loginuser.html' , {'form':AuthenticationForm()})

      else:
         user=authenticate(request, username=request.POST['username'] ,password=request.POST['password'])
         if user is None:
              return render(request, 'todo/loginuser.html' , {'form':AuthenticationForm(),'error':'username or password did not match'})
         else:
              login(request, user)
              return redirect('currenttodos')
@login_required
def createtodo(request):
       if request.method =='GET':
           return render(request, 'todo/createtodo.html' , {'form':TodoForm()})
       else:
        try:
           #we have to get the information from the 'POST' request and connect with our form
           form=TodoForm(request.POST) #whatever they send us like title,memo we are gona pass that into Todoform. and we are collecting this  data in form
           newtodo=form.save(commit=False) # cammit=false stop saving data into database
           #we have to handel which user are saving this data
           newtodo.user=request.user
           newtodo.save()
           return redirect('currenttodos')

        except ValueError:
            return render(request, 'todo/createtodo.html' , {'form':TodoForm(),'error':'Bad data passed in. T'})

@login_required
def viewtodo(request,todo_pk):   #todo_pk thats primary key use in urls.py
     todo=get_object_or_404(Todo, pk=todo_pk, user=request.user)#Todo is our model class,(user=request.user) ->matching user
     if request.method =='GET':
      form=TodoForm(instance=todo) #open with whats value are in the form now
      return render(request, 'todo/viewtodo.html' , {'todo':todo,'form':form})
     else:
         try:
           form=TodoForm(request.POST,instance=todo) # for saving with new data , instance=todo->that means we are just editing existence things.
           form.save()
           return redirect('currenttodos')
         except ValueError:
             return render(request, 'todo/viewtodo.html' , {'todo':todo,'form':form,'error':'bad info'})
@login_required
def completetodo(request, todo_pk):
    todo=get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method =='POST':
        todo.datecompleted = timezone.now() #in models.py we take datecompleted=null ,here we give it timezone, so we can understand that it's complete
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk):
    todo=get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method =='POST':
        todo.delete()        # it permanently delete from database
        return redirect('currenttodos')
