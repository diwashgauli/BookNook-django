from django.db import models


from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Category Name")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Post(models.Model):
    TRADE_CHOICES = [
        ('sale', 'Sale'),
        ('exchange', 'Exchange'),
        ('both', 'Sale or Exchange'),
    ]

    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used_like_new', 'Used - Like New'),
        ('used_good', 'Used - Good'),
        ('used_fair', 'Used - Fair'),
        ('used_poor', 'Used - Poor'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    author_name = models.CharField(max_length=100)  # Book's author
    price = models.PositiveIntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='book_images/', blank=True, null=True)

    trade_condition = models.CharField(max_length=10, choices=TRADE_CHOICES, default='sale')
    exchange_with = models.CharField(max_length=200, blank=True, null=True)  # <-- New field

    book_condition = models.CharField(
        max_length=15,
        choices=CONDITION_CHOICES,
        default='used_good',
        help_text="Condition of the book"
    )

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')  # This is already the author

    is_trending = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # comment author
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'