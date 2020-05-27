### django-media-images :
     #### settings.py :
      MEDIA_URL='/media/'
      MEDIA_ROOT=os.path.join(BASE_DIR, 'media')

     #### Urls.py
       from django.conf.urls.static import static
       urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
       
       
### grabs from database:
  
    ##### views.py:
    from.models import Project
    projects=Project.objects.all()
    return render(request,'pro/home.html',{'projects':projects})
       
     
     
  ### another set of urls
  
    ##### urls.py :
    from django.urls import path,include
        path('blog/', include('blog.urls')),
        
    create urls.py folder into apps  
    
    #####  apps urls.py:
        from django.urls import path
        from . import views
        urlpatterns = [
                path('',views.all_blogs, name='all_blogs'),
              ]

   
 ### create signup form (3.0):
 
 
    ##### urls.py :
          from django.conf.urls import url
          from django.contrib import admin
          from calc import views
          urlpatterns = [
              url(r'^admin/', admin.site.urls),
              url(r'^signup/', views.signupuser , name='signupuser'),
          ]
        
        
    ##### views.py :
           from django.shortcuts import render
           from django.contrib.auth.forms import UserCreationForm

           def signupuser(request):
              return render(request, 'todo/signupuser.html' ,  {'form':UserCreationForm()})
    
    
    ##### signupuser.html :
               {{ form.as_p }}  #as_p makes text as <p>
               
               
               
               
 ### make signup button & user can create account & save them into database  
     ##### create super user for admin by terminal
              python manage.py createsuperuser-> give username,pass 
            
            
     ##### signupuser.html :
     
              <h1>Sign Up</h1>
              <h2>{{ error }}</h2>
              <form method="POST"> #  <!post are using creating new data ->
                {% csrf_token %}   # showing text <p>
                {{ form.as_p }}    #for using submit type button
                <button type="submit">sign Up</button>
              </form>
              
        
    ##### views.py:   
        from django.shortcuts import render
        from django.contrib.auth.forms import UserCreationForm
        from django.contrib.auth.models import User  # User.objects.create_user() -> for using it
        
        def signupuser(request):
            if request.method == 'GET':  # for showing just signup/ page.
                 return render(request, 'todo/signupuser.html' ,  {'form':UserCreationForm()})
                 
             else:                      # for 'POST' ->when some one using 
                                        #signup button for create account  
                                        
                     if request.POST['password1'] == request.POST['password2']: #cheacking password & password confirm field same or not.
                                                                                
                                                                                
                        user=User.objects.create_user(request.POST['username'] , password=request.POST['password1'])#for  making new user object,pass the username & password                                                                                               
                                                                                            
                        user.save()   #save new account into database
                     else:
                     
                        return render(request, 'calc/signupuser.html' ,  {'form':UserCreationForm() , 'error':'password did  not match'})

           
            
   ### cheack user name unique when create account (IntegrityError) :
     ##### views.py:
        
           from django.shortcuts import render
           from django.contrib.auth.forms import UserCreationForm
           from django.contrib.auth.models import User  
           from django.db import IntegrityError
    
         def signupuser(request):
            if request.method == 'GET':  
                 return render(request, 'todo/signupuser.html' ,  {'form':UserCreationForm()})
                 
             else:                                              
                     if request.POST['password1'] == request.POST['password2']:
                        try:    #if user name not registered than try
                           user=User.objects.create_user(request.POST['username'] , password=request.POST['password1'])                                user.save() 
                           
                        except IntegrityError:
                           return render(request, 'todo/signupuser.html' ,  {'form':UserCreationForm() ,'error':'thisusername alredy registered'})
                           
                     else:
                        return render(request, 'todo/signupuser.html' ,  {'form':UserCreationForm() , 'error':'password did not match'})
                        
                        
                        
   ### showing logged into account : 
          ### urls.py :
              urlpatterns = [
                                url(r'^current/', views.currenttodos , name='currenttodos'),
                            ]
                            
   
         ##### views.py:
                from django.shortcuts import render, redirect
                from django.contrib.auth import login
                
                try:
                   user=User.objects.create_user(request.POST['username'] , password=request.POST['password1'])
                   user.save()
                   login(request , user) #after login we have to send them somewhere,making currenttodos page.
                   return redirect('currenttodos') #redirect into currenttodos
                   
                def currenttodos(request):
                   return render(request, 'todo/currenttodos.html' )
                
                
                
                
### show if a user is logged in:
    ##### currenttodos.html:
           {% extends 'todo/base.html' %}
           {% block content %}
              Current
           {% endblock %}
           
     
    #####  base.html :
                {% if user.is_authenticated %} <! cheacked if someone is logged in ->
                Logged in as {{ user.username }}
                <a href="logout">logout</a>
                
                {% else %}
                <a href="logout">Signup</a>
                <a href="logout">login</a>

                {% endif %}
                {% block content %}{% endblock %}
                
                
     ### make this change also in our signup page:
     
           ### signupuser.html:
              {% extends 'calc/base.html' %}
              {% block content %}
              <h1>Sign Up</h1>
              <h2>{{ error }}</h2>
              <form method="POST">  <!post are using creating new data ->
                {% csrf_token %}
                {{ form.as_p }}
              <button type="submit">sign Up</button>
              </form>
              {% endblock %}

    

### logout:
     
     ##### urls.py:
           urlpatterns = [
      path('logout/', views.logoutuser, name='logoutuser'),
    
    ]
    
    
    #####views.py:
      from django.contrib.auth import login, logout    #for account logout 
      
       def logoutuser(request):
           if request.method == 'POST':  # it can kicking user out , because browser are doing this work automaticly, so we logged out if it is post request. in base.html -> <a href="{% url 'logoutuser' %}">LOGOUT</a> -> 'GET' statement
              logout(request)   #() -> pass what things are logged out
              return redirect('home')  # redirect use for go to the another function in views.py, and it's must .
              
           
    ### base.html :
           <a href="{% url 'logoutuser' %}">LOGOUT</a> # now it's GET
           
    
     ### make a home page
     
     ### solve error:  'todo.views.logoutuser didn't return an HttpResponse object'
            error occur because this function has a 'POST' but no action is happend
            
         ##### base.html:
              <form action="{% url 'logoutuser' %}" method="POST"> 
                   {% csrf_token %}
                   <button type="submit">Logout</button>
              </form>
              
      
    
   ### user can login with their existing account:
        
        
      #####urls.py:
         urlpatterns = [
           path('login/', views.loginuser, name='loginuser'),
          ]
           

     #####views.py:
        from django.contrib.auth.forms import  AuthenticationForm
        from django.contrib.auth import authenticate
        
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
                
      
    #####  loginuser.html
       {% extends 'todo/base.html' %}
       {% block content %}
        <h1>Login</h1>
        <h2>{{ error }}</h2>
        <form method="POST">
          {% csrf_token %}
          {{form.as_p}}
          <button type="submit">Login</button>
        </form>
       {% endblock %}
       
       
 
 
### creating models for todo: 
    ##### models.py:
      from django.db import models
      from django.contrib.auth.models import User #for one to many relationship
      class Todo(models.Model): #search django model field
        title = models.CharField(max_length=100)
        memo = models.TextField(blank=True)
        created = models.DateTimeField(auto_now_add=True)
        datecompleted = models.DateTimeField(null=True)
        important =  models.BooleanField(default=False)
        user = models.ForeignKey(User, on_delete=models.CASCADE)#ForeignKey store the relationship between this todo and that.
    #python3 manage.py makemigrations
    #python3 manage.py migrate
       
    #####admin.py:
      from django.contrib import admin
      from .models import Todo
      admin.site.register(Todo)

    ### created field not showing , let's make it clear:
        ##### admin.py:
             from django.contrib import admin
             from .models import Todo
             
            #specifying 'created' as read only file
            class TodoAdmin(admin.ModelAdmin):
               readonly_fields=('created',)
               
            admin.site.register(Todo,TodoAdmin)

      
     

  ### user can now crteate todo object:
       ##### urls.py:
       
           path('create/', views.createtodo, name='createtodo'), 
     
     
      ##### views.py:
      
     def createtodo(request):
         if request.method =='GET':
             return render(request, 'todo/createtodo.html' , {'form':TodoForm()})
         else:
             #we have to get the information from the 'POST' request and connect with our form
             form=TodoForm(request.POST) #whatever they send us like title,memo we are gona pass that into Todoform. and we are collecting this  data in form
             newtodo=form.save(commit=False) # cammit=false stop saving data into database
             #we have to handel which user are saving this data
             newtodo.user=request.user
             newtodo.save()
             return redirect('currenttodos')

           
      ##### forms.py:
      
         from django.forms import ModelForm #TodoForm needs inheret, so we import it
         from .models import Todo
         
         class TodoForm(ModelForm):
          class Meta: #specify what class it is,what model,fields we want ,so we need to use meta class
            model =Todo #specifying the model ,and we need to import from .models import Todo
            fields=['title','memo','important'] #specify what we want
            
         
     ##### createtodo.html:
           {% extends 'todo/base.html' %}
           {% block content %}
            <h1>create</h1>
            <h2>{{ error }}</h2>
            <form method="POST">
              {% csrf_token %}
              {{form.as_p}}
              <button type="submit">Create</button>
            </form>
           {% endblock %}

     
    ### title size is 100 char, so 101 char found error (ValueError).Handel this by try and exception
    
     ##### views.py:
     
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

          
         
     
  ### show user todo list:
  
     ### views.py:
     from .models import Todo # for showing user todo list
     def currenttodos(request):
       todos=Todo.objects.filter(user=request.user)
       return render(request, 'todo/currenttodos.html',{'todos':todos})
       
       
       
       
     ### currenttodos.html:
        {% extends 'todo/base.html' %}
          {% block content %}
          Current lists...
          
          <ul>
            {% for todo in todos %}
            <li>{{ todo.title }} </li>
            {% endfor %}
          </ul>
    
        {% endblock %}

      
     
     
     
 ### if a todo is important show it bold & show the memo
     ##### currentstodo.html:
     {% extends 'todo/base.html' %}
     {% block content %}
      Current lists...

      <ul>
        {% for todo in todos %}
        <li>
          {% if todo.important %}<b>{% endif %}{{ todo.title }} {% if todo.important %}</b>{% endif %}
          {% if todo.memo %}-{{ todo.memo }}{% endif %}
        </li>  <!-- if a todo is important, show bold ,if memo is their show that -->
        {% endfor %}
      </ul>
     {% endblock %}

           
  ### some one able to click this todo, they can edit todo
      ##### showing a particular todo. by entaring url http://127.0.0.1:8000/todo/2
      
     ##### urls.py:
       path('todo/<int:todo_pk>', views.todo, name='view.todo'),#we are going to specifying that we are looking a int
       
       
     #####
      views.py:
        from django.shortcuts import render, redirect,get_object_or_404
        def viewtodo(request,todo_pk):   #todo_pk thats primary key use in urls.py
            todo=get_object_or_404(Todo, pk=todo_pk)#Todo is our model class
            return render(request, 'todo/viewtodo.html' , {'todo':todo})
            
            
            
            
     ##### now create todo link(we can click todo and that todo goes with another page):
        ##### currenttodos.html:
           {% extends 'todo/base.html' %}
          {% block content %}
          Current lists...
          <ul>
            {% for todo in todos %}
            <li>
              <a href="{% url 'viewtodo' todo.id%}">  <!--by default database id.-->
              {% if todo.important %}<b>{% endif %}{{ todo.title }} {% if todo.important %}</b>{% endif %}
              {% if todo.memo %}-{{ todo.memo }}{% endif %}
              </a>
            </li>  <!-- if a todo is important, show bold ,if memo is their show that -->
            {% endfor %}
          </ul>
          {% endblock %}
         
         

    ##### now edit todos:
      ##### views.py:
    def viewtodo(request,todo_pk):   #todo_pk thats primary key use in urls.py
     todo=get_object_or_404(Todo, pk=todo_pk, user=request.user)#Todo is our model class
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


         ##### viewtodo.html
            {% extends 'todo/base.html' %}
            {% block content %}
            {{ error }}
            <form method="POST">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit">save</button>
            </form>
            {% endblock %}

          
           
### complete todo
    ##### urls.py 
          path('todo/<int:todo_pk>/complete', views.completetodo, name='completetodo'),
          
    ##### views.py
        from django.utils import timezone
        
        def currenttodos(request):
           todos=Todo.objects.filter(user=request.user, datecompleted__isnull=True)
           return render(request, 'todo/currenttodos.html',{'todos':todos})
           
        def completetodo(request, todo_pk):
          todo=get_object_or_404(Todo, pk=todo_pk, user=request.user)
          if request.method =='POST':
              todo.datecompleted = timezone.now() #in models.py we take datecompleted=null ,here we give it timezone, so we can understand that it's complete
              todo.save()
              return redirect('currenttodos')

     
 ### deletetodo 
    ##### urls.py
      path('todo/<int:todo_pk>/complete', views.deletetodo, name='deletetodo'),
 
 
 
 
    ##### views.py
     def deletetodo(request, todo_pk):
       todo=get_object_or_404(Todo, pk=todo_pk, user=request.user)
     if request.method =='POST':
        todo.delete()        # it permanently delete from database
        return redirect('currenttodos')

 ### find which todo are done and when
    ##### urls.py:
          path('completed/', views.completedtodos, name='completedtodos'),
          
    ##### views.py:
      def completetodo(request, todo_pk):
        todo=get_object_or_404(Todo, pk=todo_pk, user=request.user)
        if request.method =='POST':
            todo.datecompleted = timezone.now() #in models.py we take datecompleted=null ,here we give it timezone, so we can understand that it's complete
            todo.save()
            return redirect('currenttodos')
            
            
    ##### completedtodos.html:
         {% block content %}
          completed...
          <ul>
            {% for todo in todos %}
            <li>
              <a href="{% url 'viewtodo' todo.id%}">  <!--by default database id.-->
              {% if todo.important %}<b>{% endif %}{{ todo.title }} {% if todo.important %}</b>{% endif %}
              {% if todo.memo %}-{{ todo.memo }}{% endif %}{{ todo.datecompleted|date:'M j Y H:i' }}<!-- it's a fancy bit -->
              </a>
            </li>  <!-- if a todo is important, show bold ,if memo is their show that -->
            {% endfor %}
          </ul>
          {% endblock %}

     
     
  ### login_required:
    from django.contrib.auth.decorators import login_required
    
  ##### views.py
    @login_required
    def loginuser(request):
      pass
      
 ##### settings.py:
    LOGIN_URL = '/login' #it's take the login page its don't work with loginuser.
