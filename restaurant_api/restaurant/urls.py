from django.urls import path

from restaurant import views


app_name = 'trainer_api'

urlpatterns = [
    path('create_checks/', views.CreateChecks.as_view(), name='create_checks'),
    path('new_checks/', views.NewChecks.as_view(), name='new_checks'),
    path('check/', views.CheckFile.as_view(), name='check_file'),
]
