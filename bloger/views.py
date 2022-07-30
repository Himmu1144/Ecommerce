from logging import exception
from django.http import HttpResponse
from django.shortcuts import render
from .models import Blogpost

# Create your views here.
def index(request):
    blogs = Blogpost.objects.all()
    return render(request, 'bloger/index.html',{'blogs':blogs})

def blogpost(request, id):
    post = Blogpost.objects.filter(post_id = id)[0]
    last_post = Blogpost.objects.all().last()
    
    try:
        if id == 1 or id == last_post.post_id:
            pass
        else:
            prev_post = Blogpost.objects.filter(post_id=(id-1))[0]
            next_post = Blogpost.objects.filter(post_id=(id+1))[0]

        if id == 1:
            prev_post = Blogpost.objects.filter(post_id=(id+1))[0] 
            next_post = Blogpost.objects.filter(post_id=(id+2))[0]
        elif id == last_post.post_id:
            prev_post = Blogpost.objects.filter(post_id=(id-2))[0] 
            next_post = Blogpost.objects.filter(post_id=(id-1))[0]

    except exception as e:
        pass
    if prev_post and next_post:
        return render(request,'bloger/blogpost.html',{'post':post,'next_post':next_post,'prev_post':prev_post,'last_post':last_post})
    elif prev_post:
        return render(request,'bloger/blogpost.html',{'post':post,'prev_post':prev_post,'last_post':last_post})
    elif next_post:
        return render(request,'bloger/blogpost.html',{'post':post,'next_post':next_post, 'last_post':last_post})
        
    return render(request, 'bloger/blogpost.html',{'post':post,'last_post':last_post})