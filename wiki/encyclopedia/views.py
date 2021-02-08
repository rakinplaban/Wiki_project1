from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django import forms
import markdown2
from . import util

class Newform(forms.Form):
    title = forms.CharField(label="Title",widget=forms.TextInput(attrs={
        "class" : "form-control"
    }))
    content = forms.CharField(label="Content",widget=forms.Textarea(attrs={
        "class" : "form-control",
        "cols" : 40
        }))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def newpg(request):
    if request.method == "POST":
        form = Newform(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if(util.get_entry(title) is None):
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse('entry',kwargs={'entry':title}))

            else:
                return render(request, "encyclopedia/newpg.html",{
                    "form" : Newform(),
                    "existing" : True,
                    "entry" : title
                })

        else:
            return render(request, "encyclopedia/newpg.html",{
                    "form" : Newform(),
                    "existing" : False
                })
    return render(request, "encyclopedia/newpg.html", {
        "form" : Newform()
    })