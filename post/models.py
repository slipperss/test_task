from django.db import models
from django.utils import timezone

from user.models import UserAccount


class Category(models.Model):
    """Класс модели категорий сетей"""
    name = models.CharField("Категория", max_length=50)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Post(models.Model):
    """Класс модели поста"""
    author = models.ForeignKey(
        UserAccount,
        verbose_name="Автор",
        on_delete=models.CASCADE,
        null=True,
    )
    title = models.CharField("Тема", max_length=500)
    subtopic = models.TextField("Краткое содержание", max_length=5000)
    text = models.TextField("Полное содержание", max_length=10000000)
    created_date = models.DateTimeField("Дата создания", auto_now_add=True)
    published_date = models.DateTimeField(
        "Дата публикации",
        default=timezone.now,
        blank=True,
        null=True
    )
    image = models.ImageField("Изображение", upload_to="post/", blank=True, null=True)
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    published = models.BooleanField("Опубликовать?", default=True)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-created_date"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Модель коментариев к постам"""
    user = models.ForeignKey(UserAccount, verbose_name="Пользователь", on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, verbose_name="Пост", related_name="comments", on_delete=models.CASCADE
    )
    text = models.TextField("Сообщение")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f'{self.user.id}, {self.user.first_name}, {self.user.last_name}'


class PostLike(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    liked_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'

    def date_trunc_field(self):
        return self.liked_at.date()

    def __str__(self):
        return f'{self.user} - {self.post.title}'


class PostDislike(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    dislike = models.BooleanField(default=False)
    disliked_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Дизлайк'
        verbose_name_plural = 'Дизлайки'

    def __str__(self):
        return f'{self.user} - {self.post.title}'


class PostUserView(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    viewed_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Просмотр пользователей на постах'
        verbose_name_plural = 'Просмотры пользователей на постах'

    def __str__(self):
        return f'{self.user.email} - {self.post.title}'
