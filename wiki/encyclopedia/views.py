from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django import forms
from markdown2 import Markdown
import secrets
from . import util

class Newform(forms.Form):
    title = forms.CharField(label="Title",widget=forms.TextInput(attrs={
        "class" : "form-control"
    }))
    content = forms.CharField(label="Content",widget=forms.Textarea(attrs={
        "class" : "form-control",
        "cols" : 40
        }))
    edit =  forms.BooleanField(initial=False,widget=forms.HiddenInput(),required=False)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#def title_loader(request,title):
#    return 

def entry(request,entry):
    markdowner = Markdown()
    getentry = util.get_entry(entry)
    if getentry is None:
        return render(request,"encyclopedia/pagenotfound.html",{
            "entryTitle" : entry
        })
    else:
        return render(request,"encyclopedia/entry.html",{
            "entry" : markdowner.convert(getentry),
            "entryTitle" : entry
        })

def edit(request,entry):
    entrypage = util.get_entry(entry)
    # a condition has been removed
    form = Newform()
    form.fields["title"].initial = entry
    form.fields["title"].widget = forms.HiddenInput()
    form.fields["content"].initial = entrypage
    form.fields["edit"].initial = True
    return render(request,"encyclopedia/newpg.html",{
        "form" : form,
        "edit" : form.fields["edit"].initial,
        "entryTitle": form.fields["title"].initial
    })

def newpg(request):
    if request.method == "POST":
        form = Newform(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if(util.get_entry(title) is None or form.cleaned_data["edit"] is True):
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse("str:entry",kwargs={'entry':title}))

            else:
                return HttpResponse("<h1 style=\"color:red\">This content already exists!</h1>")

        else:
            return render(request, "encyclopedia/newpg.html",{
                    "form" : form,
                    "existing" : False
                })
    return render(request, "encyclopedia/newpg.html", {
        "form" : Newform(),
        "existing" : False
    })

def random(request):
    entries =  util.list_entries()
    randomchoose = secrets.choice(entries)
    return HttpResponseRedirect(reverse("entry",kwargs={'entry': randomchoose}))


def search(request):
    value = request.GET.get('q','')
    if(util.get_entry(value) is not None):
        return HttpResponseRedirect(reverse('entry',kwargs={'entry':value}))

    else:
        substreng = []
        for entry in util.list_entries():
            if value.upper() in entry.upper():
                substreng.append(entry)

        return render(request,"encyclopedia/index.html",{
            "entries" : substreng,
            "search" : True,
            "value" : value
        })

        