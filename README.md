
**playlist:** https://www.youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p

# 1. Set up Virtual Environments


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
* Create the UserCreationForm and define the register function
users[views.py]
```
from django.shortcuts import render 
from django.contrib.auth.forms import UserCreationForm

def register(request):
	form = UserCreationForm()
	return render(request, 'users/register.html', {'form': form})
```
* create templates dir with users subdir and add register.html file 
users/templates/users[register.html]
```
{% extends "blog/base.html" %}
{% block content %}
	<div>
		<form method = "POST">
			{% csrf_token %} 
			
			<fieldset class= "form-group">
				<legend class = "border-bottom mb-4">Join Today</legend>
				{{form}} 
			</fieldset> 
			<div class = "form-group"> 
				<button class = "btn btn-outline-info" type = "submit">Sign Up</button> 
			</div>
		</form>
		<div class = "border-top pt-3">
			<small class = "text-muted">
				Already Have an Account ? <a class = "ml-2" href = "#"> Sign In </a>
			</small>
		</div>
	</div>
{% endblock content%}
```

* Create an URL Pattern, we will do that now directly in the admin's urls.py file
django_project[urls.py]
```
django_project [urls.py]
from users import views as user_views
urlpatterns = [
	path('register/', user_views.register, name = 'register'),
]
```
* Validate form, print success message and redirect to home
users[views.py]
```
from django.shortcuts import render, redirect 
from django.contrib import messages 
from django.contrib.auth.forms import UserCreationForm

def register(request):
   if request.method == 'POST' : 
 
	form = UserCreationForm(request.POST) 
	if form.is_valid(): 
		form.save() 
		username = form.cleaned_data.get('username') 
		messages.success(request, f'Account created for {username}!') 
		return redirect ('blog-home') 

   else:
	form = UserCreationForm()

   return render(request, 'users/register.html', {'form': form})
```
* Print message in the base.html. Add codes before the block content  
blog[base.py] 

```
{% if messages %} 
	{% for message in messages %} 
		<div class = 'alert alert-{{message.tags}}'> 
			{{ message }} 
		</div 
	{% endfor%} 
{% endif %} 
{% block content %} {% endblock %} 
```
* Let's add some more field in the form. We need more fields usually. First create a new form that inherits the UserCreationfForm. Let's create a forms.py file
users[forms.py]
```
from django import forms  
from django.contrib.auth.models import User
from django.contrib.auth.models import UserCreationForm

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField(required = True)  <!-- Extra added field -->
	
	class Meta:     <!--Meta gives us a nested namespace for configurations and keeps the configurations in one place-->
		model = User     <!--set the model with whom the form will interact with-->
		fields = ['username', 'email', 'password1', 'password2']   <!-- Specigying the fields of the form -->
```

* Let's just use this new form in the views [import the new form and use the instance of it ]

```
from .forms import UserRegisterForm  [**]
from django.shortcuts import render, redirect 
from django.contrib import messages 
 
def register(request):
   if request.method == 'POST' : 
 
	form = UserRegisterForm(request.POST)  [**]
	if form.is_valid(): 
		form.save() 
		username = form.cleaned_data.get('username') 
		messages.success(request, f'Account created for {username}!') 
		return redirect ('blog-home') 

   else:
	form = UserRegisterForm() [**]

   return render(request, 'users/register.html', {'form': form})
```
* Let's make the form llok bit preetier. We're going to use a third party application called Crispy-forms

-- Install crispy-forms
`pip install django-crispy-forms`

-- Add to the installed apps 
```
INSTALLED_APPS = [
    'blog.apps.BlogConfig',
    'users.apps.UsersConfig',
    'crispy-forms'
]
```
--tell crispy form which css-framework it's going to use and add in the end of the file
```
CRISPY_TEMPLATE_PACK = 'bootstrap4' 
```

* Now load the crispy-forms in the register.html and change them accordingly [Affccted codes are indicated with [**]]

```
{% extends "blog/base.html" %}
{% load crispy_forms_tags %}  [**]
{% block content %}
	<div>
		<form method = "POST">
			{% csrf_token %} 

			<fieldset class= "form-group">
				<legend class = "border-bottom mb-4">Join Today</legend>
				   {{form|crispy}} [**]
			</fieldset> 
			<div class = "form-group"> 
				<button class = "btn btn-outline-info" type = "submit">Sign Up</button> 
			</div>
		</form>
		<div class = "border-top pt-3">
			<small class = "text-muted">
				Already Have an Account ? <a class = "ml-2" href = "#"> Sign In </a>
			</small>
		</div>
	</div>
{% endblock content%}
```


# Lecture 7: Login and Logout system 

* Using the default login views (Add urls)
django_projects: urls.py 

```
from django.contrib.auth import views as auth_views
 
urlpatterns = [
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

]
```
* Create login into the users template
users/templates/users:login.html
```
{% extends 'blog\base.html '%}
{% load crispy_forms_tags %}
{% block content %}
    <div class="content-section">
        <form method = 'POST'>
            {% csrf_token %}
            <fieldset class="form-group">
                <legend class="border-bottom mb-4"> Log In</legend>
                {{ form|crispy }}
            </fieldset>
            <div class = 'form-group'>
                <button class="btn btn-outline-info" type = 'submit'>Login</button>
            </div>
        </form>
        <div class="border-top pt-3">
            <small class="text-muted">
                Don't have an account? <a class="ml-2" href="{% url 'register' %}">Sign Up</a>
            </small>
        </div>
    </div>

{% endblock content %}
```
* Login submit is looking for a profile route. We need to specify the profile route at the bottom of settings.py
django_projects: settings.py 

```
LOGIN_REDIRECT_URL = 'blog-home'
```

* Edit the logout page
users/templates/users:logout.html
```
{% extends 'blog\base.html '%}
{% block content %}
        <h2>You've been logged out!</h2>
        <div class="border-top pt-3">
            <small class="text-muted">
               <a class="ml-2" href="{% url 'login' %}">Log In Again</a>
            </small>
        </div>

{% endblock content %}
```
* Change the navigation bar to dynamically change with the logout and logout
blogs:base.html

```
<!-- Navbar Right Side -->
            <div class="navbar-nav">
                {% if user.is_authenticated %}
                    <a class="nav-item nav-link" href="{% url 'profile' %}">Profile</a>
                    <a class="nav-item nav-link" href="{% url 'logout' %}">Logout</a>
                {% else %}
                    <a class="nav-item nav-link" href="{% url 'login' %}">Login</a>
                     <a class="nav-item nav-link" href="{% url 'register' %}">Register</a>
                {% endif %}
            </div>
```

* Create user's profile 
users: views.py

```
def profile(request):
    return  render(request, 'users/profile.html') 
```

* create the profile.html page
users/templates/users: profile.html

```
{% extends 'blog\base.html '%}
{% load crispy_forms_tags %}
{% block content %}
    <h1> {{user.username}}</h1>

{% endblock content %}
```
* create the url
django_projects: urls.py
```
urlpatterns = [
    path('profile/', user_views.profile, name='profile'),
]
```
* Add on the navigation bar also 
```
{% if user.is_authenticated %}
           <a class="nav-item nav-link" href="{% url 'profile' %}">Profile</a>
           <a class="nav-item nav-link" href="{% url 'logout' %}">Logout</a>
```

* Create Restrictions on accessing profile page 
users: views.py 
```
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return  render(request, 'users/profile.html')
```

* Set the default login location 
```
LOGIN_URL = 'login' 
```

# Lecture 8: User Profile and Picture 

* Add a new Profile model
users: models.model
```
from django.contrib.auth.models import User


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	image = models.ImageField(default = 'default.jpg', upload_to = 'profile_pics')

	def __str__(self):
		return f'{self.user.username} Profile'
```

* Make migrations of the newly created model 

`python manage.py makemigrations`
`python manage.py migrate`

* Register the model
users:Admin.py
```
from .models import Profile

admin.site.register(Profile)
```
* Now the Profile model will create a folder called profile_pics in root directory. But we want to change the root directory as multiple Model can create a lot of folders in the root directory. Let's change the root directory to Media and also change the url.  
django_project: settings.py

```
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
```

* Display all the things into the Profile page. Edit the profile page 
users:profile.html
```
{% extends 'blog\base.html '%}
{% load crispy_forms_tags %}
{% block content %}
    <h1> {{user.username}}</h1>
     <div class="content-section">
         <div class="media">
             <img class="rounded-circle account-img" src = "{{ user.profile.img.url }}">
             <div class="media-body">
                 <h2 class="account-heading"> {{ user.username }} </h2>
                 <p class="text-secondary">{{ user.email }}</p>
             </div>
         </div>
         <!-- FROM HERE-->
     </div>

{% endblock content %}
```

* Serving files uploaded by a user during development 

```
from django.conf import settings
from django.conf.urls.static import static


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
```

Now Profile Pciture Should be Visible 

* Now we automatically want to add a profile while a user sign up 

* Create a signals.py file into the users app and write the codes

```
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender = User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
```

* Now we need to import our signals into the ready function of the users.app.py file 
```
class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    
    def ready(self):
        import ysers.signals 
```

# Lecture 9: Update User Profile

* Add forms to update
users: forms.py
```
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
```
* Add forms to the profile view 
users:views.py
```
from .forms import UserUpdateForm, ProfileUpdateForm

@login_required
def profile(request):
    u_form = UserUpdateForm()
    p_form = ProfileUpdateForm()
    
    context = {
        'u_form':u_form,
        'p_form': p_form
    }
    
    return  render(request, 'users/profile.html', context)
```

* Change the profile.html file 
users/templates/users: profile.html
```
         <form method = 'POST' enctype="multipart/form-data">
            {% csrf_token %}
            <fieldset class="form-group">
                <legend class="border-bottom mb-4"> Profile Info</legend>
                {{ u_form|crispy }}
                {{ p_form|crispy }}
            </fieldset>
            <div class = 'form-group'>
                <button class="btn btn-outline-info" type = 'submit'>Update</button>
            </div>
        </form>
```

* Forms should be filled in with the current user information
users: views.py
```
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form':u_form,
        'p_form': p_form
    }

    return  render(request, 'users/profile.html', context)
```

* Image Resize (Override the profile model)
users:models.py
```
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height>300 or img.width>300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
 ```
* Let's modify the blog views with the profile picture 
```
<article class="media content-section">
            <img class="rounded-circle article-img" src="{{post.author.profile.image.url}}">
```


# Lecture 10: Create, Update and Delete Posts

* Make the home as a list view 

```
from django.views.generic import ListView

class PostListView(ListView):
    model = Post
```
* Change urls.py 

```
from .views import PostListView
urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'), 
]
```
* This will looking for a template with a naming convention <app>/<model>_<viewtype>.html by default. So, change the template that it is looking for. 
blog:views.py

```
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html 
    context_object_name = 'posts'
```
* Order the post new to old 
blog: views.py
```
class PostListView(ListView):
    ordering =  ['-date_posted']
```
* Create Individual post Detail View 
blog: views.py
```
from django.views.generic import DetailView

class PostDetailView(DetailView):
    model = Post
```
* Make the url path (<pk> for having unique path for each individual element and specify the datatyp if we know it)
blogs: views.html
```
from .views import  PostDetailView

urlpatterns = [
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
]
```
* Create the conventional <app>/<model>_<viewtype>.html> file, post_detail.html in this case and change the instance name to be object as per the convention
blog/templates/blog: post_detail.html
```
{% extends 'blog\base.html' %}
{% block content %}
    <article class="media content-section">
        <img class="rounded-circle article-img" src="{{object.author.profile.image.url}}">
      <div class="media-body">
        <div class="article-metadata">
          <a class="mr-2" href="#">{{ object.author }}</a>
          <small class="text-muted">{{ object.date_posted |date:"F d, Y"}}</small>
        </div>
        <h2 class="article-title">{{ object.title }}</h2>
          <p class="article-content"> {{object.content}}</p>

      </div>
    </article>
{% endblock content %}
```
* Active the Home Blog links
blog/templates/blog: home.html
```
<h2><a class="article-title" href="{% url 'post-detail' post.id %}">{{ post.title }}</a></h2>
```

**-------------- Create -------------**
	
* Add a create view to create a new blog 
blogs:views.py
	
```
from .views import PostCreateView

class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content']
```

blogs:urls.py

```
from .views import PostCreateView
path('post/new/', PostCreateView.as_view(), name='post-create'),
```
blogs:post_form.html
	
```
{% extends 'blog\base.html '%}
{% load crispy_forms_tags %}
{% block content %}
    <div class="content-section">
        <form method = 'POST'>
            {% csrf_token %}
            <fieldset class="form-group">
                <legend class="border-bottom mb-4"> Blog Post</legend>
                {{ form|crispy }}
            </fieldset>
            <div class = 'form-group'>
                <button class="btn btn-outline-info" type = 'submit'>Post</button>
            </div>
        </form>
    </div>

{% endblock content %}
```
* Now only a authenticated user can post a blog. So, we need to haave the user id. Let's validate the form and get the user id
```
class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
```
* Redirect URL error resolve once we create a post 
blog: models.py

```
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
```
	
* Restrict unauthorized people from addidng post. For the class-based view we add mixins 
blog: views.py
	
```
from django.contrib.auth.mixins import LoginRequiredMixin

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
```
**--------------- Update ----------------**
	
* Post Update
blogs:views.py

```
from .views import PostUpdateView

class PostUpdateView(LoginRequiredMixin, UpdateView): 
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
```
blogs:urls.py
```
from .views import PostUpdateView
path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
```
* Check the author of the post who is trying to update
	
```
from django.contrib.auth.mixins import UserPassesTestMixin


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
```

** ---------------- Delete ----------------**

* Post Delete 
blogs:views.py
```
from .views import PostDeleteView

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/blog/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
```
blogs:urls.py
```
from .views import PostDeleteView

path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
```


* Add the conventional html file post_confirm_delete.html
blog/template/blog/post_confirm_delete.html
```
{% extends 'blog\base.html '%}

{% block content %}
    <div class="content-section">
        <form method = 'POST'>
            {% csrf_token %}
            <fieldset class="form-group">
                <legend class="border-bottom mb-4"> Delete Post</legend>
                <h2> Are you sure you want to delete the post "{{ object.title }}"</h2>
            </fieldset>
            <div class = 'form-group'>
                <button class="btn btn-outline-danger" type = 'submit'>Yes, Delete</button>
                <a class="btn btn-outline-secondary" href="{% url 'post-detail' object.id %}">Cancel</a>
            </div>
        </form>
    </div>

{% endblock content %}
```
*Let's now update the interface to create, update, edit and delete 
blog/templates/blog: base.html 

```
<!-- Navigation -->

<div class="navbar-nav">
     {% if user.is_authenticated %}
           <a class="nav-item nav-link" href="{% url 'post-create' %}">New Post</a>
```                   
blog/templates/blog: post-detail.html 
```
<div class="media-body">
        <div class="article-metadata">
          <a class="mr-2" href="#">{{ object.author }}</a>
          <small class="text-muted">{{ object.date_posted |date:"F d, Y"}}</small>
        </div>
          {% if object.author == user %}
                <a class="btn btn-secondary btn-sm mt-1 mb-1" href="{% url 'post-update' object.id %}">Update</a>
                <a class="btn btn-danger btn-sm mt-1 mb-1" href="{% url 'post-delete' object.id %}">Delete</a>
          {%  endif %}
        <h2 class="article-title">{{ object.title }}</h2>
          <p class="article-content"> {{object.content}}</p>

</div>
```	

# Lecture 11: Pagination
	
* Add some dummy posts [json file] and add them using a script 

`import json`
`from blog.models import post`

`with open('post.json') as f:
    posts_json = json.load(f)`
    
`for post in posts_json:
    post = Post(title = post['title'], content = post['content'], author_id = post['user_id'])
    post.save()`


* Add paginator to views
blog: views.py

class PostListView(ListView):
 
    paginate_by = 5

* Create the pagination logics in the Home page
blog/templates/blog: home.html

{% if is_paginated %}

        {% if page_obj.has_previous %}
            <a class="btn btn-outline-info mb-4" href="?page=1">First</a>
            <a class="btn btn-outline-info mb-4" href="?page={{ page_obj.previous_page_number }}">Previous</a>
        {% endif %}

        {% for num in page_obj.paginator.page_range %}
            {% if page_obj.number == num %}
                <a class="btn btn-info mb-4" href="?page={{ num }}">{{ num }}</a>
            {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
                <a class="btn btn-outline-info mb-4" href="?page={{ num }}">{{ num }}</a>
            {% endif %}
        {% endfor %}

        {% if page_obj.has_next %}
            <a class="btn btn-outline-info mb-4" href="?page={{ page_obj.next_page_number }}"> Next </a>
            <a class="btn btn-outline-info mb-4" href="?page={{ page_obj.paginator.num_pages }}">Last</a>
        {% endif %}

 {% endif %}
