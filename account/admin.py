from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User, Subdivision

from string import ascii_letters, digits


class MyDateInput(forms.DateInput):
    input_type = 'date'
    format = r'%Y-%m-%d'


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)
    receipt = forms.DateField(
        label='Дата приёма',
        required=True,
        widget=MyDateInput({'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('email', 'name', 'subdivision', 'education', 'education_profile', 'receipt', 'is_superuser')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают!")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data["password1"]:
            user.set_password(self.cleaned_data["password1"])
        else:
            user.set_password(
                User.objects.make_random_password(
                    length=12)
            )
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    #password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = '__all__'



class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'name', 'subdivision', 'receipt', 'is_active', 'is_admin', 'is_superuser')
    list_filter = ('is_admin', 'is_active', 'is_superuser')
    fieldsets = (
        ('Информация об аккаунте', {'fields': ('email', 'password')}),
        ('Персональная информация', {
            'fields': (
						'name', 
                        'subdivision', 
                        'education', 
                        'education_profile', 
                        'receipt',
                    )
        }),
        ('Привилегии', {'fields': ('is_admin', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        ('Информация об аккаунте', {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',)}
        ),
        ('Персональная информация', {
            'fields': (
                        'name', 
                        'subdivision', 
                        'education', 
                        'education_profile', 
                        'receipt',
                    )

        }),
        ('Права доступа:', {
            'fields': (
                    'is_superuser',
                    'is_active',
                )
            }),
    )
    search_fields = ('email',)
    ordering = ('name', 'subdivision',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(Subdivision)
admin.site.unregister(Group)