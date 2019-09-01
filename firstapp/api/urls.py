from django.urls import include, path
from firstapp.authorization.view import views
urlpatterns = [
    path('session/',include('authorization.views.seesion'))
]
