from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.urls import reverse
from django.utils.text import slugify


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('У пользователя обязательно должен быть e-mail')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    email = models.EmailField(
        verbose_name='E-mail',
        max_length=255,
        unique=True,
        blank=True,
        null=True,
    )

    name = models.CharField(
	    'ФИО пользователя',
	    max_length=250,
    )

    password = models.CharField(
        'Пароль',
        max_length=100,
        blank=True
    )

    subdivision = models.ForeignKey(
        'Subdivision',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Подразделение'
    )

    education = models.TextField('Образование')

    education_profile = models.CharField('Профиль образования', max_length=80)

    receipt = models.DateField('Дата приема')

    slug = models.SlugField(
        max_length=75,
        blank=True,
        editable=False
    )

    is_active = models.BooleanField('Активный пользователь', default=True)
    is_admin = models.BooleanField('Администратор', default=False)
    is_superuser =  models.BooleanField('Супер пользователь', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_absolute_url(self):
        kwargs = {
            'pk': self.id,
            'slug': self.slug
        }
        return reverse('user_detail', kwargs=kwargs)

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_super(self):
        return self.is_superuser

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['subdivision', 'name']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


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