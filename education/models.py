from django.db import models
from django.core.validators import FileExtensionValidator

from quiz.models import Poll
from account.models import User

from datetime import timedelta


def user_directory_path(instance, filename):
    return f'user_{instance.user_name.id}/{filename}'


class FirstEducation(models.Model):
    """Первичное обучение"""

    user_name = models.ForeignKey(
        User,
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
        User,
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
