from django.shortcuts import render
from django import forms
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
    return render(request, "encyclopedia/newpg.html", {
        "form" : Newform()
    })