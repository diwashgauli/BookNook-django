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
    path('comment/', views.CommentView.as_view(), name='comment'),
    path('profile/edit/', views.EditProfileView.as_view(), name='edit-profile'),
    path('profile/<str:username>/', views.UserProfileView.as_view(), name='user_profile'),
    path("all-categories/",views.CategoryListView.as_view(),name="all-categories"),
     path('category/<int:category_id>/', views.PostByCategoryView.as_view(), name='post-by-category'),
     path('subscribe/', views.SubscribeView.as_view(), name='subscribe'),
  


      # Home view for /
    # Other routes...
]