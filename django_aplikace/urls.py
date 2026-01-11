from django.urls import path
from . import views

urlpatterns = [
    path("", views.prihlaseni, name="prihlaseni"),
    path("kviz/", views.kviz, name="kviz"),
    path("hotovo/", views.hotovo, name="hotovo"),

    path("ucitel/prihlaseni/", views.ucitel_prihlaseni, name="ucitel_prihlaseni"),
    path("ucitel/odhlasit/", views.ucitel_odhlasit, name="ucitel_odhlasit"),

    path("ucitel/", views.ucitel, name="ucitel"),
    path("ucitel/vymazat/", views.vymazat_vysledky, name="vymazat_vysledky"),
]
