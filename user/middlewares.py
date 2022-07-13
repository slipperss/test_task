from django.utils import timezone
from django.conf import settings

from datetime import timedelta as td
from dateutil.parser import parse

from user.models import UserAccount


class LastUserActivityMiddleware:
    """
    Проверяем когда был сделан последний запрос и обновляем поле last_request,
    обновление каждый час(настройка в settings) если запрос от пользователя поступает
    """
    KEY = "last-activity"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            last_activity = request.session.get(self.KEY)

            too_old_time = timezone.now() - td(seconds=settings.LAST_ACTIVITY_INTERVAL_SECONDS)
            # print('********', last_activity , '-' ,too_old_time, '********')
            # print(parse(last_activity) < too_old_time)
            if (last_activity is None or not last_activity) or parse(last_activity) < too_old_time:
                # print("******* Enter **********")
                UserAccount.objects.filter(id=request.user.id).update(last_request=timezone.now())
                # print('success')

            request.session[self.KEY] = timezone.now().isoformat()
        return response
