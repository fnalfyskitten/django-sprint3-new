from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

TITLE_MAX_LENGTH = 256


class BasePost(models.Model):
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True


class Category(BasePost):
    title = models.CharField(max_length=TITLE_MAX_LENGTH,
                             verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; '
        'разрешены символы латиницы, цифры, дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:50]


class Location(BasePost):
    name = models.CharField(max_length=TITLE_MAX_LENGTH,
                            verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

        def __str__(self):
            return self.name[:50]


class PostManager(models.Manager):
    def get_published(self):
        now = timezone.now()
        return self.filter(
            is_published=True,
            pub_date__lte=now,
            category__is_published=True
        ).select_related('author', 'location', 'category')


class Post(BasePost):
    title = models.CharField(max_length=TITLE_MAX_LENGTH,
                             verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем — '
        'можно делать отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )

    objects = PostManager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        default_related_name = 'post'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title[:50]
