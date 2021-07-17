from django.urls import path
from needs import views

urlpatterns = [
    path('need/', views.need_list_view),
    path('need/<int:pk>/', views.need_detail_view),
    path('goal/', views.goal_list_view),
    path('goal/<int:pk>/', views.goal_detail_view),
    path('step/', views.step_list_view),
    path('step/<int:pk>/', views.step_detail_view),
    path('iteration/', views.iteration_list_view),
    path('iteration/<int:pk>/', views.iteration_detail_view),
    
]
