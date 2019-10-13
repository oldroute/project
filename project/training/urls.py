from django.conf.urls import url
from . import views

app_name = 'training'

urlpatterns = [
    url("^solutions/\d+/$", views.solution, name="solution"),
]
