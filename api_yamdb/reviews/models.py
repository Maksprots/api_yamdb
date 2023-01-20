from django.contrib.auth.models import AbstractUser
from django.db import models
# Эти валидаторы нужны для ограничения оценки типа: от 1 до 10
# Чтобы не было оценок 99 из 10 :)
from django.core.validators import MaxValueValidator, MinValueValidator

# Список для выбора роли
USER_ROLE_CHOICES = [
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
]
"""Выбор ролей"""


class User (AbstractUser):
    """Кастомная модель User"""

    username = models.CharField(
        max_length=32,
        default='username_default',
        unique=True
    )
    first_name = models.CharField(
        max_length=32,
        default='user_name_default'
    )
    last_name = models.CharField(
        max_length=64,
        default='user_last_name_default'
    )
    email = models.EmailField(
        verbose_name='email_address',
        blank=False,
        unique=True,
        max_length=254,
    )
    bio = models.TextField('bio', blank=True)
    role = models.CharField(
        max_length=16,
        choices=USER_ROLE_CHOICES,
        default='user',
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property                       # нужно для удобного доступа
    def is_user(self):              # чтобы не вызывать постоянно функцию
        return self.role == 'user'  # советую почитать про этот декоратор!

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return (
            self.role == 'admin'
            or self.is_superuser
            or self.is_staff
        )


class Categories(models.Model):
    """Модель категорий"""

    name = models.TextField(
        blank=False,
        unique=True,
        max_length=32
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров"""

    name = models.CharField(
        blank=False,
        unique=True,
        max_length=32
    )
    slug = models.SlugField(
        max_length=25,
        unique=True,
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений, к которым пишут отзывы"""

    name = models.CharField(
        blank=False,
        max_length=150,
    )
    year = models.IntegerField()
    description = models.TextField(
        'description',
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.PROTECT,
        related_name='category',
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle'
    )

    class Meta:
        ordering = ['-id', ]

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Модель отношения Произведение-Жанр"""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )


class Review(models.Model):
    """Модель отзывов на произведения"""

    id = models.AutoField(primary_key=True)
    title = models.ForeignKey(
        Title,
        verbose_name='titles',
        on_delete=models.PROTECT,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='rating')
    pub_date = models.DateTimeField(
        'pub_date',
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"], name="one_review_one_author"
            ),
        ]

    def __str__(self):
        return self.text


class Comments(models.Model):
    """Модель комментариев к отзывам"""

    id = models.AutoField(primary_key=True)
    review_id = models.ForeignKey(
        Review,
        verbose_name='Pu',
        related_name='comments',
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='author',
    )
    pub_date = models.DateTimeField(
        'pub_date',
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text
