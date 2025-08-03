from django.urls import path,include
from . import views


urlpatterns = [
        path('', views.navbar,name='navbar'),
        path('login/', views.login,name='login'),
        path('registration/', views.registration,name='registration'),
        path('admin_login/', views.admin_login,name='admin_login'),
        path('admin_registration/', views.admin_registration,name='admin_registration'),
        path('about/', views.about,name='about'),
        path('contact/', views.contact,name='contact'),
        path('logout/', views.logout,name='logout'),
        path('admin_logout/', views.admin_logout,name='admin_logout'),
        path('userhome/', views.userhome,name='userhome'),
        # path('predict/', views.predict,name='predict'),
        # path('detect/', views.detect, name='detect'),
        path('admin_home/', views.admin_home,name='admin_home'),
        path('upload_video/', views.upload_video, name='upload_video'),  # Adjust the URL path as needed
        path('view_user/',views.view_user, name='view_user'),
        path('video_feed/', views.video_feed, name='video_feed'),
        path('run_detection/', views.run_detection, name='run_detection'),

]
