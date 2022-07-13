from rest_framework import serializers

from .models import Post, PostLike, PostDislike, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'user', 'text', 'created_at',)
        read_only_fields = ('user', 'created_at')


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(allow_null=True, read_only=True)
    dislikes = serializers.IntegerField(allow_null=True, read_only=True)
    views = serializers.IntegerField(allow_null=True, read_only=True)
    comments_count = serializers.IntegerField(allow_null=True, read_only=True)
    published_date_field = serializers.DateTimeField(source='published_date', read_only=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'author',
            'title',
            'subtopic',
            'text',
            'published_date_field',
            'image',
            'category',
            'likes',
            'dislikes',
            'views',
            'comments_count',
        )
        read_only_fields = ('author',)


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ('like',)


class PostDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostDislike
        fields = ('dislike',)
