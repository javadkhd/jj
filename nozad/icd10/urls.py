from django.urls import path
from . import views


app_name = 'icd10'
urlpatterns = [
    path('col10/', views.col_10, name='col10'),
    path('col11/', views.col_11, name='col11'),
    path('col12/', views.col_12, name='col12'),
    path('col13/', views.col_13, name='col13'),


]
