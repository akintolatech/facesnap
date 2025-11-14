from django.urls import path
from . import views
app_name = 'facesnapper'

urlpatterns = [
    path('', views.onboard  , name='onboard'),
    path('dashboard/', views.dashboard  , name='dashboard'),
    path('student_list/<int:class_id>/', views.student_list  , name='student_list'),
    path('capture/<int:student_id>/', views.capture, name='capture'),
    path('upload_photo/', views.upload_photo, name='upload_photo'),
    path('success/<int:student_id>/', views.upload_success, name='upload_success'),
    path('upload_students/<int:class_id>/', views.upload_students, name='upload_students'),
]