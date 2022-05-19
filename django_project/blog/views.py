from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
posts = [
    {
        'post_author': 'Khair',
        'post_title': 'Is Machine Learning the future ?',
        'post_time': '18/5/2022',
        'content': 'sasgfhjkkkkkkkkkkklkafaf'
    },
    {
        'post_author': 'Ahammed',
        'post_title': 'Data Analyst vs Data Scientist vs Data Engineer',
        'post_time': '22/5/2022',
        'content': 'sasgfhjkkkkkkkkkkklkafaf'
    }
]


def home(request):
    context = {
        'posts':posts
    }
    return render(request, 'blog/home.html', context)

def about (request):
    return render(request, 'blog/about.html', {'title': 'About'})