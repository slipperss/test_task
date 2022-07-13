from django.db.models import Count, Case, When

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (CreateModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin, DestroyModelMixin,
                                   ListModelMixin)

from .models import Post, PostUserView, Comment
from .permissions import IsPostOwnerOrStaffOrReadOnly
from .serializers import PostSerializer, PostLikeSerializer, PostDislikeSerializer, CommentSerializer
from .services import estimate_func, check_post_activity


class PostApiView(GenericViewSet, CreateModelMixin,
                  RetrieveModelMixin, UpdateModelMixin,
                  DestroyModelMixin, ListModelMixin):
    queryset = Post.objects.filter(published=True).annotate(
        likes=Count(Case(When(postlike__like=True, then=1)), distinct=True),
        dislikes=Count(Case(When(postdislike__dislike=True, then=1)), distinct=True),
        views=Count('postuserview', distinct=True),
        comments_count=Count('comments', distinct=True)
    ).select_related('author')

    serializer_class = PostSerializer
    permission_classes = [IsPostOwnerOrStaffOrReadOnly]
    lookup_field = 'id'

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        print('******', args, kwargs, request.data)
        PostUserView.objects.get_or_create(user_id=self.request.user.id, post_id=kwargs['id'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CommentView(GenericViewSet, RetrieveModelMixin, UpdateModelMixin,
                  DestroyModelMixin, ListModelMixin, CreateModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(Comment.objects.filter(user=self.request.user))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostLikeView(GenericAPIView):
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'post_id'

    def patch(self, request: bool, id: int, format=None):
        try:
            user = self.request.user
            grade_status = 'like'  # статус для функции estimate_func
            like = estimate_func(user, request, id, grade_status)
            if like:
                return Response(like, status=status.HTTP_200_OK)
            return Response(
                {'error': 'No data to show'},
                status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(
                {'error': 'Something went wrong when retrieving detail'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PostDislikeView(GenericAPIView):
    serializer_class = PostDislikeSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'post_id'

    def patch(self, request: bool, id: int, format=None):
        try:
            user = self.request.user
            grade_status = 'dislike'  # статус для функции estimate_func
            dislike = estimate_func(user, request, id, grade_status)
            if dislike:
                return Response(dislike, status=status.HTTP_200_OK)
            return Response(
                {'error': 'No data to show'},
                status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(
                {'error': 'Something went wrong when retrieving detail'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PostsAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            try:
                date_from = self.request.query_params['date_from']
                date_to = self.request.query_params['date_to']
                analyzed_data = check_post_activity(date_from, date_to)
            except:
                analyzed_data = check_post_activity()

            if analyzed_data:
                return Response(analyzed_data, status.HTTP_200_OK)
            return Response(
                {'error': 'No data to show'},
                status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(
                {'error': 'Something went wrong when retrieving detail'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
