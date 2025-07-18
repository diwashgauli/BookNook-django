from django.shortcuts import render
from django.db.models import Q
from django.views.generic import ListView
from .models import Post  # your book model

from django.views.generic import TemplateView
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.views.generic import ListView,CreateView,DeleteView,UpdateView,DetailView
from .models import Post
from booknook.forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class HomeView(ListView):
    model = Post
    template_name = 'book/home.html'
    context_object_name = 'all_books'  

    def get_queryset(self):
       
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        context['trending_books'] = Post.objects.filter(is_trending=True)
        context['popular_books'] = Post.objects.filter(is_popular=True)
        return context




class MyProfileView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'book/my_profile.html' 
    context_object_name = 'posts' 

    def get_queryset(self):
        
        return Post.objects.filter(posted_by=self.request.user).order_by('-created_at')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'book/post_create.html'  # create this template
    success_url = reverse_lazy('my_profile')  # redirect to profile or other page

    def form_valid(self, form):
        form.instance.posted_by = self.request.user  # set the logged-in user as author
        return super().form_valid(form)
    


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'book/post_confirm_delete.html'  # create this template
    success_url = reverse_lazy('my_profile')

    def test_func(self):
        post = self.get_object()
        # Allow delete only if the logged-in user is the owner (posted_by)
        return post.posted_by == self.request.user
    


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'book/post_edit.html'  # create this template
    success_url = reverse_lazy('my_profile')

    def test_func(self):
        post = self.get_object()
        return post.posted_by == self.request.user
    


class PostDetailView(DetailView):
    model = Post
    template_name = 'book/post_detail.html'  # create this template
    context_object_name = 'post'


class SearchView(ListView):
    model = Post
    template_name = 'book/search_results.html'
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(author_name__icontains=query)
            )
        return Post.objects.none()