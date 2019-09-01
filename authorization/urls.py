from django.urls import path
from authorization import views

urlpatterns = [
    # path('session1',views.session1),
    # path('session2',views.session2),
    path('authorize',views.authorize)
]
