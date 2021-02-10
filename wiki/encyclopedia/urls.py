from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newpg/",views.newpg, name="newpg"),
    path("wiki/<str:entry>/edit",views.newpg, name = "editentry"),
    path("wiki/<str:entry>", views.retrieve_content, name="wiki_page"),
    path("pagenotfound/",views.retrieve_content,name="pagenotfound")
]
