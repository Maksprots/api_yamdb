from api.utils import username_validation
from django.contrib.auth.models import AbstractUser
# Эти валидаторы    нужны для ограничения оценки типа: от 1 до 10
# Чтобы не было оценок 99 из 10 :)
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User
from .utils import year_validate




class Category(models.Model):
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
    year = models.IntegerField(validators=(year_validate,))
    description = models.TextField(
        'description',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='category',
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        through_fields=('title', 'genre')
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
        default=1,
        verbose_name='rating')
    pub_date = models.DateTimeField(
        'pub_date',
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-pub_date']
        unique_together = ('title', 'author',)

    def __str__(self):
        return self.text


class Comments(models.Model):
    """Модель комментариев к отзывам"""

    id = models.AutoField(primary_key=True)
    review = models.ForeignKey(
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
