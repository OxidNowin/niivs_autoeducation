import re

from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib import messages

from .models import *


class PollListView(View):

	def get(self, request):
		poll_model = Poll.objects.all()
		context = {
			'poll_model': poll_model,
		}
		return render(request, 'quiz/poll.html', context)

	def post(self, request):
		form = request.POST
		print(request.POST)
		try:
			poll_model = Poll(
				poll_name=form['poll_name']
			)
		except:
			messages.error(request, f'Тест с таким названием существует!')
			return redirect('poll_list')
		else:
			poll_model.save()
		poll = Poll.objects.latest('id')
		qn = 0
		for key in form.keys():
			pattern = r'^question_\d$'
			if re.search(pattern, key) and form[key]:
					qn += 1
		if qn > 0:
			for i in range(qn):
				qn_in_form = f'question_{i+1}'
				an = 0
				question_model = Question(
					poll_id = poll.id,
					text_question = form[qn_in_form]
				)
				question_model.save()
				question = Question.objects.latest('id')
				for key in form.keys():
					pattern = rf'^answer_\d_{qn_in_form}$'
					if re.search(pattern, key) and form[key]:
						an += 1
				if an > 0:
					for j in range(an):
						an_in_form = f'answer_{j+1}_{qn_in_form}'
						is_right_form = 'is_right_' + an_in_form
						is_right = False
						if is_right_form in form.keys():
							is_right = True
						answer_model = Answer(
							question_id = question.id,
							text_answer = form[an_in_form],
							is_right = is_right
						)
						answer_model.save()
				else:
					messages.error(request, 'Нет ответов к вопросу')
					return redirect('poll_list')
			messages.success(request, f'Тест {poll.poll_name} добавлен!')
		else:
			messages.error(request, 'Вы не добавили вопросы!')
			poll.delete()
		return redirect('poll_list')

class PollDetailView(View):

	def get(self, request, pk):
		poll_model = Poll.objects.get(id=pk)
		question_model = Question.objects.filter(poll_id=pk)
		answer_model = Answer.objects.filter(question_id__poll_id=pk)
		context = {
			'poll_model': poll_model,
			'question_model': question_model,
			'answer_model': answer_model,
		}
		return render(request, 'quiz/poll_detail.html', context)

	def post(self, request, pk):
		if 'delete_poll' in request.POST:
			poll_id = request.POST['delete_poll']
			p = Poll.objects.get(id=poll_id)
			p.delete()
			messages.success(request, f'Тест {p.poll_name} удален!')
		elif 'delete_question' in request.POST:
			question_id = request.POST['delete_question']
			q = Question.objects.get(id=question_id)
			q.delete()
			messages.success(request, f'Вопрос {q.text_question} удален!')
			return redirect('poll_detail', pk=pk)
		return redirect('poll_list') 
