from django.utils.dateparse import parse_date
from django.db.models import Q

from .models import PostLike, PostDislike, PostUserView


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


def estimate_func(user, request: bool, id: int, grade_status: str):
    """
    Создание лайка(дизлайка) и проверка на существование лайка(дизлайка)
    При лайке(дизлайке) = True, дизлайк(лайк) не может существовать
    """
    bool_check = request.data[grade_status]  # проверка на True or False

    if grade_status == 'like':
        if bool(bool_check) == True:
            dislike_existing = get_or_none(PostDislike, user_id=user.id, post_id=id)  # существование дизлайка
            if dislike_existing:
                dislike_existing.delete()  # удаление при существовании
        like = PostLike.objects.update_or_create(user_id=user.id, post_id=id,
                                                 defaults={grade_status: bool_check})
        result = {
            'post_id': id,
            'user_id': user.id,
            'like': like[1]
        }
        return result

    if grade_status == 'dislike':
        if bool(bool_check) == True:
            like_existing = get_or_none(PostLike, user_id=user.id, post_id=id)  # существование дизлайка
            if like_existing:
                like_existing.delete()  # удаление при существовании
        dislike = PostDislike.objects.update_or_create(user_id=user.id, post_id=id,
                                                       defaults={grade_status: bool_check})
        result = {
            'post_id': id,
            'user_id': user.id,
            'dislike': dislike[1]
        }
        return result


# Проверка активности на всех постах (лайки, дизлайки, просмотры)
def check_post_activity(date_from: str = '2022-07-06', date_to: str = '2022-07-11'):
    parsed_date_from = parse_date(date_from)  # парсим дату с str в datetime.date
    parsed_date_to = parse_date(date_to)  # парсим дату с str в datetime.date

    likes_count = PostLike.objects.filter(Q(liked_at__gt=parsed_date_from) &
                                          Q(liked_at__lt=parsed_date_to) &
                                          Q(like=True)).count()
    dislike_count = PostDislike.objects.filter(Q(disliked_at__gt=parsed_date_from) &
                                               Q(disliked_at__lt=parsed_date_to) &
                                               Q(dislike=True)).count()
    views_count = PostUserView.objects.filter(Q(viewed_at__gt=parsed_date_from) &
                                              Q(viewed_at__lt=parsed_date_to)).count()
    return {
        'likes_count': likes_count,
        'dislike_count': dislike_count,
        'views_count': views_count,
    }
