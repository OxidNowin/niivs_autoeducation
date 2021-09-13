from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify
from django.urls import reverse

from quiz.models import Poll

from datetime import timedelta


def user_directory_path(instance, filename):
    return f'user_{instance.user_name.id}/{filename}'


class UserCard(models.Model):
    """Пользователь"""

    name = models.CharField("ФИО пользователя", max_length=150)

    # email = models.EmailField(max_length=150, unique=True)

    subdivision = models.ForeignKey(
        "Subdivision",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Подразделение"
    )

    education = models.TextField("Образование")

    education_profile = models.CharField("Профиль образования", max_length=80)

    receipt = models.DateField("Дата приема")

    slug = models.SlugField(
        max_length=75,
        blank=True,
        editable=False
    )

    def get_absolute_url(self):
        kwargs = {
            'pk': self.id,
            'slug': self.slug
        }
        return reverse('usercard_detail', kwargs=kwargs)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Subdivision(models.Model):
    """Подразделение"""

    subdivision_name = models.CharField(
        "Аббревиатура подразделения",
        max_length=20,
        unique=True
    )

    def __str__(self):
        return self.subdivision_name

    class Meta:
        ordering = ["subdivision_name"]
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"


class FirstEducation(models.Model):
    """Первичное обучение"""

    user_name = models.ForeignKey(
        "UserCard",
        on_delete=models.CASCADE,
        verbose_name="ФИО"
    )

    date = models.DateField("Дата сдачи", blank=True)

    estimate = models.BooleanField("Отметка о сдаче", null=True)

    fe_file = models.FileField(
        upload_to=user_directory_path,
        verbose_name="Подтверждение обучения",
        blank=True,
        validators=([FileExtensionValidator(['xlsx', 'docx'])])
    )

    test = models.ForeignKey(
        Poll, 
        on_delete=models.SET_NULL,
        verbose_name="Тест",
        null=True,
    )

    def save(self, *args, **kwargs):
        self.date = UserCard.objects.get(name=self.user_name.name).receipt + timedelta(days=+90)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user_name.name

    class Meta:
        verbose_name = "Первичное обучение"
        verbose_name_plural = "Первичные обучения"


class PeriodEducation(models.Model):
    """Периодическое обучение"""

    year_edu = 'YE'
    subdivision_edu = 'SE'

    type_choices = [
        (year_edu, 'Годовое обучение'),
        (subdivision_edu, 'Обучение по подразделениям')
    ]

    user_name = models.ForeignKey(
        "UserCard",
        on_delete=models.CASCADE,
        verbose_name="ФИО"
    )

    type = models.CharField(
        verbose_name='Тип периодического обучения',
        max_length=30,
        choices=type_choices,
        default=year_edu,
    )

    test_issueng_date = models.DateField("Дата выдачи тестовых заданий")

    completion_date = models.DateField("Дата сдачи", blank=True, null=True)

    percent_of_complete = models.PositiveSmallIntegerField(
        "Процент выполнения",
        blank=True,
        null=True
    )

    pe_file = models.FileField(
        upload_to=user_directory_path,
        verbose_name="Подтверждение обучения",
        blank=True,
        validators=([FileExtensionValidator(['xlsx', 'docx'])])
    )

    def save(self, *args, **kwargs):
        if self.type == self.subdivision_edu:
            self.completion_date = self.test_issueng_date + timedelta(days=+1)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user_name.name

    class Meta:
        verbose_name = "Периодическое обучение"
        verbose_name_plural = "Периодические обучения"
