from django.urls import path
from face_recog import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView,LogoutView
#from django_email_verification import urls as mail_urls
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path('',views.home),
    path('/face',views.mark,name="face"),
    path('/show',views.show,name="show"),
    path('display',views.display_all,name="display"), 
    path('<int:id>',views.play,name="play"), 
]   +static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)