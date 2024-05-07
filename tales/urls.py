from django.urls import path
from . import views

urlpatterns = [
    path('', views.tale_list, name='tale_list'),
    path('tale/<int:pk>/', views.tale_detail, name='tale_detail'),
    path('tale/new/', views.tale_new, name='tale_new'),
    path('tale/<int:pk>/edit/', views.tale_edit, name='tale_edit'),
    path('tale/<int:pk>/delete/', views.tale_delete, name='tale_delete'),
    path('tale/<int:tale_id>/questions/new/', views.question_new, name='question_new'),
    path('questions/<int:pk>/edit/', views.question_edit, name='question_edit'),
    path('questions/<int:pk>/delete/', views.question_delete, name='question_delete'),
    # urls.py
    path('tale/<int:tale_id>/generate_question/', views.generate_question, name='generate_question'),

]
