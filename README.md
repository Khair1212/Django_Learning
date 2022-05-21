**playlist:** https://www.youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p

# Set up Virtual Environments

* Install the virtual environment Package
  
  ```pip install virtualenv```

* Create the virtual environment 
   
   ```virtualenv ~project name~```

* Activate the virtual environment
    
    ```source ~project name~/bin/activate```  [Mac OS/ Linux] \
    ```~project name~\Scripts\activate``` [Windows]
    
* Deactivate the virtual environment
    
    ```deactivate```


# Lecture 1: Getting Started with Django

* Install Django 
```pip install django```

* Start a Project
```django-admin startproject ~project name~```

* Run server 
```python manage.py runserver```

* Start App
```python manage.py startapp ~appname~```

# Lecture 2: Applications and Routes

* Start an app
```python manage.py startapp firstapp```
* Go to app views to add a new page
```
  from django.http import HttpResponse
  def home(request):
      return HttpResponse("<h1>My Home </h1>")
``` 
     
* Make app url file and add url there

```
  from django.urls import path
  from . import views

  urlpatterns = [
	path('', views.home, name = "blog.home",
  ]
```
* Add app url to main urls file
```
  from django.urls import path, include

  urlpatterns = [
	path('admin/', admin.site.urls,
	path("blog/", include('blog.urls'))
  ]
```


# Lecture 3: Templates


We can't just add bunch of code in the views function. So, we just need to create a temlate and refer that to views. \
First create a templates directory in the app folder. Inside the template folder create a folder with the app name like "blog" in our case. Now inside that folder write down the html files. Now add the app configuration in the settings.py Installed App list . \

```
INSTALLED_APPS = [
	'blog.apps.BlogConfig' [BlogConfig from the apps.py]
	'',
	'',
]
```
* Use the render package 

```
def home(request):
    return render(request, 'blog/home.html')
```

* Render Data from views 

1) Add som data first like a list of dictionary

```posts = [
    {
        'post_author': 'Khair',
        'post_title': 'Is Machine Learning the future ?',
        'post_time': '18/5/2022'
    },
    {
        'post_author': 'Ahammed',
       'post_title': 'Data Analyst vs Data Scientist vs Data Engineer',
        'post_time': '22/5/2022'
    }
]
```
* Add that dictionary in the render function

```
def home(request):
    context = {
        'posts':posts
    }
    return render(request, 'blog/home.html', context)
```

* Use Ginger to fetch the data in the template 

```
{% for post in posts %}
    <h1>{{post.post_title}}</h1>
    <p>By {{post.post_author}} on {{post.post_time}}</p>
{% endfor %}
```
* Create a base html page 

```
<!DOCTYPE html>
<html>
   <head>
   </head>

    <body>
   	(% block content %} {% endblock %}
    </body
</html>
```
* inherit the base html

```
{% extends blog\base.html %}
{% block content %}

	\\
{% endblock content %}
```
** Adding static Folder 

add a folder name static and then 'blog' in the static folder [same as app name]. Add css and other static filer there

```
{% load static %}
<link rel = "stylesheet", type = "text/css" href = " {% static 'blog/main.css' %}">
```

* Make the links dynamic using url
```href = '{% url 'blog-home[name]' %}'```

# Lecture 4: Admin Panel

```
python manage.py createsuperuser [this will raise error as we haven't migrate the database yet] 

python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser
```

type username, email and password and log in to the admin panel 

# Lecture 5: Database and Migrations

Django already has a built-in authentication system and a user model files
* create the very first database [Post table]

models.py
```
from django.utils import timezone
from django.contrib.auth.models import User
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
```
* In order to have some descriptive Post model let's add a __str__ function

```
def __str__(self):
	return self.title 
```

* Make migrations of the new Post model 

```
python manage.py makemigrations
```

* Create the sql file that is gonna generate 

```
python manage.py sqlmigrate blog 0001   <!--0001-migration number-->
```

* Migrate the model

```
python manage.py migrate
```

* Let's work with the model interactively

```
python maange.py shell

<!--Interactive Code-->

from blog.models import Post  <!--import Post model-->
from django.contrib.auth.models import User <!--import User model-->
User.objects.all() <!--Get all posts -->
User.objects.first() 
User.objects.filter(username = 'khair1212') 
User.objects.filter(username = 'khair1212').first()
user = User.objects.filter(username = 'khair1212').first()
user.id
user.pk
User.objects.get(id=1) <!--Get user of specific id-->

Post.objects.all()
post_1 = Post(title= "Blog_1", content = "First Blog Post", author = user) <!-- user ~ variable that we created earlier-->
post_1.save() <!--save the post to migrate in the Model-->

 
Post.objects.all()
post = Post.objects.first()
post.date_posted
post.content
post.author 


user.post_set.all()
user.post_set.create(title = "Blog 2", content = "Second Blog Content!")  <!-- create post without specifying author-->
```

* Make changes to views file to get the data from the Post model 

```
from .models import Post

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)
```

* Format the date 
home.html 
```
 <small class="text-muted">{{ post.date_posted | date:"F d, Y"}}</small>
```

* Register the model to the admin panel 
admin.py 
```
from .model import Post

admin.site.register(Post)
```


# Lecture 6: User Registration 

* Create a new user app 

`python manage.py startapp register`

* Setting up in the installed app 
django_project[settings.py]
```
INSTALLED_APPS = [
    'blog.apps.BlogConfig',
    'users.apps.UsersConfig',
]
```
* Add some views functions
```
from django.shortcuts import render 
from django.contrib.auth.forms import UserCreationForm

def register(request):
	form = UserCreationForm()
	return render(request, 'users/register.html', {'form': form})
```
