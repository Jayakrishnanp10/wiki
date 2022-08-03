from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>",views.wiki,name="wiki"),
    path("newpage", views.newpage, name="newpage"),
    path("search", views.search, name="search"),
    path("random", views.randoms, name="random"),
    path("edit/<str:title>",views.edit,name="edit"),
    path("login", views.login_wiki, name="login"),
    path("logout", views.logout_wiki, name="logout"),
    path("signup", views.signup, name="signup")
]
