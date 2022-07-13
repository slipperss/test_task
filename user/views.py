from django.contrib.auth.models import update_last_login

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from user.models import UserAccount
from user.services import check_user_activity


class UserActivityDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id, format=None):
        try:
            analyzed_data = check_user_activity(id) # достаем данные о активности пользователя
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


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = UserAccount.objects.get(email=request.data['email'])
            update_last_login(sender=None, user=user) # обновляем поле last_login у юзера когда у он получает токен
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
