from rest_framework.serializers import ModelSerializer

from user.models import UserAccount


class UserAccountSerializer(ModelSerializer):
    class Meta:
        model = UserAccount
        fields = '__all__'
