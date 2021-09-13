from django.db import models

class Poll(models.Model):
	poll_name = models.CharField('Название теста', max_length=300, unique=True)

	class Meta:
		ordering = ['poll_name']
		verbose_name = "Тест"
		verbose_name_plural = "Тесты"

	def __str__(self):
		return self.poll_name

class Question(models.Model):
	poll = models.ForeignKey(Poll, on_delete=models.CASCADE, verbose_name='Тест')
	text_question = models.CharField('Текст вопроса', max_length=500)

	class Meta:
		ordering = ['poll']
		verbose_name = "Вопрос"
		verbose_name_plural = "Вопросы"

	def __str__(self):
		return f'{self.poll}: {self.text_question}'

class Answer(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
	text_answer = models.CharField('Ответ на вопрос', max_length=500)
	is_right = models.BooleanField('Правильный ответ')

	class Meta:
		ordering = ['question']
		verbose_name = "Ответ"
		verbose_name_plural = "Ответы"

	def __str__(self):
		return f'{self.question}: {self.text_answer}'
		