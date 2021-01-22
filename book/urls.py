from django.urls import path
from .import views


urlpatterns = [
    path('reviews/', views.review_list, name='review_list'),
    path('', views.allBooks, name='allBooks'),

    path('reviews/<int:pk>', views.review_detail, name='review_detail'),
    path('Book/', views.allBooks, name='allBooks'),

    path('Book/<int:pk>', views.book_detail, name='book_detail'),
    path('Book/<int:pk>/add_review/', views.add_review, name='add_review'),
    
    path('accounts/logout/', views.logout_view, name='logout_view'),
    path('accounts/register/', views.SignUp.as_view(), name='signup'),

    path('recommendation/', views.get_suggestions, name='get_suggestions'),

    path('allbooks/',views.allBooks, name='allBooks'),  
    path('recommendation2/', views.get_suggestions2, name='get_suggestions2'),

    path('select/', views.select, name='select'),
    
]