from django import forms
from .models import *

class PollForm(forms.ModelForm):

	class Meta:
		model = Poll
		fields = '__all__'

class QuestionForm(forms.ModelForm):

	class Meta:
		model = Question
		fields = '__all__'

class AnswerForm(forms.ModelForm):

	class Meta:
		model = Answer
		fields = '__all__'