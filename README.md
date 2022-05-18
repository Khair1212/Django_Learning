**playlist:** https://www.youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p

# Lecture 1: Applications and Routes

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
