from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from . import util
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

import markdown2

import random

from django import forms

class wikiforms(forms.Form):
    title=forms.CharField(label="title",widget=forms.TextInput(attrs={'placeholder':'enter title'}))
    content=forms.CharField(label="content",widget=forms.Textarea(attrs={'placeholder':'enter content here'}))



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
 
def wiki(request,entry):
    return render(request,"encyclopedia/wiki.html",{
        "title":entry,
        "content":markdown2.markdown(util.get_entry(entry))
    })

@login_required(login_url='login')
def newpage(request):
    if request.method=="POST":
        form=wikiforms(request.POST)
        if form.is_valid():
            title=form.cleaned_data["title"]
            content=form.cleaned_data["content"]
            util.save_entry(title,content)
        else:
            return render(request,"encyclopedia/newpage.html",{
            "form":form
        })

    return render(request,"encyclopedia/newpage.html",{
        "form":wikiforms()
    })

def search(request):
    title=request.GET.get('q')
    if util.get_entry(title) is not None:
        return render(request,"encyclopedia/wiki.html",{
        "title":title,
        "content":markdown2.markdown(util.get_entry(title))
        })
    else:
        li=[]
        a=0
        for entry in util.list_entries():
            if title.lower() in entry.lower():
                li.append(entry)
                a=1
        if a==1:
            return render(request,"encyclopedia/notfound.html",{
                "entries": li
            })
        else:
            return render(request,"encyclopedia/notfound.html",{
                "entries": util.list_entries()
            })

def randoms(request):
    entry=random.choice(util.list_entries())
    return render(request,"encyclopedia/wiki.html",{
        "title":entry,
        "content":markdown2.markdown(util.get_entry(entry))
    })

@login_required(login_url='login')
def edit(request,title):
    if request.method=="POST":
        content=request.POST["content"]
        Title=request.POST["title"]
        util.save_entry(Title,content)
        return HttpResponseRedirect(reverse("wiki",args=(Title,)))
    else:
        return render(request,"encyclopedia/edit.html",{
            "content":util.get_entry(title),
            "title":title
        })

def login_wiki(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request,"encyclopedia/login.html",{
                "message":"error in password or username"
            })
    else:
        return render(request,"encyclopedia/login.html")


def logout_wiki(request):
    logout(request)
    return render(request, "encyclopedia/login.html", {
        "message": "Logged out."
    })

def signup(request):
    if request.method=="POST":
        username=request.POST["username"]
        email=request.POST["email"]
        password1=request.POST["password1"]
        password2=request.POST["password2"]
        if password1!=password2:
            return render(request, "encyclopedia/signup.html", {
                "message": "Passwords must match."
            })
        try:
            user=User.objects.create_user(username, email, password1)
            user.save()
        except IntegrityError:
            return render(request, "encyclopedia/signup.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request,"encyclopedia/signup.html")