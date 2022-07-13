from django.contrib import admin

from .models import Category, Post, PostLike, PostDislike, PostUserView, Comment

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostLike)
admin.site.register(PostDislike)
admin.site.register(PostUserView)
