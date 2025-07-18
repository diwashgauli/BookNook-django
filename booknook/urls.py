from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('my-profile/', views.MyProfileView.as_view(), name='my_profile'),
    path('books/create/', views.PostCreateView.as_view(), name='add_book'),
    path('books/<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete_post'),
    path('books/<int:pk>/edit/', views.PostUpdateView.as_view(), name='edit_post'),
    path('books/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('search/', views.BookSearchView.as_view(), name='book_search'),


      # Home view for /
    # Other routes...
]