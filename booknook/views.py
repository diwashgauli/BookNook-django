from django.shortcuts import render, redirect
from django.db.models import Q
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView, TemplateView
from django.views import View
from django.core.paginator import Paginator, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Post, Comment, Category
from .forms import PostForm, CommentForm, SubscriberForm, EditProfileForm


class HomeView(ListView):
    model = Post
    template_name = 'book/home.html'
    context_object_name = 'all_books'
    paginate_by = 3

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
    template_name = 'book/post_create.html'
    success_url = reverse_lazy('my_profile')

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'book/post_confirm_delete.html'
    success_url = reverse_lazy('my_profile')

    def test_func(self):
        post = self.get_object()
        return post.posted_by == self.request.user


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'book/post_edit.html'
    success_url = reverse_lazy('my_profile')

    def test_func(self):
        post = self.get_object()
        return post.posted_by == self.request.user


class PostDetailView(DetailView):
    model = Post
    template_name = 'book/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['comments'] = Comment.objects.filter(post=post).order_by('-created_at')
        return context


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


class BookSearchView(View):
    template_name = "book/search_results.html"

    def get(self, request, *args, **kwargs):
        query = request.GET.get("query", "")
        book_list = Post.objects.filter(
            Q(title__icontains=query) | Q(author_name__icontains=query)
        ).order_by("-created_at")

        page = request.GET.get("page", 1)
        paginate_by = 2
        paginator = Paginator(book_list, paginate_by)

        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
        except:
            books = paginator.page(paginator.num_pages)

        trending_books = Post.objects.filter(is_trending=True).order_by("-created_at")[:5]
        popular_books = Post.objects.filter(is_popular=True).order_by("-created_at")[:5]

        return render(
            request,
            self.template_name,
            {
                "page_obj": books,
                "query": query,
                "trending_books": trending_books,
                "popular_books": popular_books,
            },
        )


class CommentView(View):
    def post(self, request, *args, **kwargs):
        post_id = request.POST["post"]
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post_id = post_id
            comment.save()
            return redirect("post_detail", post_id)
        else:
            post = Post.objects.get(pk=post_id)
            popular_posts = Post.objects.filter(published_at__isnull=False, status="active").order_by("-published_at")[:5]
            trending_posts = Post.objects.filter(published_at__isnull=False, status="active").order_by("-views")[:5]

            return render(
                request,
                "book/post_detail.html",
                {
                    "post": post,
                    "form": form,
                    "popular_posts": popular_posts,
                    "trending_posts": trending_posts,
                },
            )


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/edit_profile.html'
    success_url = reverse_lazy('my_profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserProfileView(View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        books = user.posts.all()
        return render(request, 'book/user_profile.html', {'profile_user': user, 'books': books})


class CategoryListView(ListView):
    model = Category
    template_name = "book/categories.html"
    context_object_name = "categories"


class PostByCategoryView(ListView):
    model = Post
    template_name = "book/list.html"
    context_object_name = "posts"
    paginate_by = 3

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(category__id=self.kwargs["category_id"]).order_by("-created_at")
        return query


class SubscribeView(View):
    def post(self, request):
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Subscribed!")
        else:
            messages.error(request, "Invalid or duplicate email.")
        return redirect('home')
