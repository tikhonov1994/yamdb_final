from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models

from .validators import year_validator


class CustomUser(AbstractUser):
    ROLE_USER = 'user'
    ROLE_MODERATOR = 'moderator'
    ROLE_ADMIN = 'admin'
    USERS_ROLE = (
        (ROLE_USER, 'Пользователь'),
        (ROLE_MODERATOR, 'Модератор'),
        (ROLE_ADMIN, 'Админ'),
    )
    bio = models.TextField(
        verbose_name="О себе",
        blank=True,
        null=True,
        max_length=200
    )
    role = models.CharField(
        verbose_name='Роль пользователя',
        max_length=10,
        choices=USERS_ROLE,
        default=ROLE_USER,
    )
    email = models.EmailField(
        verbose_name="Электронная почта",
        validators=[validators.validate_email],
        unique=True,
    )
    confirmation_code = models.CharField(
        null=True,
        blank=True,
        max_length=255
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['confirmation_code', 'username']

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_moderator(self):
        return self.role == self.ROLE_MODERATOR


class Category(models.Model):
    name = models.CharField(verbose_name='Название',
                            unique=True, max_length=200)
    slug = models.SlugField(verbose_name="Ссылка", unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('slug',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(verbose_name='Название',
                            unique=True, max_length=200)
    slug = models.SlugField(verbose_name="Ссылка", unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('slug',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(verbose_name='Название', max_length=200)
    year = models.PositiveSmallIntegerField(verbose_name="Год создания",
                                            blank=True, null=True,
                                            validators=[year_validator])
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        blank=True, null=True
    )
    description = models.CharField(verbose_name='Описание',
                                   max_length=1000, blank=True)
    genre = models.ManyToManyField(Genre,
                                   verbose_name='Жанр',
                                   related_name="genre_titles")

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('id',)


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Текст')
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[
            validators.MinValueValidator(0),
            validators.MaxValueValidator(10)
        ]
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Комментарий'
    )
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)
