from user.models import UserAccount


# Проверка активности юзера по айди (last_login, last_request и ост инфа по профилю)
def check_user_activity(id: int):
    user_obj = UserAccount.objects.get(id=id)
    return {
        'first_name': user_obj.first_name,
        'last_name': user_obj.last_name,
        'email': user_obj.email,
        'date_joined': user_obj.date_joined,
        'last_login': user_obj.last_login,
        'last_request': user_obj.last_request
    }
