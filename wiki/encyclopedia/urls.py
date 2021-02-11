from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newpg/",views.newpg, name="newpg"),
    path("wiki/<str:entry>/edit",views.edit, name = "editentry"),
    path("wiki/<str:entry>", views.entry, name="wiki_page"),
    path("pagenotfound/",views.entry,name="pagenotfound"),
    path("search/",views.search,name="search")
]
