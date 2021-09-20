from django import forms
from .models import *
from account.models import User


class MyDateInput(forms.DateInput):
	input_type = 'date'
	format = r'%Y-%m-%d'

"""
class UserCardForm(forms.ModelForm):

	name = forms.CharField(
		max_length=150, 
		label="ФИО сотрудника",
		error_messages={'required': 'Введите ФИО сотрудника'})

	education = forms.CharField(
		max_length=500, 
		label="Информация об образовании",
		error_messages={'required': 'Введите информацию об обучении'})

	education_profile = forms.CharField(
		max_length=200, 
		label="Профиль обучения",
		error_messages={'required': 'Введите информацию о профиле обучения'})

	receipt = forms.DateField(
		label='Дата приёма', 
		required=True,
		widget=MyDateInput({'class': 'form-control'}))

	class Meta:
		model = User
		fields = ('name', 'subdivision', 'education', 'education_profile', 'receipt')
"""

class FirstEducationForm(forms.ModelForm):
	class Meta:
		model = FirstEducation
		fields = ('user_name', 'test','fe_file')


class PeriodEducationForm(forms.ModelForm):

	test_issueng_date = forms.DateField(
		label='Дата выдачи тестовых заданий', 
		required=True,
		widget=MyDateInput({'class': 'form-control'}))

	completion_date = forms.DateField(
		label='Дата сдачи',
		required=False,
		widget=MyDateInput({'class': 'form-control'}))

	class Meta:
		model = PeriodEducation
		fields = "__all__"